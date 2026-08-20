"""Pluggable storage for the SmartZone service ticket.

The client holds one long-lived service ticket and reuses it across calls. The
storage sits behind :class:`TicketCache` so a shared/Redis-backed store can be
supplied later without touching the client. Only the in-memory implementation
ships here.
"""

import abc
from typing import Optional


class TicketCache(abc.ABC):
    """Storage seam for a single SmartZone service ticket."""

    @abc.abstractmethod
    def get(self) -> Optional[str]:
        """Return the stored ticket, or ``None`` if none is held."""

    @abc.abstractmethod
    def set(self, ticket: str) -> None:
        """Store ``ticket`` as the current ticket."""

    @abc.abstractmethod
    def clear(self) -> None:
        """Drop any stored ticket."""


class InMemoryTicketCache(TicketCache):
    """Holds the ticket in a single process-local attribute."""

    def __init__(self) -> None:
        self._ticket: Optional[str] = None

    def get(self) -> Optional[str]:
        return self._ticket

    def set(self, ticket: str) -> None:
        self._ticket = ticket

    def clear(self) -> None:
        self._ticket = None
