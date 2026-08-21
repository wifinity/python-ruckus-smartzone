"""Client-side validation for SmartZone request fields.

The controller enforces these constraints too, but validating before the call
turns a raw 422 into a clear, local error and avoids a round trip.
"""

import re

from ruckus_smartzone.exceptions import SmartZoneValidationError

# common_normalName from the v13_1 spec: 2-32 printable characters, with no
# leading or trailing space. Used for zone, WLAN-group and AP-group names.
NORMAL_NAME_MIN_LENGTH = 2
NORMAL_NAME_MAX_LENGTH = 32
NORMAL_NAME_PATTERN = re.compile(r"^[!-~]([ -~]){0,30}[!-~]$")


def validate_group_name(name: str) -> str:
    """Return ``name`` if it satisfies the group-name constraints.

    Args:
        name: Proposed group name (WLAN group or AP group).

    Raises:
        SmartZoneValidationError: If the name is not a string of 2-32 printable
            characters without a leading or trailing space.
    """
    if not isinstance(name, str):
        raise SmartZoneValidationError(
            f"group name must be a string, got {type(name).__name__}"
        )
    if not NORMAL_NAME_PATTERN.match(name):
        raise SmartZoneValidationError(
            f"group name {name!r} is invalid: it must be "
            f"{NORMAL_NAME_MIN_LENGTH}-{NORMAL_NAME_MAX_LENGTH} printable "
            "characters with no leading or trailing space"
        )
    return name
