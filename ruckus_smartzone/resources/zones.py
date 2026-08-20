"""Zone resource wrapper.

A zone is a site on the controller, named from the site code. This wraps the
``/rkszones`` collection: list, detail, create, modify, replace, delete, and a
lookup-by-name helper for workflows that resolve a zone from its site code.
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.resources.base import BaseResource, find_one_by_name

_PATH = "rkszones"


class ZonesResource(BaseResource):
    """Operations on SmartZone zones (``/rkszones``)."""

    def list(self, **params: Any) -> List[Dict[str, Any]]:
        """Return every zone, following pagination."""
        return self.client.paginate(_PATH, params=params or None)

    def get(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """Return one zone by id."""
        return self.client.get(f"{_PATH}/{zone_id}")

    def create(self, zone: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a zone from a full request body; returns ``{id, ...}``."""
        return self.client.post(_PATH, json=zone)

    def update(self, zone_id: str, changes: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply a partial modification to a zone (PATCH)."""
        return self.client.patch(f"{_PATH}/{zone_id}", json=changes)

    def replace(self, zone_id: str, zone: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Replace a zone's configuration wholesale (PUT)."""
        return self.client.put(f"{_PATH}/{zone_id}", json=zone)

    def delete(self, zone_id: str) -> Optional[Dict[str, Any]]:
        """Delete a zone by id."""
        return self.client.delete(f"{_PATH}/{zone_id}")

    def find_by_name(self, name: str) -> Dict[str, Any]:
        """Return the single zone whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no zone has that name.
            ValueError: If more than one zone has that name.
        """
        return find_one_by_name(self.list(), name, kind="zone")
