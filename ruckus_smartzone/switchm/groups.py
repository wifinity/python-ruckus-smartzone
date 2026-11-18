"""Switch group resource wrapper (``/group``).

A switch group belongs to a domain. Moving a switch into a group approves it
(see :meth:`~ruckus_smartzone.switchm.switches.SwitchesResource.move`).
"""

from typing import Any, Dict, List, Mapping, Optional

from ruckus_smartzone.switchm.base import SwitchmResource, build_body, single


class SwitchGroupsResource(SwitchmResource):
    """Operations on switch groups."""

    def list(
        self, domain_id: str, *, show_staging_group: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Return the switch groups of a domain as ``{id, label, type}`` entries.

        The domain's default (staging) group, where unapproved switches land,
        is listed with the others.
        """
        params = None
        if show_staging_group is not None:
            params = {"showStagingGroup": str(show_staging_group).lower()}
        body = self.switchm.get(f"group/ids/byDomain/{domain_id}", params=params) or {}
        data = body.get("data") or {}
        items: List[Dict[str, Any]] = data.get("list") or []
        return items

    def get(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Return one switch group by id."""
        return self.switchm.get(f"group/{group_id}")

    def find_by_name(self, domain_id: str, name: str) -> Dict[str, Any]:
        """Return the group of a domain whose name matches exactly, in full.

        Raises:
            SmartZoneNotFoundError: If no group has that name.
            ValueError: If more than one group has that name.
        """
        matches = [g for g in self.list(domain_id) if g.get("label") == name]
        entry = single(matches, kind="switch group", label=f"name {name!r}")
        return self.get(entry["id"]) or {}

    def create(self, fields: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a switch group (``POST /group``).

        ``fields`` takes ``group_switchGroup`` keys, at least ``name`` and
        ``domainId``. The controller returns no id; look the group up with
        :meth:`find_by_name`.
        """
        return self.switchm.post("group", json=build_body("group_switchGroup", fields))

    def update(
        self, group_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Change a group's name or description (PATCH)."""
        return self.switchm.patch(
            f"group/{group_id}", json=build_body("group_switchGroup", fields)
        )

    def delete(self, group_id: str) -> Optional[Dict[str, Any]]:
        """Delete a switch group."""
        return self.switchm.delete(f"group/{group_id}")
