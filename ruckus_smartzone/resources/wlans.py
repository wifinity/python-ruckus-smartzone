"""Zone WLAN resource wrapper.

WLANs are the Wi-Fi networks defined inside a zone. This wraps the
``/rkszones/{zoneId}/wlans`` collection. Creation bodies vary by WLAN type
(open, 802.1X, hotspot, …), so create/replace stay dict-first pass-throughs.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.resources.base import BaseResource, find_one_by_name


def _path(zone_id: str) -> str:
    return f"rkszones/{zone_id}/wlans"


class WLANsResource(BaseResource):
    """Operations on the WLANs within a zone."""

    def list(self, zone_id: str, **params: Any) -> List[Dict[str, Any]]:
        """Return every WLAN in a zone, following pagination."""
        return self.client.paginate(_path(zone_id), params=params or None)

    def get(self, zone_id: str, wlan_id: str) -> Optional[Dict[str, Any]]:
        """Return one WLAN by id."""
        return self.client.get(f"{_path(zone_id)}/{wlan_id}")

    def create(self, zone_id: str, wlan: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a WLAN from a full request body; returns ``{id, ...}``."""
        return self.client.post(_path(zone_id), json=wlan)

    def update(
        self, zone_id: str, wlan_id: str, changes: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply a partial modification to a WLAN (PATCH)."""
        return self.client.patch(f"{_path(zone_id)}/{wlan_id}", json=changes)

    def replace(
        self, zone_id: str, wlan_id: str, wlan: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Replace a WLAN's configuration wholesale (PUT)."""
        return self.client.put(f"{_path(zone_id)}/{wlan_id}", json=wlan)

    def delete(self, zone_id: str, wlan_id: str) -> Optional[Dict[str, Any]]:
        """Delete a WLAN by id."""
        return self.client.delete(f"{_path(zone_id)}/{wlan_id}")

    def find_by_name(self, zone_id: str, name: str) -> Dict[str, Any]:
        """Return the single WLAN in a zone whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no WLAN has that name.
            ValueError: If more than one WLAN has that name.
        """
        return find_one_by_name(self.list(zone_id), name, kind="WLAN")
