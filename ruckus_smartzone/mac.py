"""MAC address validation and canonical formatting helpers.

SmartZone identifies APs by MAC in colon-separated uppercase form
(``8C:0C:90:2B:8B:90``). :func:`normalize_mac` accepts the common written forms
and returns that canonical form, raising on anything that is not an EUI-48 MAC.
"""

from __future__ import annotations

import re

# Twelve hex digits, optionally grouped by ':' or '-' in pairs or by '.' in
# fours. Grouping must be consistent throughout.
_BARE = re.compile(r"^[0-9A-Fa-f]{12}$")
_PAIRS = re.compile(r"^([0-9A-Fa-f]{2})([:-])(?:[0-9A-Fa-f]{2}\2){4}[0-9A-Fa-f]{2}$")
_QUADS = re.compile(r"^[0-9A-Fa-f]{4}(?:\.[0-9A-Fa-f]{4}){2}$")


def normalize_mac(mac: str) -> str:
    """Validate a MAC and return SmartZone's canonical ``8C:0C:...`` form.

    Args:
        mac: A MAC in bare (``8C0C902B8B90``), colon, hyphen, or dotted-quad
            (``8c0c.902b.8b90``) form.

    Returns:
        The MAC as colon-separated uppercase pairs.

    Raises:
        ValueError: If ``mac`` is not a string or is not a valid EUI-48 MAC.
    """
    if not isinstance(mac, str):
        raise ValueError(
            f"Invalid MAC address {mac!r}: expected a string, "
            f"got {type(mac).__name__}."
        )
    candidate = mac.strip()
    if not (
        _BARE.match(candidate) or _PAIRS.match(candidate) or _QUADS.match(candidate)
    ):
        raise ValueError(
            f"Invalid MAC address {mac!r}. "
            "Use a valid EUI-48 MAC (for example: '8C:0C:90:2B:8B:90', "
            "'8C-0C-90-2B-8B-90', '8c0c.902b.8b90', or '8C0C902B8B90')."
        )
    digits = re.sub(r"[:.\-]", "", candidate).upper()
    return ":".join(digits[i : i + 2] for i in range(0, 12, 2))
