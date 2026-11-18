"""Ruckus SmartZone API Python client library."""

__version__ = "1.3.0"

from ruckus_smartzone.client import SmartZoneClient
from ruckus_smartzone.exceptions import (
    SmartZoneAPIError,
    SmartZoneAuthenticationError,
    SmartZoneBusinessRuleError,
    SmartZoneBusyError,
    SmartZoneConnectionError,
    SmartZoneDeploymentError,
    SmartZoneDeploymentTimeoutError,
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
    APGroupsResource,
    DPSKResource,
    FirewallProfilesResource,
    MoveBatchResult,
    MoveResult,
    PrecedenceProfilesResource,
    WLANGroupsResource,
    WLANsResource,
    ZonesResource,
)
from ruckus_smartzone.switchm import AUTHENTICATION_TYPES, SwitchManager
from ruckus_smartzone.ticket_cache import InMemoryTicketCache, TicketCache

__all__ = [
    "SmartZoneClient",
    "ZonesResource",
    "WLANsResource",
    "WLANGroupsResource",
    "AccessPointsResource",
    "APGroupsResource",
    "FirewallProfilesResource",
    "PrecedenceProfilesResource",
    "DPSKResource",
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
    "SmartZoneBusinessRuleError",
    "SmartZoneDeploymentError",
    "SmartZoneDeploymentTimeoutError",
    "SwitchManager",
    "AUTHENTICATION_TYPES",
    "TicketCache",
    "InMemoryTicketCache",
    "set_log_level",
]
