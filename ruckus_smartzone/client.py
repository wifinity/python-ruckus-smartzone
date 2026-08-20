"""Synchronous SmartZone client: transport, session lifecycle and resilience.

A single :class:`SmartZoneClient` owns an ``httpx.Client`` and a
:class:`~ruckus_smartzone.auth.ServiceTicketManager`. It attaches the service
ticket to every request as a URL query parameter, refreshes the ticket on a 401,
backs off on rate limiting and controller-busy responses, and pages list
endpoints. Resource wrappers layer on top of the low-level verbs and
:meth:`SmartZoneClient.paginate`.
"""

import logging
import time
from types import TracebackType
from typing import Any, Dict, Optional, Type

import httpx

from ruckus_smartzone.auth import ServiceTicketManager, _json_or_none
from ruckus_smartzone.const import (
    API_VERSION,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    PUBLIC_API_PATH,
    SERVICE_TICKET_PARAM,
)
from ruckus_smartzone.exceptions import (
    SmartZoneBusyError,
    SmartZoneConnectionError,
    SmartZoneRateLimitError,
    raise_for_response,
)
from ruckus_smartzone.logging_config import get_logger, mask_url, set_log_level
from ruckus_smartzone.ticket_cache import InMemoryTicketCache, TicketCache

logger = get_logger("ruckus_smartzone.client")

# HTTP statuses treated as a transient controller-busy/config-lock signal. The
# controller serialises configuration writes; the exact status is confirmed by
# live verification. 423 Locked and 503 Service Unavailable are retried.
BUSY_STATUS_CODES = frozenset({423, 503})

# Fallback wait (seconds) when a 429 carries no readable RateLimit-Reset header.
DEFAULT_RATE_LIMIT_WAIT = 1

# Exponential backoff bounds (seconds) for controller-busy retries.
BUSY_BACKOFF_BASE = 1.0
BUSY_BACKOFF_MAX = 60.0


def _normalize_base_url(base_url: str) -> str:
    """Return the versioned public API root, with a trailing slash.

    Accepts either a controller root (``https://host:8443``) or a URL that
    already carries the versioned path, and always yields
    ``https://host:8443/wsg/api/public/v13_1/`` so relative request paths merge
    correctly under ``httpx``.
    """
    trimmed = base_url.rstrip("/")
    suffix = f"{PUBLIC_API_PATH}/{API_VERSION}"
    if not trimmed.endswith(suffix):
        trimmed = f"{trimmed}{suffix}"
    return f"{trimmed}/"


def _rate_limit_reset(response: httpx.Response) -> int:
    """Seconds to wait for a 429, from ``RateLimit-Reset`` (plus a margin)."""
    raw = response.headers.get("RateLimit-Reset")
    try:
        return int(raw) + 1
    except (TypeError, ValueError):
        return DEFAULT_RATE_LIMIT_WAIT


class SmartZoneClient:
    """Client for the Ruckus SmartZone public API (``v13_1``)."""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        *,
        verify: bool = True,
        timeout: float = 30.0,
        ticket_cache: Optional[TicketCache] = None,
        max_retries: int = 3,
        log_level: Optional[Any] = None,
    ) -> None:
        """Initialize the client.

        Args:
            base_url: Controller URL, e.g. ``https://host:8443``; the versioned
                public API path is appended if absent.
            username: Controller admin username.
            password: Controller admin password.
            verify: TLS certificate verification; set ``False`` for a
                self-signed controller.
            timeout: Per-request timeout in seconds.
            ticket_cache: Storage for the service ticket; an in-memory cache is
                used when omitted.
            max_retries: Retry budget shared by rate-limit and busy backoff.
            log_level: When set, configures the ``ruckus_smartzone`` logger.
        """
        if log_level is not None:
            set_log_level(log_level)
        # The ticket travels in the URL; keep the HTTP libraries from logging it.
        logging.getLogger("httpx").disabled = True
        logging.getLogger("httpcore").disabled = True

        self._http = httpx.Client(
            base_url=_normalize_base_url(base_url),
            verify=verify,
            timeout=timeout,
        )
        self._max_retries = max_retries
        self._tickets = ServiceTicketManager(
            self._http,
            username,
            password,
            ticket_cache or InMemoryTicketCache(),
        )

    @property
    def controller_version(self) -> Optional[str]:
        """SmartZone controller version reported at logon, if known."""
        return self._tickets.controller_version

    def get(
        self, path: str, *, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Issue a GET and return the parsed JSON body."""
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a POST and return the parsed JSON body."""
        return self._request("POST", path, params=params, json=json)

    def put(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a PUT and return the parsed JSON body."""
        return self._request("PUT", path, params=params, json=json)

    def patch(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a PATCH and return the parsed JSON body."""
        return self._request("PATCH", path, params=params, json=json)

    def delete(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
    ) -> Optional[Dict[str, Any]]:
        """Issue a DELETE and return the parsed JSON body."""
        return self._request("DELETE", path, params=params, json=json)

    def paginate(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> list:
        """Fetch every item of a paged list endpoint.

        Walks ``index``/``listSize`` over the ``{totalCount, hasMore,
        firstIndex, list}`` response shape and returns the concatenated
        ``list`` entries in order.

        Args:
            path: List endpoint path.
            params: Extra query parameters applied to every page.
            page_size: Items per page; clamped to the API maximum (1000).
        """
        page_size = min(page_size, MAX_PAGE_SIZE)
        results: list = []
        fetched = 0
        offset = 0
        while True:
            page_params = dict(params or {})
            page_params["listSize"] = page_size
            page_params["index"] = offset
            page = self.get(path, params=page_params) or {}

            items = page.get("list") or []
            results.extend(items)
            fetched += len(items)

            if not items:
                break
            total = page.get("totalCount")
            has_more = page.get("hasMore")
            if has_more is False:
                break
            if has_more is None:
                if total is not None and fetched >= total:
                    break
                if len(items) < page_size:
                    break
            offset += page_size

        return results

    def session_info(self) -> Optional[Dict[str, Any]]:
        """Return the controller's interactive admin sessions.

        Backed by ``GET /sessionManagement``, which reports GUI/admin logins; an
        API service-ticket session is not listed here. To check whether a ticket
        is still valid, make a request with it and observe the status.
        """
        return self.get("sessionManagement")

    def close(self) -> None:
        """Release the service ticket and close the underlying connection."""
        try:
            self._tickets.release()
        finally:
            self._http.close()

    def __enter__(self) -> "SmartZoneClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        _auth_retry: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Send one request with ticket injection, refresh and backoff."""
        request_params = dict(params or {})
        request_params[SERVICE_TICKET_PARAM] = self._tickets.get_ticket()

        attempts = 0
        while True:
            try:
                response = self._http.request(
                    method, path, params=request_params, json=json
                )
            except httpx.RequestError as exc:
                raise SmartZoneConnectionError(
                    f"Request to {method} {path} failed: {exc}",
                    original_error=exc,
                ) from exc

            status = response.status_code
            logger.debug("%s %s -> %s", method, mask_url(response.request.url), status)

            if status == 429:
                wait = _rate_limit_reset(response)
                if attempts < self._max_retries:
                    attempts += 1
                    logger.debug(
                        "Rate limited; waiting %ss (attempt %s)", wait, attempts
                    )
                    time.sleep(wait)
                    continue
                raise SmartZoneRateLimitError(
                    f"Rate limit not cleared after {attempts} retries",
                    response_data=_json_or_none(response),
                    retry_after=wait,
                )

            if status in BUSY_STATUS_CODES:
                if attempts < self._max_retries:
                    attempts += 1
                    delay = min(
                        BUSY_BACKOFF_BASE * (2 ** (attempts - 1)),
                        BUSY_BACKOFF_MAX,
                    )
                    logger.debug(
                        "Controller busy (%s); retrying in %ss (attempt %s)",
                        status,
                        delay,
                        attempts,
                    )
                    time.sleep(delay)
                    continue
                raise SmartZoneBusyError(
                    f"Controller still busy after {attempts} retries",
                    status_code=status,
                    response_data=_json_or_none(response),
                )

            if status == 401 and _auth_retry:
                logger.debug("Ticket rejected (401); refreshing and retrying")
                self._tickets.invalidate()
                request_params[SERVICE_TICKET_PARAM] = self._tickets.get_ticket()
                _auth_retry = False
                continue

            return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Optional[Dict[str, Any]]:
        """Return the JSON body, or raise the mapped error on a 4xx/5xx."""
        if response.status_code >= 400:
            raise_for_response(response.status_code, _json_or_none(response))
        return _json_or_none(response)
