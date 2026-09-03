"""Access point resource wrapper.

Access points are identified by a global MAC namespace, so the create/read/modify/
delete and move operations here are the only ones in the SDK not fenced inside a
zone. Two responsibilities are owned here rather than by the caller:

- **Chunking.** ``POST /aps/move`` accepts at most 50 MACs per call; :meth:`move`
  splits a larger set into batches and reports each batch's outcome, so partial
  success is visible rather than swallowed.
- **A pre-flight zone guard.** :meth:`move`, :meth:`update` and :meth:`replace`
  take an ``expected_zone_id`` and refuse, before any write, if an AP is not in
  that zone — so a wrong MAC cannot touch an AP the caller did not mean to change.

MACs are normalised to SmartZone's colon-uppercase form for every request.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE, MAX_MOVE_BATCH, MAX_PAGE_SIZE
from ruckus_smartzone.exceptions import SmartZoneAPIError, SmartZoneZoneMismatchError
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.resources.base import BaseResource

_PATH = "aps"


@dataclass
class MoveBatchResult:
    """Outcome of one ``POST /aps/move`` call within a chunked move."""

    macs: List[str]
    ok: bool
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class MoveResult:
    """Aggregate outcome of a chunked :meth:`AccessPointsResource.move`."""

    batches: List[MoveBatchResult] = field(default_factory=list)

    @property
    def all_succeeded(self) -> bool:
        """True when every batch succeeded."""
        return all(batch.ok for batch in self.batches)

    @property
    def moved_macs(self) -> List[str]:
        """MACs in batches that succeeded."""
        return [mac for batch in self.batches if batch.ok for mac in batch.macs]

    @property
    def failed_macs(self) -> List[str]:
        """MACs in batches that failed."""
        return [mac for batch in self.batches if not batch.ok for mac in batch.macs]


def _chunk(items: List[str], size: int) -> List[List[str]]:
    """Split ``items`` into consecutive lists of at most ``size``."""
    return [items[i : i + size] for i in range(0, len(items), size)]


class AccessPointsResource(BaseResource):
    """Operations on access points (``/aps``)."""

    def list(
        self, zone_id: Optional[str] = None, **params: Any
    ) -> List[Dict[str, Any]]:
        """Return access points, following pagination.

        Args:
            zone_id: Restrict the listing to one zone.
            **params: Extra query parameters (e.g. ``domainId``).
        """
        query = dict(params)
        if zone_id is not None:
            query["zoneId"] = zone_id
        return self.client.paginate(_PATH, params=query or None)

    def get(self, mac: str) -> Optional[Dict[str, Any]]:
        """Return one AP's configuration by MAC, including its ``zoneId``."""
        return self.client.get(f"{_PATH}/{normalize_mac(mac)}")

    def create(self, ap: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create an AP from a full request body (requires ``mac`` and ``zoneId``)."""
        return self.client.post(_PATH, json=ap)

    def update(
        self,
        mac: str,
        changes: Dict[str, Any],
        *,
        expected_zone_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Apply a partial modification to an AP (PATCH).

        Args:
            mac: AP MAC.
            changes: Partial ``ap_modifyAP`` body.
            expected_zone_id: When set, the AP is refused unless it is in this
                zone (see :meth:`_verify_zone`).
        """
        norm = normalize_mac(mac)
        if expected_zone_id is not None:
            self._verify_zone([norm], expected_zone_id)
        return self.client.patch(f"{_PATH}/{norm}", json=changes)

    def replace(
        self,
        mac: str,
        ap: Dict[str, Any],
        *,
        expected_zone_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Replace an AP's configuration wholesale (PUT).

        Args:
            mac: AP MAC.
            ap: Full ``ap_modifyAP`` body.
            expected_zone_id: When set, the AP is refused unless it is in this
                zone (see :meth:`_verify_zone`).
        """
        norm = normalize_mac(mac)
        if expected_zone_id is not None:
            self._verify_zone([norm], expected_zone_id)
        return self.client.put(f"{_PATH}/{norm}", json=ap)

    def delete(
        self, mac: str, *, validate_mesh: Optional[bool] = None
    ) -> Optional[Dict[str, Any]]:
        """Delete an AP by MAC.

        Args:
            mac: AP MAC.
            validate_mesh: When set, passed as the ``validateMesh`` query flag.
        """
        params: Optional[Dict[str, Any]] = None
        if validate_mesh is not None:
            params = {"validateMesh": validate_mesh}
        return self.client.delete(f"{_PATH}/{normalize_mac(mac)}", params=params)

    def operational_summary(self, mac: str) -> Optional[Dict[str, Any]]:
        """Return an AP's live operational state and applied configuration.

        This is how a caller confirms an AP has checked in and applied a
        configuration change.
        """
        return self.client.get(f"{_PATH}/{normalize_mac(mac)}/operational/summary")

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return bulk AP state via ``POST /query/ap``, following pagination.

        The query endpoint pages by ``page``/``limit`` in the POST body (one-based
        pages) over the ``{totalCount, hasMore, firstIndex, list}`` shape.

        Args:
            criteria: Extra query criteria (e.g. ``filters``, ``fullTextSearch``)
                merged into every page's body.
            page_size: Items per page; clamped to the API maximum (1000).
        """
        limit = min(page_size, MAX_PAGE_SIZE)
        results: List[Dict[str, Any]] = []
        fetched = 0
        page = 1
        while True:
            body = dict(criteria or {})
            body["page"] = page
            body["limit"] = limit
            response = self.client.post("query/ap", json=body) or {}

            items = response.get("list") or []
            results.extend(items)
            fetched += len(items)

            if not items:
                break
            total = response.get("totalCount")
            has_more = response.get("hasMore")
            if has_more is False:
                break
            if has_more is None:
                if total is not None and fetched >= total:
                    break
                if len(items) < limit:
                    break
            page += 1

        return results

    def move(
        self,
        macs: List[str],
        *,
        target_zone_id: str,
        expected_zone_id: Optional[str] = None,
        chunk_size: int = MAX_MOVE_BATCH,
    ) -> MoveResult:
        """Move APs to another zone, chunked at 50.

        The MACs are normalised and, when ``expected_zone_id`` is set, every AP is
        pre-flight checked before any move is issued. The move is then split into
        batches of at most ``chunk_size`` (the endpoint's 50-MAC cap) and each
        batch's outcome is recorded, so a failed batch is visible rather than
        silently swallowed; later batches are still attempted.

        This moves an AP between zones only. Placing an AP in an AP group is a
        separate operation — set the AP's ``apGroupId`` via :meth:`update` (which
        :meth:`APGroupsResource.add_member` wraps). Passing an AP group into the
        move endpoint records group membership without re-homing the AP's
        ``apGroupId``, leaving the two out of sync, so that path is not offered.

        Args:
            macs: AP MACs to move.
            target_zone_id: Destination zone id.
            expected_zone_id: When set, every AP is refused unless it is in this
                zone (see :meth:`_verify_zone`); no move is issued on a mismatch.
            chunk_size: Maximum MACs per call; capped at the endpoint's limit.

        Returns:
            A :class:`MoveResult` with one :class:`MoveBatchResult` per batch.
        """
        normalized = [normalize_mac(mac) for mac in macs]
        if expected_zone_id is not None:
            self._verify_zone(normalized, expected_zone_id)

        batch_size = min(chunk_size, MAX_MOVE_BATCH)
        result = MoveResult()
        for batch in _chunk(normalized, batch_size):
            body: Dict[str, Any] = {
                "apMacs": batch,
                "targetZoneId": target_zone_id,
            }
            try:
                response = self.client.post(f"{_PATH}/move", json=body)
                result.batches.append(
                    MoveBatchResult(macs=batch, ok=True, response=response)
                )
            except SmartZoneAPIError as exc:
                result.batches.append(
                    MoveBatchResult(macs=batch, ok=False, error=str(exc))
                )
        return result

    def _verify_zone(self, macs: List[str], expected_zone_id: str) -> None:
        """Refuse unless every AP in ``macs`` is in ``expected_zone_id``.

        Args:
            macs: Normalised AP MACs to check.
            expected_zone_id: Zone id every AP must currently be in.

        Raises:
            SmartZoneZoneMismatchError: If any AP is in a different zone (or has
                none). No AP is modified when this is raised.
        """
        mismatches: Dict[str, Optional[str]] = {}
        for mac in macs:
            detail = self.get(mac) or {}
            actual = detail.get("zoneId")
            if actual != expected_zone_id:
                mismatches[mac] = actual
        if mismatches:
            summary = ", ".join(
                f"{mac} in {zone!r}" for mac, zone in mismatches.items()
            )
            raise SmartZoneZoneMismatchError(
                f"Expected zone {expected_zone_id!r} but found: {summary}",
                mismatches=mismatches,
            )
