"""Smoke tests for the package scaffold."""

import ruckus_smartzone
from ruckus_smartzone import (
    SmartZoneAPIError,
    SmartZoneAuthenticationError,
    SmartZoneNotFoundError,
    SmartZonePermissionError,
    SmartZoneValidationError,
)


def test_version() -> None:
    assert ruckus_smartzone.__version__ == "0.1.0"


def test_exports_are_callable() -> None:
    assert callable(ruckus_smartzone.set_log_level)


def test_exception_hierarchy() -> None:
    for exc in (
        SmartZoneAuthenticationError,
        SmartZonePermissionError,
        SmartZoneNotFoundError,
        SmartZoneValidationError,
    ):
        assert issubclass(exc, SmartZoneAPIError)


def test_exception_status_codes() -> None:
    assert SmartZoneAuthenticationError().status_code == 401
    assert SmartZonePermissionError().status_code == 403
    assert SmartZoneNotFoundError().status_code == 404
    assert SmartZoneValidationError().status_code == 422
