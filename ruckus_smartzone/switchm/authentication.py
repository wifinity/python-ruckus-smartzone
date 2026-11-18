"""Switch-level authentication and flexible-authentication profile wrappers.

Port-level flexible authentication (802.1X, MAC auth) is refused until the
switch has authentication enabled with an auth-default VLAN
(``PUT /authentication/{switchId}``).
"""

from typing import Any, Dict, List, Mapping, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import (
    SwitchmResource,
    build_body,
    check_authentication_type,
)


class SwitchAuthenticationResource(SwitchmResource):
    """Switch-level authentication (``/authentication/{switchId}``)."""

    def get(self, switch_id: str) -> Optional[Dict[str, Any]]:
        """Return a switch's authentication settings."""
        return self.switchm.get(f"authentication/{normalize_mac(switch_id)}")

    def update(
        self,
        switch_id: str,
        *,
        enabled: bool,
        default_vlan: Optional[int] = None,
        guest_vlan: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """Set a switch's authentication settings.

        Enabling it pushes ``authentication``, ``auth-default-vlan`` and
        ``aaa authentication dot1x default radius`` to the switch. The default
        VLAN does not have to exist first.
        """
        body = build_body(
            "authentication_UpdateAuthentication",
            {
                "authEnable": enabled,
                "authDefaultVlan": default_vlan,
                "guestVlan": guest_vlan,
            },
        )
        return self.switchm.put(f"authentication/{normalize_mac(switch_id)}", json=body)


class FlexAuthProfilesResource(SwitchmResource):
    """Flexible-authentication profiles (``/flexibleAuthenticationProfile``)."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return profiles matching ``criteria``, every page."""
        return self.switchm.query(
            "flexibleAuthenticationProfile/query", criteria, page_size=page_size
        )

    def list_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Return a switch group's profiles."""
        return self.switchm.get_pages(f"flexibleAuthenticationProfile/query/{group_id}")

    def get(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Return one profile."""
        return self.switchm.get(f"flexibleAuthenticationProfile/{profile_id}")

    def create(self, fields: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a profile from ``..._CreateFlexibleAuthenticationProfile`` fields.

        Raises:
            ValueError: On an unknown field or an unaccepted
                ``authenticationType``.
        """
        check_authentication_type(fields)
        return self.switchm.post(
            "flexibleAuthenticationProfile",
            json=build_body(
                "flexibleAuthenticationProfile_CreateFlexibleAuthenticationProfile",
                fields,
            ),
        )

    def update(
        self, profile_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a profile from ``..._UpdateFlexibleAuthenticationProfile`` fields.

        Raises:
            ValueError: On an unknown field or an unaccepted
                ``authenticationType``.
        """
        check_authentication_type(fields)
        return self.switchm.put(
            f"flexibleAuthenticationProfile/{profile_id}",
            json=build_body(
                "flexibleAuthenticationProfile_UpdateFlexibleAuthenticationProfile",
                fields,
            ),
        )

    def delete(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Delete a profile."""
        return self.switchm.delete(f"flexibleAuthenticationProfile/{profile_id}")
