"""WLAN group resource wrapper.

A WLAN group is a named bundle of WLANs that APs point their radios at. On
``v13_1`` the group object itself is only ``{name, description}`` and has no PUT;
its WLAN membership lives in a separate ``/members`` sub-resource. A rename
therefore reaches only ``name`` and cannot disturb membership.

This wraps ``/rkszones/{zoneId}/wlangroups`` and its ``/members`` collection.
Members are addressed by the WLAN's id.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from ruckus_smartzone.resources.base import BaseResource, find_one_by_name
from ruckus_smartzone.validation import validate_group_name


def _path(zone_id: str) -> str:
    return f"rkszones/{zone_id}/wlangroups"


def _members_path(zone_id: str, group_id: str) -> str:
    return f"{_path(zone_id)}/{group_id}/members"


class WLANGroupsResource(BaseResource):
    """Operations on WLAN groups and their members within a zone."""

    def list(self, zone_id: str, **params: Any) -> List[Dict[str, Any]]:
        """Return every WLAN group in a zone, following pagination."""
        return self.client.paginate(_path(zone_id), params=params or None)

    def get(self, zone_id: str, group_id: str) -> Optional[Dict[str, Any]]:
        """Return one WLAN group by id, including its ``members``."""
        return self.client.get(f"{_path(zone_id)}/{group_id}")

    def find_by_name(self, zone_id: str, name: str) -> Dict[str, Any]:
        """Return the single WLAN group whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no group has that name.
            ValueError: If more than one group has that name.
        """
        return find_one_by_name(self.list(zone_id), name, kind="WLAN group")

    def create(
        self, zone_id: str, name: str, description: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a WLAN group; returns ``{id, ...}``.

        The name is validated locally against the controller's constraints.
        """
        validate_group_name(name)
        body: Dict[str, Any] = {"name": name}
        if description is not None:
            body["description"] = description
        return self.client.post(_path(zone_id), json=body)

    def update(
        self,
        zone_id: str,
        group_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Modify a WLAN group's ``name`` and/or ``description`` (PATCH).

        The body carries only the fields given, so membership is never touched.

        Raises:
            ValueError: If neither ``name`` nor ``description`` is given.
        """
        body: Dict[str, Any] = {}
        if name is not None:
            validate_group_name(name)
            body["name"] = name
        if description is not None:
            body["description"] = description
        if not body:
            raise ValueError("Provide at least one of 'name' or 'description'")
        return self.client.patch(f"{_path(zone_id)}/{group_id}", json=body)

    def rename(
        self, zone_id: str, group_id: str, name: str
    ) -> Optional[Dict[str, Any]]:
        """Rename a WLAN group, leaving its membership untouched."""
        return self.update(zone_id, group_id, name=name)

    def delete(self, zone_id: str, group_id: str) -> Optional[Dict[str, Any]]:
        """Delete a WLAN group by id."""
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
            return self.create(zone_id, name, description)
        group_id = existing["id"]
        if description is None:
            return existing
        return self.update(zone_id, group_id, description=description)

    def list_members(self, zone_id: str, group_id: str) -> List[Dict[str, Any]]:
        """Return the group's WLAN members, read from its detail body."""
        detail = self.get(zone_id, group_id) or {}
        members = detail.get("members")
        return members if isinstance(members, list) else []

    def add_member(
        self, zone_id: str, group_id: str, wlan_id: str, **fields: Any
    ) -> Optional[Dict[str, Any]]:
        """Add a WLAN to the group.

        Args:
            zone_id: Owning zone id.
            group_id: WLAN-group id.
            wlan_id: Id of the WLAN to add (the member's ``id``).
            **fields: Optional member fields such as ``accessVlan``, ``nasId``,
                ``vlanPooling``.
        """
        body: Dict[str, Any] = {"id": wlan_id, **fields}
        return self.client.post(_members_path(zone_id, group_id), json=body)

    def modify_member(
        self,
        zone_id: str,
        group_id: str,
        member_id: str,
        changes: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Apply a partial modification to a member (PATCH)."""
        path = f"{_members_path(zone_id, group_id)}/{member_id}"
        return self.client.patch(path, json=changes)

    def replace_member(
        self,
        zone_id: str,
        group_id: str,
        member_id: str,
        member: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Replace a member's settings wholesale (PUT)."""
        path = f"{_members_path(zone_id, group_id)}/{member_id}"
        return self.client.put(path, json=member)

    def remove_member(
        self, zone_id: str, group_id: str, member_id: str
    ) -> Optional[Dict[str, Any]]:
        """Remove a WLAN from the group by member id."""
        path = f"{_members_path(zone_id, group_id)}/{member_id}"
        return self.client.delete(path)
