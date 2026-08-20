"""Ruckus SmartZone API Python client library."""

__version__ = "0.1.0"

from ruckus_smartzone.exceptions import (
    SmartZoneAPIError,
    SmartZoneAuthenticationError,
    SmartZoneConnectionError,
    SmartZoneNotFoundError,
    SmartZonePermissionError,
    SmartZoneValidationError,
)
from ruckus_smartzone.logging_config import set_log_level

__all__ = [
    "SmartZoneAPIError",
    "SmartZoneAuthenticationError",
    "SmartZonePermissionError",
    "SmartZoneNotFoundError",
    "SmartZoneValidationError",
    "SmartZoneConnectionError",
    "set_log_level",
]
