"""Firewall profile resource wrapper.

Firewall profiles are global to the controller (not zone-scoped). This wraps the
``/firewallProfiles`` collection: list, detail, and a lookup-by-name helper for
callers that reference a firewall profile by name and need its id (the WLAN body's
``firewallProfileId`` is a plain id string with no name form).
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.resources.base import BaseResource, find_one_by_name

_PATH = "firewallProfiles"


class FirewallProfilesResource(BaseResource):
    """Operations on SmartZone firewall profiles (``/firewallProfiles``)."""

    def list(self, **params: Any) -> List[Dict[str, Any]]:
        """Return every firewall profile, following pagination."""
        return self.client.paginate(_PATH, params=params or None)

    def get(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Return one firewall profile by id."""
        return self.client.get(f"{_PATH}/{profile_id}")

    def find_by_name(self, name: str) -> Dict[str, Any]:
        """Return the single firewall profile whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no firewall profile has that name.
            ValueError: If more than one firewall profile has that name.
        """
        return find_one_by_name(self.list(), name, kind="firewall profile")
