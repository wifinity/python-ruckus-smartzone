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
from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.switchm.base import (
    SwitchmResource,
    build_body,
    check_authentication_type,
    single,
    switch_filter,
)

# Fields the bulk endpoint keeps unchanged when they are named in
# ``ignoreList``; any other name there makes it fail with a bare 500.
BULK_IGNORABLE = (
    "portName",
    "portProtected",
    "taggedVlans",
    "untaggedVlans",
    "broadcastLimitKbps",
    "multicastLimitKbps",
    "unknownUnicastLimitKbps",
    "poeEnabled",
    "poeClass",
    "poePriority",
    "poeBudget",
    "inAclConfigName",
    "outAclConfigName",
    "portSpeed",
    "rstpAdminEdgePortEnabled",
    "stpBpduGuardEnabled",
    "stpRootGuardEnabled",
    "portDhcpSnooping",
    "pppoeIa",
    "arpInspectionEnabled",
    "v6NdInspectionEnabled",
    "dhcpSnoopingTrustPortEnabled",
    "ipsgEnabled",
    "lldpEnabled",
    "dscpTrustEnabled",
    "voiceVlanId",
    "flexibleAuthenticationEnabled",
    "authenticationType",
    "changeAuthOrder",
    "dot1XPortControl",
    "authDefaultVlan",
    "authFailAction",
    "restrictedVlan",
    "authTimeoutAction",
    "criticalVlan",
)

# Fields the bulk endpoint always sets from the body.
_NOT_IGNORABLE = ("portEnabled", "isStormControlUnitKbps")

# Fields ``bulk_update`` accepts in ``fields``.
BULK_FIELDS = frozenset(BULK_IGNORABLE + _NOT_IGNORABLE)

# Values filling the bulk body for the fields the web UI always sends. The
# endpoint refuses a body without them, but an ignored field keeps its current
# value, so these are never applied unless ``fields`` leaves a
# non-ignorable field unset and the switch reports no value for it.
BULK_PLACEHOLDERS: Dict[str, Any] = {
    "portEnabled": True,
    "portProtected": False,
    "untaggedVlans": "1",
    "isStormControlUnitKbps": True,
    "poeEnabled": True,
    "poeClass": "0",
    "poePriority": 3,
    "portSpeed": "AUTO",
    "rstpAdminEdgePortEnabled": False,
    "stpBpduGuardEnabled": False,
    "stpRootGuardEnabled": False,
    "arpInspectionEnabled": False,
    "v6NdInspectionEnabled": False,
    "dhcpSnoopingTrustPortEnabled": False,
    "ipsgEnabled": False,
    "lldpEnabled": True,
    "dscpTrustEnabled": False,
    "flexibleAuthenticationEnabled": False,
    "authenticationType": "802.1x",
    "changeAuthOrder": False,
    "dot1XPortControl": "auto",
    "authFailAction": "block",
    "authTimeoutAction": "none",
    "portName": "x",
}

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
        return self.merge_put(
            f"portSettings/{port_settings_id}",
            "portSettings_UpdatePortSettings",
            fields,
            drop=[key for key in _FIRMWARE_GATED if key not in fields],
        )

    def bulk_update(
        self,
        switch_id: str,
        group_id: str,
        ports: Iterable[str],
        fields: Mapping[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Apply the same changes to several ports of one switch in one call.

        ``POST /portSettings/bulk`` sets every field not named in its
        ``ignoreList`` from the body, and refuses a body without a value for
        each field the web UI sends, even ignored ones. The body is therefore
        :data:`BULK_PLACEHOLDERS` overlaid with ``fields``, and ``ignoreList``
        is every :data:`BULK_IGNORABLE` field not in ``fields``, so only
        ``fields`` change. ``portEnabled`` and ``isStormControlUnitKbps``
        cannot be ignored: unless ``fields`` sets them, they are read from the
        switch's current port settings and must agree across ``ports``.

        Each call is one ``PORT_CONFIGURATION`` deployment; back-to-back calls
        succeed where a burst of per-port PUTs is refused with an ongoing local
        configuration change.

        Args:
            switch_id: Switch MAC.
            group_id: Switch group id.
            ports: Port identifiers (``1/1/10``), not port settings ids.
            fields: Only the settings that change, keyed by API name.

        Raises:
            ValueError: On no ports, an empty id, a field outside
                :data:`BULK_FIELDS`, an unaccepted ``authenticationType``, or
                ports that disagree on a non-ignorable field ``fields`` omits.
            SmartZoneNotFoundError: If the switch has no such port.
        """
        port_list = list(ports)
        if not port_list:
            raise ValueError("at least one port is required")
        if not switch_id or not group_id:
            raise ValueError("switch_id and group_id are required")
        unknown = sorted(key for key in fields if key not in BULK_FIELDS)
        if unknown:
            raise ValueError(f"portSettings bulk update has no field(s) {unknown}")
        check_authentication_type(fields)
        mac = normalize_mac(switch_id)

        body: Dict[str, Any] = dict(BULK_PLACEHOLDERS)
        missing = [key for key in _NOT_IGNORABLE if key not in fields]
        if missing:
            body.update(self._current_values(mac, port_list, missing))
        body.update(build_body("portSettings_createBulk", fields))
        body["idList"] = port_list
        body["ignoreList"] = [key for key in BULK_IGNORABLE if key not in fields]
        body["groupId"] = group_id
        body["switchId"] = mac
        return self.switchm.post("portSettings/bulk", json=body)

    def _current_values(
        self, switch_id: str, ports: List[str], keys: List[str]
    ) -> Dict[str, Any]:
        """Return the shared current value of ``keys`` across ``ports``."""
        by_port = {p.get("port"): p for p in self.list_switch(switch_id)}
        current = []
        for port in ports:
            if port not in by_port:
                raise SmartZoneNotFoundError(f"switch {switch_id} has no port {port!r}")
            current.append(by_port[port])
        values: Dict[str, Any] = {}
        for key in keys:
            seen = {settings.get(key) for settings in current} - {None}
            if len(seen) > 1:
                raise ValueError(
                    f"ports disagree on {key}; set it in fields to apply one value"
                )
            values[key] = seen.pop() if seen else BULK_PLACEHOLDERS[key]
        return values
