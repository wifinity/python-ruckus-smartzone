"""Port settings resource wrapper (``/portSettings``).

Port settings are per switch port, keyed by a controller id; ``port`` holds
the ``unit/module/port`` identifier (``1/1/10``). VLAN membership is written as
strings (``untaggedVlans``, ``taggedVlans``).

``PUT /portSettings/{id}`` is a full replace: a field left out of the body is
reset (an omitted ``portEnabled`` disables the port, an omitted ``poeEnabled``
turns PoE off).
"""

from typing import Any, Dict, Iterable, List, Mapping, Optional

from ruckus_smartzone.const import DEFAULT_PAGE_SIZE
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import (
    SwitchmResource,
    build_body,
    check_authentication_type,
    merge_body,
    single,
    switch_filter,
)

# Firmware-gated object that a PUT refuses on firmware without PPPoE IA
# support, even when it is sent back unchanged.
_FIRMWARE_GATED = ("pppoeIa",)


class PortSettingsResource(SwitchmResource):
    """Operations on switch port settings."""

    def query(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> List[Dict[str, Any]]:
        """Return port settings matching ``criteria``, every page."""
        return self.switchm.query("portSettings/query", criteria, page_size=page_size)

    def list_switch(self, switch_id: str) -> List[Dict[str, Any]]:
        """Return the port settings of every port on a switch."""
        return self.query(switch_filter("switchId", normalize_mac(switch_id)))

    def get(self, port_settings_id: str) -> Optional[Dict[str, Any]]:
        """Return one port's settings by id."""
        return self.switchm.get(f"portSettings/{port_settings_id}")

    def find(self, switch_id: str, port: str) -> Dict[str, Any]:
        """Return the settings of one port, by switch and ``1/1/10`` identifier.

        Raises:
            SmartZoneNotFoundError: If the switch has no such port.
            ValueError: If the port is listed more than once.
        """
        matches = [p for p in self.list_switch(switch_id) if p.get("port") == port]
        return single(matches, kind="port", label=f"identifier {port!r}")

    def update(
        self, port_settings_id: str, fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Change some of one port's settings, keeping the rest.

        Reads the port, keeps its ``portSettings_UpdatePortSettings`` fields
        (dropping nulls, which the controller rejects, and ``pppoeIa`` unless
        ``fields`` sets it), applies ``fields`` and PUTs the full body, since
        the PUT resets any field it does not carry. Flexible authentication on
        a port needs switch-level authentication first
        (:class:`~ruckus_smartzone.switchm.authentication.SwitchAuthenticationResource`).
        One port write can start more than one deployment transaction.

        Raises:
            ValueError: On an unknown field or an unaccepted
                ``authenticationType``.
        """
        check_authentication_type(fields)
        current = self.get(port_settings_id) or {}
        body = merge_body(
            "portSettings_UpdatePortSettings",
            current,
            fields,
            drop=[key for key in _FIRMWARE_GATED if key not in fields],
        )
        return self.switchm.put(f"portSettings/{port_settings_id}", json=body)

    def bulk_update(
        self, port_settings_ids: Iterable[str], fields: Mapping[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Apply the same ``portSettings_createBulk`` fields to several ports.

        The body is sent as given, with no merge. Not verified against a
        controller: treat it as the same full replace as a single-port PUT and
        pass every setting the ports should keep.

        Raises:
            ValueError: On no ids, an unknown field or an unaccepted
                ``authenticationType``.
        """
        ids = list(port_settings_ids)
        if not ids:
            raise ValueError("at least one port settings id is required")
        check_authentication_type(fields)
        body = build_body("portSettings_createBulk", fields)
        body["idList"] = ids
        return self.switchm.post("portSettings/bulk", json=body)
