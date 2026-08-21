"""AP group resource wrapper.

An AP group is a zone-scoped bundle whose radios are pre-pointed at WLAN groups
(``radioConfig.radio{24g,5g,5gLower,5gUpper,6g}.wlanGroupId``), so moving an AP
into a group is what changes the SSIDs that AP broadcasts. An AP belongs to one
AP group per zone; its zone placement is a separate concern owned by
``access_points.move``.

This wraps ``/rkszones/{zoneId}/apgroups`` and two sub-resources: membership at
``/members/{apMac}`` (keyed on the global AP MAC namespace) and the per-radio
``wlanGroupId`` overrides under ``/radioConfig/{radio}/wlanGroupId``.

``update`` (PATCH) carries only the fields given. ``replace`` (PUT) is a
full-object replace: the controller rejects a partial body and rejects an
echoed-back detail body, so a PUT must carry a complete, curated body.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.resources.base import BaseResource, find_one_by_name
from ruckus_smartzone.validation import validate_group_name

_RADIOS = ("radio24g", "radio5g", "radio5gLower", "radio5gUpper", "radio6g")


def _path(zone_id: str) -> str:
    return f"rkszones/{zone_id}/apgroups"


def _members_path(zone_id: str, group_id: str) -> str:
    return f"{_path(zone_id)}/{group_id}/members"


def _validate_radio(radio: str) -> str:
    if radio not in _RADIOS:
        raise ValueError(f"radio must be one of {_RADIOS}, got {radio!r}")
    return radio


class APGroupsResource(BaseResource):
    """Operations on AP groups and their members within a zone."""

    def list(self, zone_id: str, **params: Any) -> List[Dict[str, Any]]:
        """Return every AP group in a zone, following pagination."""
        return self.client.paginate(_path(zone_id), params=params or None)

    def get(self, zone_id: str, group_id: str) -> Optional[Dict[str, Any]]:
        """Return one AP group by id, including its ``radioConfig``."""
        return self.client.get(f"{_path(zone_id)}/{group_id}")

    def get_default(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """Return the zone's default AP group."""
        return self.client.get(f"{_path(zone_id)}/default")

    def find_by_name(self, zone_id: str, name: str) -> Dict[str, Any]:
        """Return the single AP group whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no group has that name.
            ValueError: If more than one group has that name.
        """
        return find_one_by_name(self.list(zone_id), name, kind="AP group")

    def create(
        self,
        zone_id: str,
        name: str,
        *,
        description: Optional[str] = None,
        **fields: Any,
    ) -> Optional[Dict[str, Any]]:
        """Create an AP group; returns ``{id, ...}``.

        The name is validated locally against the controller's constraints.
        Extra AP-group body fields (e.g. ``radioConfig``) are passed through.
        Some zones reject a minimal body and need a fuller one, depending on
        their AP firmware, so pass the fields the target zone requires.
        """
        validate_group_name(name)
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        body.update(fields)
        return self.client.post(_path(zone_id), json=body)

    def update(
        self, zone_id: str, group_id: str, changes: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply a partial modification to an AP group (PATCH).

        The body carries only the fields given.

        Raises:
            ValueError: If ``changes`` is empty.
        """
        if not changes:
            raise ValueError("Provide at least one field to change")
        if "name" in changes:
            validate_group_name(changes["name"])
        return self.client.patch(f"{_path(zone_id)}/{group_id}", json=changes)

    def replace(
        self, zone_id: str, group_id: str, group: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Replace an AP group's configuration wholesale (PUT).

        This is a full-object replace: the body must be complete and curated. A
        partial body, or a detail body read back and echoed, is rejected by the
        controller.
        """
        if "name" in group:
            validate_group_name(group["name"])
        return self.client.put(f"{_path(zone_id)}/{group_id}", json=group)

    def delete(self, zone_id: str, group_id: str) -> Optional[Dict[str, Any]]:
        """Delete an AP group by id."""
        return self.client.delete(f"{_path(zone_id)}/{group_id}")

    def upsert_by_name(
        self, zone_id: str, name: str, description: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create the group, or update it in place if one already has the name.

        A get-by-name → create-or-update convenience built on POST-or-PATCH.
        Returns the create result when creating, or the PATCH result when
        updating an existing group.
        """
        try:
            existing = self.find_by_name(zone_id, name)
        except SmartZoneNotFoundError:
            return self.create(zone_id, name, description=description)
        group_id = existing["id"]
        if description is None:
            return existing
        return self.update(zone_id, group_id, {"description": description})

    def add_member(
        self, zone_id: str, group_id: str, ap_mac: str
    ) -> Optional[Dict[str, Any]]:
        """Move an AP into this group, switching what it broadcasts.

        The AP must already be in ``zone_id``: its current zone is checked first
        and, if it is elsewhere, the move is refused before any write. Zone
        placement is a separate operation (``access_points.move``).

        Raises:
            SmartZoneZoneMismatchError: If the AP is not in ``zone_id``.
        """
        mac = normalize_mac(ap_mac)
        self.client.access_points._verify_zone([mac], zone_id)
        return self.client.post(f"{_members_path(zone_id, group_id)}/{mac}")

    def remove_member(
        self, zone_id: str, group_id: str, ap_mac: str
    ) -> Optional[Dict[str, Any]]:
        """Remove an AP from this group by MAC."""
        mac = normalize_mac(ap_mac)
        return self.client.delete(f"{_members_path(zone_id, group_id)}/{mac}")

    def set_radio_wlan_group(
        self, zone_id: str, group_id: str, radio: str, wlan_group_id: str
    ) -> Optional[Dict[str, Any]]:
        """Point one of the group's radios at a WLAN group (PATCH).

        Args:
            zone_id: Owning zone id.
            group_id: AP-group id.
            radio: One of ``radio24g``, ``radio5g``, ``radio5gLower``,
                ``radio5gUpper``, ``radio6g``.
            wlan_group_id: WLAN-group id the radio should broadcast.

        Raises:
            ValueError: If ``radio`` is not a known radio.
        """
        _validate_radio(radio)
        body = {"radioConfig": {radio: {"wlanGroupId": wlan_group_id}}}
        return self.client.patch(f"{_path(zone_id)}/{group_id}", json=body)

    def clear_radio_wlan_group(
        self, zone_id: str, group_id: str, radio: str
    ) -> Optional[Dict[str, Any]]:
        """Clear a radio's ``wlanGroupId`` override.

        Args:
            zone_id: Owning zone id.
            group_id: AP-group id.
            radio: One of ``radio24g``, ``radio5g``, ``radio5gLower``,
                ``radio5gUpper``, ``radio6g``.

        Raises:
            ValueError: If ``radio`` is not a known radio.
        """
        _validate_radio(radio)
        path = f"{_path(zone_id)}/{group_id}/radioConfig/{radio}/wlanGroupId"
        return self.client.delete(path)
