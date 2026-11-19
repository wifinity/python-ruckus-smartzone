"""VLAN resource wrapper (``/vlans``).

A VLAN config belongs to a switch group or to one switch.
"""

from typing import Any, Dict, Iterable, List, Mapping, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import SwitchmResource, build_body, switch_filter


class VLANsResource(SwitchmResource):
    """Operations on VLAN configs."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return VLAN configs matching ``criteria``, every page."""
        return self.switchm.query("vlans/query", criteria, page_size=page_size)

    def list_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Return the VLAN configs of a switch group."""
        return self.query(switch_filter("SWITCH_GROUP", group_id))

    def list_switch(self, switch_id: str) -> List[Dict[str, Any]]:
        """Return the VLAN configs of one switch."""
        return self.query(switch_filter("switchId", normalize_mac(switch_id)))

    def get(self, vlan_config_id: str) -> Optional[Dict[str, Any]]:
        """Return one VLAN config by id."""
        return self.switchm.get(f"vlans/{vlan_config_id}")

    def default_vlan(self, switch_id: str) -> Optional[Dict[str, Any]]:
        """Return a switch's default VLAN config."""
        return self.switchm.get(f"vlans/defaultvlan/{normalize_mac(switch_id)}")

    def create(self, fields: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a VLAN config from ``vlanConfig_createVlanConfig`` fields.

        Set ``groupId`` for a group VLAN or ``switchId`` for a switch VLAN,
        plus ``vlanId`` and ``name``. ``pushTimeType`` is required by the
        controller and defaults to ``NOW``.
        """
        body = build_body("vlanConfig_createVlanConfig", fields)
        body.setdefault("pushTimeType", "NOW")
        return self.switchm.post("vlans", json=body)

    def update(
        self, vlan_config_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a VLAN config from ``vlanConfig_updateVlanConfig`` fields.

        Reads the object and PUTs it back in full with ``fields`` applied
        (see :meth:`SwitchmResource.merge_put`), so pass only what changes.
        """
        return self.merge_put(
            f"vlans/{vlan_config_id}", "vlanConfig_updateVlanConfig", fields
        )

    def delete(self, vlan_config_id: str) -> Optional[Dict[str, Any]]:
        """Delete one VLAN config."""
        return self.switchm.delete(f"vlans/{vlan_config_id}")

    def delete_many(self, vlan_config_ids: Iterable[str]) -> Optional[Dict[str, Any]]:
        """Delete VLAN configs by id; an empty list makes no request."""
        ids = list(vlan_config_ids)
        if not ids:
            return None
        return self.switchm.delete("vlans", json={"idList": ids})
