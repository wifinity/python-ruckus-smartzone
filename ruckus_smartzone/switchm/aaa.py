"""Switch group AAA server and AAA settings wrappers (``/group/{id}/aaa*``)."""

from typing import Any, Dict, Iterable, List, Mapping, Optional

from ruckus_smartzone.switchm.base import SwitchmResource, build_body


class AAAServersResource(SwitchmResource):
    """Operations on a switch group's AAA (RADIUS/TACACS+) servers and settings."""

    def list(self, group_id: str) -> List[Dict[str, Any]]:
        """Return a group's AAA servers."""
        return self.switchm.get_pages(f"group/{group_id}/aaaServers")

    def get(self, group_id: str, server_id: str) -> Optional[Dict[str, Any]]:
        """Return one AAA server."""
        return self.switchm.get(f"group/{group_id}/aaaServers/{server_id}")

    def create(
        self, group_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create an AAA server from ``aaaServers_createAdminAAAServer`` fields."""
        return self.switchm.post(
            f"group/{group_id}/aaaServers",
            json=build_body("aaaServers_createAdminAAAServer", fields),
        )

    def update(
        self, group_id: str, server_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Modify an AAA server from ``aaaServers_createAdminAAAServer`` fields.

        Reads the object and PUTs it back in full with ``fields`` applied
        (see :meth:`SwitchmResource.merge_put`), so pass only what changes.
        """
        return self.merge_put(
            f"group/{group_id}/aaaServers/{server_id}",
            "aaaServers_createAdminAAAServer",
            fields,
        )

    def delete(self, group_id: str, server_id: str) -> Optional[Dict[str, Any]]:
        """Delete one AAA server."""
        return self.switchm.delete(f"group/{group_id}/aaaServers/{server_id}")

    def delete_many(
        self, group_id: str, server_ids: Iterable[str]
    ) -> Optional[Dict[str, Any]]:
        """Delete AAA servers by id; an empty list makes no request."""
        ids = list(server_ids)
        if not ids:
            return None
        return self.switchm.delete(f"group/{group_id}/aaaServers", json={"idList": ids})

    def get_settings(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Return a group's AAA settings (authentication/authorization/accounting)."""
        return self.switchm.get(f"group/{group_id}/aaaSettings")

    def update_settings(
        self, group_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Modify a group's AAA settings from ``aaaSettings_AAASetting`` fields.

        Reads the object and PUTs it back in full with ``fields`` applied
        (see :meth:`SwitchmResource.merge_put`), so pass only what changes.
        """
        return self.merge_put(
            f"group/{group_id}/aaaSettings", "aaaSettings_AAASetting", fields
        )
