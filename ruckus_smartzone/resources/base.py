"""Shared helpers for resource wrappers.

Resource wrappers are dict-first: they build paths, call the client's HTTP verbs
and :meth:`~ruckus_smartzone.client.SmartZoneClient.paginate`, and return the
parsed JSON bodies unchanged.
"""

from typing import TYPE_CHECKING, Any, Dict, List

from ruckus_smartzone.exceptions import SmartZoneNotFoundError

if TYPE_CHECKING:
    from ruckus_smartzone.client import SmartZoneClient


class BaseResource:
    """Base for resource wrappers, holding the owning client."""

    def __init__(self, client: "SmartZoneClient") -> None:
        """Initialize the resource.

        Args:
            client: The owning :class:`SmartZoneClient`.
        """
        self.client = client


def find_one_by_name(
    items: List[Dict[str, Any]], name: str, *, kind: str
) -> Dict[str, Any]:
    """Return the single item whose ``name`` matches exactly.

    Args:
        items: Candidate objects, each a dict that may carry a ``name``.
        name: Name to match exactly.
        kind: Object kind, used only in error messages (e.g. ``"zone"``).

    Raises:
        SmartZoneNotFoundError: If no item has the given name.
        ValueError: If more than one item has the given name.
    """
    matches = [item for item in items if item.get("name") == name]
    if not matches:
        raise SmartZoneNotFoundError(f"No {kind} found with name {name!r}")
    if len(matches) > 1:
        raise ValueError(f"Multiple {kind}s found with name {name!r}")
    return matches[0]
