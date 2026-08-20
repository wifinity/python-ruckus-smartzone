"""Service-ticket acquisition, reuse and release for SmartZone.

SmartZone issues a service ticket on logon that is valid for 24 hours and is
meant to be reused across calls. :class:`ServiceTicketManager` holds one ticket
behind a :class:`~ruckus_smartzone.ticket_cache.TicketCache`, acquires it lazily,
invalidates it so the next call re-acquires (used after a 401), and releases it
on logoff.
"""

from typing import Any, Dict, Optional

import httpx

from ruckus_smartzone.const import SERVICE_TICKET_PARAM
from ruckus_smartzone.exceptions import (
    SmartZoneAuthenticationError,
    raise_for_response,
)
from ruckus_smartzone.logging_config import get_logger
from ruckus_smartzone.ticket_cache import TicketCache

logger = get_logger("ruckus_smartzone.auth")

# Logon and logoff endpoints, relative to the versioned base URL.
_SERVICE_TICKET_PATH = "serviceTicket"


def _json_or_none(response: httpx.Response) -> Optional[Dict[str, Any]]:
    """Return a parsed JSON object body, or ``None`` if there is none."""
    if not response.content:
        return None
    try:
        data = response.json()
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


class ServiceTicketManager:
    """Owns the lifecycle of a single SmartZone service ticket."""

    def __init__(
        self,
        http: httpx.Client,
        username: str,
        password: str,
        cache: TicketCache,
    ) -> None:
        """Initialize the manager.

        Args:
            http: Client whose base URL is the versioned public API root; the
                logon/logoff calls are issued through it.
            username: Controller admin username.
            password: Controller admin password.
            cache: Storage for the held ticket.
        """
        self._http = http
        self._username = username
        self._password = password
        self._cache = cache
        self.controller_version: Optional[str] = None

    def get_ticket(self) -> str:
        """Return the held ticket, acquiring one if none is held."""
        ticket = self._cache.get()
        if ticket is not None:
            return ticket
        return self._acquire()

    def invalidate(self) -> None:
        """Drop the held ticket so the next call acquires a fresh one."""
        self._cache.clear()

    def release(self) -> None:
        """Log off, releasing the ticket on the controller. Best-effort."""
        ticket = self._cache.get()
        if ticket is None:
            return
        logger.debug("Releasing SmartZone service ticket")
        try:
            self._http.request(
                "DELETE",
                _SERVICE_TICKET_PATH,
                params={SERVICE_TICKET_PARAM: ticket},
            )
        except httpx.HTTPError as exc:
            logger.warning("Failed to release service ticket: %s", exc)
        finally:
            self._cache.clear()

    def _acquire(self) -> str:
        """Log on and cache a new ticket."""
        logger.debug("Acquiring SmartZone service ticket")
        try:
            response = self._http.post(
                _SERVICE_TICKET_PATH,
                json={"username": self._username, "password": self._password},
            )
        except httpx.RequestError as exc:
            raise SmartZoneAuthenticationError(
                f"Could not reach the controller to log on: {exc}"
            ) from exc

        if response.status_code != 200:
            # The error body carries no ticket, so it is safe to attach.
            raise_for_response(response.status_code, _json_or_none(response))

        data = _json_or_none(response) or {}
        ticket = data.get("serviceTicket")
        if not isinstance(ticket, str) or not ticket:
            # Never attach the body here: on success it holds the ticket.
            raise SmartZoneAuthenticationError(
                "Logon response did not contain a service ticket"
            )

        self.controller_version = data.get("controllerVersion")
        self._cache.set(ticket)
        logger.debug(
            "Acquired service ticket (controller version %s)",
            self.controller_version,
        )
        return ticket
