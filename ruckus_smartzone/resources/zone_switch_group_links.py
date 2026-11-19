"""Zone switch group link resource wrapper.

A Switch Manager switch group is tied to a public-API zone by a link record
``{id, zoneId, switchGroupId, link}``. The record lives in the public API's
``/zoneSwitchGroupLinks`` collection, not in Switch Manager. Zone ids come from
``client.zones`` and switch group ids from ``client.switchm.groups``.

The list endpoint accepts at most one of its ``zoneId``, ``switchGroupId`` and
``domainId`` filters; the controller answers two or more with HTTP 500. A
``switchGroupId`` filter naming an unknown group also gets HTTP 500, while an
unknown ``zoneId`` gets an empty list.

``PUT`` takes the full ``{zoneId, switchGroupId, link}`` body, so :meth:`update`
reads the record, overlays the given fields and writes the merged body back.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.resources.base import BaseResource

_PATH = "zoneSwitchGroupLinks"

LINK_FIELDS = ("zoneId", "switchGroupId", "link")


class ZoneSwitchGroupLinksResource(BaseResource):
    """Operations on zone-to-switch-group links (``/zoneSwitchGroupLinks``)."""

    def list(
        self,
        *,
        zone_id: Optional[str] = None,
        switch_group_id: Optional[str] = None,
        domain_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return every link matching the given filter, following pagination.

        Raises:
            ValueError: If more than one filter is given.
        """
        params = {
            key: value
            for key, value in (
                ("zoneId", zone_id),
                ("switchGroupId", switch_group_id),
                ("domainId", domain_id),
            )
            if value is not None
        }
        if len(params) > 1:
            raise ValueError(
                "Filter by at most one of zone_id, switch_group_id and domain_id"
            )
        return self.client.paginate(_PATH, params=params or None)

    def get(self, link_id: str) -> Optional[Dict[str, Any]]:
        """Return one link by id."""
        return self.client.get(f"{_PATH}/{link_id}")

    def find(self, zone_id: str, switch_group_id: str) -> Optional[Dict[str, Any]]:
        """Return the link between a zone and a switch group, or ``None``.

        Links are listed by zone and matched on the switch group client-side.
        The record is returned whatever its ``link`` flag.

        Raises:
            ValueError: If more than one link joins the pair.
        """
        matches = [
            item
            for item in self.list(zone_id=zone_id)
            if item.get("zoneId") == zone_id
            and item.get("switchGroupId") == switch_group_id
        ]
        if len(matches) > 1:
            raise ValueError(
                f"Multiple links found for zone {zone_id!r} "
                f"and switch group {switch_group_id!r}"
            )
        return matches[0] if matches else None

    def create(
        self, zone_id: str, switch_group_id: str, link: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Link a switch group to a zone; returns ``{id}``."""
        body = {"zoneId": zone_id, "switchGroupId": switch_group_id, "link": link}
        return self.client.post(_PATH, json=body)

    def update(self, link_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Change a link's ``zoneId``, ``switchGroupId`` or ``link`` (PUT).

        The current record is read and the given fields overlaid on it, so the
        PUT carries a complete body.

        Raises:
            ValueError: If ``fields`` is empty or names a field outside
                :data:`LINK_FIELDS`.
        """
        if not fields:
            raise ValueError("Provide at least one field to change")
        unknown = sorted(set(fields) - set(LINK_FIELDS))
        if unknown:
            raise ValueError(
                f"Unknown link fields {unknown}; allowed fields are {list(LINK_FIELDS)}"
            )
        current = self.get(link_id) or {}
        body = {key: current[key] for key in LINK_FIELDS if key in current}
        body.update(fields)
        return self.client.put(f"{_PATH}/{link_id}", json=body)

    def delete(self, link_id: str) -> Optional[Dict[str, Any]]:
        """Delete a link by id."""
        return self.client.delete(f"{_PATH}/{link_id}")
