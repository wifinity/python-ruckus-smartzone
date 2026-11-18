"""Tests for error-response mapping, including Switch Manager envelopes."""

import pytest

from ruckus_smartzone.exceptions import (
    SmartZoneAPIError,
    SmartZoneBusinessRuleError,
    SmartZoneDeploymentError,
    SmartZoneDeploymentTimeoutError,
    SmartZoneNotFoundError,
    SmartZoneValidationError,
    raise_for_response,
)

MSG_KEY = (
    "server.switch.portSettings.cannot.enable.flexible.auth.without."
    "switch.authentication"
)


def test_msg_key_500_is_business_rule_error() -> None:
    body = {
        "success": False,
        "error": {"message": "Enable switch auth first", "msgKey": MSG_KEY},
    }

    with pytest.raises(SmartZoneBusinessRuleError) as excinfo:
        raise_for_response(500, body)

    assert excinfo.value.msg_key == MSG_KEY
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Enable switch auth first"
    assert excinfo.value.response_data == body


def test_msg_key_without_message_uses_key() -> None:
    with pytest.raises(SmartZoneBusinessRuleError) as excinfo:
        raise_for_response(500, {"error": {"msgKey": "server.x", "msgValues": [1]}})

    assert excinfo.value.message == "server.x"
    assert excinfo.value.msg_values == [1]


def test_422_envelope_message_is_unescaped() -> None:
    body = {
        "success": False,
        "error": {"message": " [&quot;filters/type&quot;] bad", "msgKey": None},
    }

    with pytest.raises(SmartZoneValidationError) as excinfo:
        raise_for_response(422, body)

    assert excinfo.value.message == '["filters/type"] bad'


def test_plain_500_stays_generic() -> None:
    with pytest.raises(SmartZoneAPIError) as excinfo:
        raise_for_response(500, {"message": "boom"})

    assert type(excinfo.value) is SmartZoneAPIError
    assert excinfo.value.status_code == 500


def test_404_with_error_code_211_is_not_found() -> None:
    with pytest.raises(SmartZoneNotFoundError):
        raise_for_response(404, {"message": "Permission denied.", "errorCode": 211})


def test_deployment_error_flags_local_config_conflict() -> None:
    err = SmartZoneDeploymentError(
        "failed",
        switch_message="Failed to apply configuration due to an ongoing local "
        "configuration change on the switch",
    )

    assert err.local_config_conflict
    assert not SmartZoneDeploymentError("failed").local_config_conflict


def test_timeout_is_a_deployment_error() -> None:
    assert issubclass(SmartZoneDeploymentTimeoutError, SmartZoneDeploymentError)
    assert SmartZoneDeploymentTimeoutError("t").transactions == []
