"""Ruckus SmartZone API Python client library."""

__version__ = "0.1.0"

from ruckus_smartzone.client import SmartZoneClient
from ruckus_smartzone.exceptions import (
    SmartZoneAPIError,
    SmartZoneAuthenticationError,
    SmartZoneBusyError,
    SmartZoneConnectionError,
    SmartZoneNotFoundError,
    SmartZonePermissionError,
    SmartZoneRateLimitError,
    SmartZoneValidationError,
    SmartZoneZoneMismatchError,
)
from ruckus_smartzone.logging_config import set_log_level
from ruckus_smartzone.mac import normalize_mac
from ruckus_smartzone.resources import (
    AccessPointsResource,
    MoveBatchResult,
    MoveResult,
    WLANGroupsResource,
    WLANsResource,
    ZonesResource,
)
from ruckus_smartzone.ticket_cache import InMemoryTicketCache, TicketCache

__all__ = [
    "SmartZoneClient",
    "ZonesResource",
    "WLANsResource",
    "WLANGroupsResource",
    "AccessPointsResource",
    "MoveResult",
    "MoveBatchResult",
    "normalize_mac",
    "SmartZoneAPIError",
    "SmartZoneAuthenticationError",
    "SmartZonePermissionError",
    "SmartZoneNotFoundError",
    "SmartZoneValidationError",
    "SmartZoneZoneMismatchError",
    "SmartZoneConnectionError",
    "SmartZoneRateLimitError",
    "SmartZoneBusyError",
    "TicketCache",
    "InMemoryTicketCache",
    "set_log_level",
]
