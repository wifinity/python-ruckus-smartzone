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
    assert ruckus_smartzone.__version__ == "1.3.0"


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


def test_switchm_exports() -> None:
    from ruckus_smartzone import (
        AUTHENTICATION_TYPES,
        SmartZoneBusinessRuleError,
        SmartZoneDeploymentError,
        SmartZoneDeploymentTimeoutError,
        SwitchManager,
    )

    assert AUTHENTICATION_TYPES == ("802.1x", "macauth", "802.1x_and_macauth")
    for exc in (
        SmartZoneBusinessRuleError,
        SmartZoneDeploymentError,
        SmartZoneDeploymentTimeoutError,
    ):
        assert issubclass(exc, SmartZoneAPIError)
    assert callable(SwitchManager)
