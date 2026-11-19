"""Shared helpers for Switch Manager resource wrappers.

Wrappers are dict-first: they build paths and query bodies, call the
:class:`~ruckus_smartzone.switchm.manager.SwitchManager` verbs, and return the
parsed JSON bodies unchanged. Write bodies are built from the caller's fields
and checked against the generated request schema, so a GET body is never sent
back as a write.
"""

from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Mapping, Optional, Union

from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from ruckus_smartzone.generated.models import SWITCHM_SCHEMA_INDEX
from ruckus_smartzone.mac import normalize_mac

if TYPE_CHECKING:
    from ruckus_smartzone.switchm.manager import SwitchManager

# Flexible-authentication types the controller accepts. The spec has no enum;
# the controller is case-sensitive and turns any other value into a null
# ("AuthenticationType cannot be empty").
AUTHENTICATION_TYPES = ("802.1x", "macauth", "802.1x_and_macauth")


def _prune_none(value: Any) -> Any:
    """Return ``value`` with ``None`` entries removed from nested dicts."""
    if isinstance(value, dict):
        return {k: _prune_none(v) for k, v in value.items() if v is not None}
    return value


def build_body(definition: str, fields: Mapping[str, Any]) -> Dict[str, Any]:
    """Return a write body holding only the caller's non-``None`` fields.

    ``None`` inside nested objects is removed too; the controller rejects it.

    Args:
        definition: Request-body definition name in the Switch Manager spec,
            e.g. ``portSettings_UpdatePortSettings``.
        fields: Body fields, keyed by their API (camelCase) names.

    Raises:
        ValueError: If a field is not a property of ``definition``. A GET body
            fails this check: it carries read-only keys such as ``id`` or
            ``createdTime`` that no write schema accepts.
    """
    allowed = SWITCHM_SCHEMA_INDEX[definition].get("properties") or {}
    unknown = sorted(key for key in fields if key not in allowed)
    if unknown:
        raise ValueError(f"{definition} has no field(s) {unknown}")
    return {
        key: _prune_none(value) for key, value in fields.items() if value is not None
    }


def merge_body(
    definition: str,
    current: Mapping[str, Any],
    fields: Mapping[str, Any],
    *,
    drop: Iterable[str] = (),
    unset: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Return a full write body: the current object with the caller's changes.

    For full-replace PUTs, where a field left out of the body is reset. The
    current object (a GET body) is cut down to the properties of
    ``definition``; its ``None`` values (nested ones too, which the controller
    rejects), the ``drop`` keys, and any key whose value equals its ``unset``
    marker (a GET reporting "not set" as ``0``, ``""`` or ``[]``) are removed;
    the caller's non-``None`` fields are applied on top.

    Raises:
        ValueError: If a caller field is not a property of ``definition``.
    """
    changes = build_body(definition, fields)
    allowed = SWITCHM_SCHEMA_INDEX[definition].get("properties") or {}
    skipped = set(drop)
    markers = unset or {}
    body = {
        key: _prune_none(value)
        for key, value in current.items()
        if key in allowed
        and key not in skipped
        and value is not None
        and not (key in markers and value == markers[key])
    }
    body.update(changes)
    return body


def check_authentication_type(fields: Mapping[str, Any]) -> None:
    """Refuse an ``authenticationType`` the controller does not accept.

    Raises:
        ValueError: If ``fields`` sets ``authenticationType`` to a value outside
            :data:`AUTHENTICATION_TYPES`.
    """
    value = fields.get("authenticationType")
    if value is not None and value not in AUTHENTICATION_TYPES:
        raise ValueError(
            f"authenticationType must be one of {AUTHENTICATION_TYPES}, got {value!r}"
        )


def switch_filter(filter_type: str, value: str) -> Dict[str, Any]:
    """Return a query body with one ``filters`` entry."""
    return {"filters": [{"type": filter_type, "value": value}]}


def switch_extra_filter(switch_id: str) -> Dict[str, Any]:
    """Return a query body filtering on one switch through ``extraFilters``.

    Port details, config backups and jobs take the switch as an
    ``extraFilters`` entry of type ``SWITCH``; their ``filters`` enum has no
    switch type.
    """
    return {"extraFilters": [{"type": "SWITCH", "value": switch_id}]}


def join_macs(switch_ids: Union[str, Iterable[str]]) -> str:
    """Return switch MACs as the comma-separated string the controller takes."""
    ids = [switch_ids] if isinstance(switch_ids, str) else list(switch_ids)
    if not ids:
        raise ValueError("at least one switch id is required")
    return ",".join(normalize_mac(mac) for mac in ids)


def single(items: List[Dict[str, Any]], *, kind: str, label: str) -> Dict[str, Any]:
    """Return the only item of ``items``.

    Raises:
        SmartZoneNotFoundError: If ``items`` is empty.
        ValueError: If ``items`` holds more than one item.
    """
    if not items:
        raise SmartZoneNotFoundError(f"No {kind} found with {label}")
    if len(items) > 1:
        raise ValueError(f"Multiple {kind}s found with {label}")
    return items[0]


class SwitchmResource:
    """Base for Switch Manager resource wrappers, holding the owning manager."""

    def __init__(self, switchm: "SwitchManager") -> None:
        """Initialize the resource.

        Args:
            switchm: The owning :class:`SwitchManager`.
        """
        self.switchm = switchm

    def merge_put(
        self,
        path: str,
        definition: str,
        fields: Mapping[str, Any],
        *,
        drop: Iterable[str] = (),
        unset: Optional[Mapping[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Change some fields of the object at ``path``, keeping the rest.

        Switch Manager has no PATCH for config objects, and its PUTs reset any
        field the body leaves out. This GETs the object, builds the full body
        with :func:`merge_body` and PUTs it to the same path. The controller
        diffs against its own database, so re-sent unchanged values generate
        no switch CLI.

        Raises:
            ValueError: If a field is not a property of ``definition``; raised
                before any request.
        """
        build_body(definition, fields)
        current = self.switchm.get(path) or {}
        body = merge_body(definition, current, fields, drop=drop, unset=unset)
        return self.switchm.put(path, json=body)
