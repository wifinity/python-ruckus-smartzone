"""Switch resource wrapper (``/switch``).

A switch's id is its MAC address in colon-separated uppercase form.
"""

from typing import Any, Dict, Iterable, List, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import (
    SwitchmResource,
    single,
    switch_extra_filter,
    switch_filter,
)


class SwitchesResource(SwitchmResource):
    """Operations on switches managed by the controller."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return switches matching ``criteria`` (``POST /switch``), every page."""
        return self.switchm.query("switch", criteria, page_size=page_size)

    def list_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Return the switches in one switch group."""
        return self.query(switch_filter("SWITCH_GROUP", group_id))

    def get(self, switch_id: str) -> Optional[Dict[str, Any]]:
        """Return one switch by id (its MAC)."""
        return self.switchm.get(f"switch/{normalize_mac(switch_id)}")

    def find_by_serial(self, serial_number: str) -> Dict[str, Any]:
        """Return the switch whose ``serialNumber`` matches exactly.

        The controller's ``POST /switch`` has no serial filter, so this runs a
        full-text search and keeps exact matches. ``registrationStatus`` tells
        an unapproved (``PENDING``) switch from an approved one.

        Raises:
            SmartZoneNotFoundError: If no switch has that serial number.
            ValueError: If more than one switch has that serial number.
        """
        found = self.query({"fullTextSearch": {"type": "AND", "value": serial_number}})
        matches = [s for s in found if s.get("serialNumber") == serial_number]
        return single(matches, kind="switch", label=f"serial {serial_number!r}")

    def move(
        self, group_id: str, switch_ids: Iterable[str]
    ) -> Optional[Dict[str, Any]]:
        """Move switches into a switch group (``PUT /switch/move/{groupId}``).

        Moving an unapproved switch out of the domain's staging group approves
        it. If the group has a provision CLI template for the switch's model,
        it runs on the switch's first approval: it replaces the startup config
        and reloads the switch.
        """
        ids = [normalize_mac(mac) for mac in switch_ids]
        if not ids:
            raise ValueError("at least one switch id is required")
        return self.switchm.put(f"switch/move/{group_id}", json=ids)

    def delete(self, switch_id: str) -> Optional[Dict[str, Any]]:
        """Delete a switch from the controller.

        Deleting an online switch sends it a manager-disable event: it stops
        talking to the controller until its manager is re-enabled on the switch
        or it is factory-reset. All controller-side state for the switch
        (backups, authentication, port settings) is dropped.
        """
        return self.switchm.delete(f"switch/{normalize_mac(switch_id)}")

    def port_details(self, switch_id: str) -> List[Dict[str, Any]]:
        """Return the live port details of a switch, including LLDP neighbours.

        Each entry carries ``portIdentifier`` (``1/1/10``), ``status``,
        ``neighborName``, ``connectedDevice``, ``vlans`` and the matching
        ``portSettingId``.
        """
        return self.switchm.query(
            "switch/ports/details", switch_extra_filter(normalize_mac(switch_id))
        )
