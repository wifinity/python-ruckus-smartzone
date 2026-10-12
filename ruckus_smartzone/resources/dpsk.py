"""DPSK (Dynamic PSK) key resource wrapper.

DPSK keys are per-user passphrases bound to a DPSK-enabled WLAN. This wraps the
``/rkszones/{zoneId}/wlans/{id}/dpsk`` collection plus the zone-level DPSK list
and the zone's delete-expired-keys setting.

The API has no single-key create or per-key DELETE: keys are created through
``batchGenUnbound`` (``create`` is the one-key form of :meth:`generate`) and
deleted by POSTing an ``idList`` to the collection. ``PATCH`` accepts only
``userName``.
"""

from typing import Any, Dict, Iterable, List, Optional, Union

from ruckus_smartzone.exceptions import SmartZoneAPIError, SmartZoneNotFoundError
from ruckus_smartzone.resources.base import BaseResource

DELETE_EXPIRED_INTERVALS = ("Never", "AfterOneDay", "AfterSixMonths")


def _path(zone_id: str, wlan_id: str) -> str:
    return f"rkszones/{zone_id}/wlans/{wlan_id}/dpsk"


class DPSKResource(BaseResource):
    """Operations on the DPSK keys of a zone's WLANs."""

    def list(self, zone_id: str, wlan_id: str, **params: Any) -> List[Dict[str, Any]]:
        """Return every DPSK key of a WLAN, following pagination."""
        return self.client.paginate(_path(zone_id, wlan_id), params=params or None)

    def list_zone(self, zone_id: str, **params: Any) -> List[Dict[str, Any]]:
        """Return every DPSK key across all WLANs in a zone, following pagination."""
        return self.client.paginate(f"rkszones/{zone_id}/dpsk", params=params or None)

    def get(self, zone_id: str, wlan_id: str, dpsk_id: str) -> Optional[Dict[str, Any]]:
        """Return one DPSK key by id.

        The detail endpoint answers with the paged list shape; a single-item
        ``list`` is unwrapped to the key itself.

        Raises:
            SmartZoneNotFoundError: If the response lists no key.
        """
        body = self.client.get(f"{_path(zone_id, wlan_id)}/{dpsk_id}")
        if isinstance(body, dict) and "list" in body:
            items: List[Dict[str, Any]] = body.get("list") or []
            if not items:
                raise SmartZoneNotFoundError(f"No DPSK key found with id {dpsk_id!r}")
            return items[0]
        return body

    def generate(
        self,
        zone_id: str,
        wlan_id: str,
        *,
        amount: Optional[int] = None,
        passphrases: Optional[Iterable[str]] = None,
        user_name: Optional[str] = None,
        vlan_id: Optional[int] = None,
        user_role_id: Optional[str] = None,
        group_dpsk: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Batch-generate DPSK keys on a WLAN.

        Keys get controller-generated passphrases unless ``passphrases`` is
        given. With ``amount`` above 1 the controller suffixes ``user_name``
        with a zero-based index (``student_0``, ``student_1``, …).

        Passphrases must be unique on the WLAN (a reused one is rejected with
        ``SmartZoneValidationError``); user names are not checked for
        uniqueness.

        Returns:
            ``{resultCount, dpskInfoList}`` as reported by the controller.
        """
        body: Dict[str, Any] = {}
        if amount is not None:
            body["amount"] = amount
        if passphrases is not None:
            body["passphraseList"] = list(passphrases)
        if user_name is not None:
            body["userName"] = user_name
        if vlan_id is not None:
            body["vlanId"] = vlan_id
        if user_role_id is not None:
            body["userRoleId"] = user_role_id
        if group_dpsk is not None:
            body["groupDpsk"] = group_dpsk
        return (
            self.client.post(f"{_path(zone_id, wlan_id)}/batchGenUnbound", json=body)
            or {}
        )

    def create(
        self,
        zone_id: str,
        wlan_id: str,
        *,
        user_name: str,
        passphrase: Optional[str] = None,
        vlan_id: Optional[int] = None,
        user_role_id: Optional[str] = None,
        group_dpsk: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Create one DPSK key and return it.

        The passphrase is controller-generated when ``passphrase`` is omitted.
        ``group_dpsk=True`` makes a group key shared by many devices rather than
        one bound to the MAC of its first user. The controller accepts a
        duplicate ``user_name``, so check :meth:`find_by_user_name` first when
        the call must be idempotent.

        Raises:
            SmartZoneAPIError: If the controller reports no created key.
        """
        result = self.generate(
            zone_id,
            wlan_id,
            amount=1,
            passphrases=[passphrase] if passphrase is not None else None,
            user_name=user_name,
            vlan_id=vlan_id,
            user_role_id=user_role_id,
            group_dpsk=group_dpsk,
        )
        created: List[Dict[str, Any]] = result.get("dpskInfoList") or []
        if not created:
            raise SmartZoneAPIError(
                f"DPSK create for {user_name!r} returned no key", response_data=result
            )
        return created[0]

    def update(
        self, zone_id: str, wlan_id: str, dpsk_id: str, *, user_name: str
    ) -> Optional[Dict[str, Any]]:
        """Rename a DPSK key (PATCH); ``userName`` is the only modifiable field."""
        return self.client.patch(
            f"{_path(zone_id, wlan_id)}/{dpsk_id}", json={"userName": user_name}
        )

    def delete_many(self, zone_id: str, wlan_id: str, dpsk_ids: Iterable[str]) -> int:
        """Delete DPSK keys by id; returns the controller's deleted count.

        An empty ``dpsk_ids`` makes no request and returns 0.
        """
        ids = list(dpsk_ids)
        if not ids:
            return 0
        result = self.client.post(_path(zone_id, wlan_id), json={"idList": ids}) or {}
        return int(result.get("resultCount") or 0)

    def delete(self, zone_id: str, wlan_id: str, dpsk_id: str) -> int:
        """Delete one DPSK key by id; returns the controller's deleted count."""
        return self.delete_many(zone_id, wlan_id, [dpsk_id])

    def upload(
        self,
        zone_id: str,
        wlan_id: str,
        csv: Union[bytes, str],
        *,
        filename: str = "dpsk.csv",
    ) -> Dict[str, Any]:
        """Upload a DPSK CSV file to a WLAN.

        Returns:
            ``{resultCount, dpskInfoList}`` as reported by the controller.
        """
        content = csv.encode("utf-8") if isinstance(csv, str) else csv
        files = {"uploadFile": (filename, content, "text/csv")}
        return self.client.post(f"{_path(zone_id, wlan_id)}/upload", files=files) or {}

    def find_by_user_name(
        self, zone_id: str, wlan_id: str, user_name: str
    ) -> Dict[str, Any]:
        """Return the single DPSK key on a WLAN whose ``userName`` matches exactly.

        Raises:
            SmartZoneNotFoundError: If no key has that user name.
            ValueError: If more than one key has that user name.
        """
        matches = [
            key
            for key in self.list(zone_id, wlan_id)
            if key.get("userName") == user_name
        ]
        if not matches:
            raise SmartZoneNotFoundError(
                f"No DPSK key found with user name {user_name!r}"
            )
        if len(matches) > 1:
            raise ValueError(f"Multiple DPSK keys found with user name {user_name!r}")
        return matches[0]

    def get_delete_expired(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """Return the zone's delete-expired-DPSK setting (``{deleteExpiredDpsk}``)."""
        return self.client.get(f"rkszones/{zone_id}/deleteExpiredDpsk")

    def set_delete_expired(
        self, zone_id: str, interval: str
    ) -> Optional[Dict[str, Any]]:
        """Set when the zone deletes expired DPSK keys.

        Args:
            interval: One of ``Never``, ``AfterOneDay``, ``AfterSixMonths``.

        Raises:
            ValueError: If ``interval`` is not an accepted value.
        """
        if interval not in DELETE_EXPIRED_INTERVALS:
            raise ValueError(
                f"interval must be one of {DELETE_EXPIRED_INTERVALS}, got {interval!r}"
            )
        return self.client.put(
            f"rkszones/{zone_id}/deleteExpiredDpsk",
            json={"deleteExpiredDpsk": interval},
        )
