"""Precedence profile resource wrapper.

Precedence profiles are global to the controller (not zone-scoped). This wraps the
``/precedence`` collection: list, detail, and a lookup-by-name helper for callers
that reference a precedence profile by name and need its id (the WLAN body's
``precedenceProfileId`` is a plain id string with no name form).
"""

from typing import Any, Dict, List, Optional

from ruckus_smartzone.resources.base import BaseResource, find_one_by_name

_PATH = "precedence"


class PrecedenceProfilesResource(BaseResource):
    """Operations on SmartZone precedence profiles (``/precedence``)."""

    def list(self, **params: Any) -> List[Dict[str, Any]]:
        """Return every precedence profile, following pagination."""
        return self.client.paginate(_PATH, params=params or None)

    def get(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Return one precedence profile by id."""
        return self.client.get(f"{_PATH}/{profile_id}")

    def find_by_name(self, name: str) -> Dict[str, Any]:
        """Return the single precedence profile whose name matches exactly.

        Raises:
            SmartZoneNotFoundError: If no precedence profile has that name.
            ValueError: If more than one precedence profile has that name.
        """
        return find_one_by_name(self.list(), name, kind="precedence profile")
