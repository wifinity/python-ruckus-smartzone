"""Tests for transport resilience: rate-limit, busy retry and error mapping."""

from typing import List

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.client import DEFAULT_RATE_LIMIT_WAIT
from ruckus_smartzone.exceptions import (
    SmartZoneAPIError,
    SmartZoneAuthenticationError,
    SmartZoneBusyError,
    SmartZoneConnectionError,
    SmartZoneNotFoundError,
    SmartZonePermissionError,
    SmartZoneRateLimitError,
    SmartZoneValidationError,
)

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def register_session(respx_mock: respx.MockRouter, ticket: str = "t-1") -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": ticket})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def test_retries_on_rate_limit_then_succeeds(
    respx_mock: respx.MockRouter, controller_url: str, no_sleep: List[float]
) -> None:
    register_session(respx_mock)
    aps = respx_mock.get(f"{BASE}/aps").mock(
        side_effect=[
            httpx.Response(429, headers={"RateLimit-Reset": "2"}),
            httpx.Response(200, json={"list": []}),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        assert client.get("aps") == {"list": []}

    assert aps.call_count == 2
    assert no_sleep == [3]


def test_rate_limit_without_header_uses_default_wait(
    respx_mock: respx.MockRouter, controller_url: str, no_sleep: List[float]
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/aps").mock(
        side_effect=[
            httpx.Response(429),
            httpx.Response(200, json={"list": []}),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.get("aps")

    assert no_sleep == [DEFAULT_RATE_LIMIT_WAIT]


def test_rate_limit_exhausted_raises(
    respx_mock: respx.MockRouter, controller_url: str, no_sleep: List[float]
) -> None:
    register_session(respx_mock)
    aps = respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(429, headers={"RateLimit-Reset": "1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw", max_retries=2) as client:
        with pytest.raises(SmartZoneRateLimitError) as excinfo:
            client.get("aps")

    assert excinfo.value.retry_after == 2
    assert aps.call_count == 3  # initial attempt plus two retries
    assert len(no_sleep) == 2


def test_retries_on_busy_then_succeeds(
    respx_mock: respx.MockRouter, controller_url: str, no_sleep: List[float]
) -> None:
    register_session(respx_mock)
    aps = respx_mock.get(f"{BASE}/aps").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(200, json={"list": []}),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        assert client.get("aps") == {"list": []}

    assert aps.call_count == 2
    assert no_sleep == [1.0]


def test_busy_exhausted_raises(
    respx_mock: respx.MockRouter, controller_url: str, no_sleep: List[float]
) -> None:
    register_session(respx_mock)
    aps = respx_mock.get(f"{BASE}/aps").mock(return_value=httpx.Response(503))

    with SmartZoneClient(controller_url, "admin", "pw", max_retries=2) as client:
        with pytest.raises(SmartZoneBusyError) as excinfo:
            client.get("aps")

    assert excinfo.value.status_code == 503
    assert aps.call_count == 3


@pytest.mark.parametrize(
    "status,body,expected",
    [
        (403, {"errorCode": 211}, SmartZoneNotFoundError),
        (403, {}, SmartZonePermissionError),
        (404, {}, SmartZoneNotFoundError),
        (422, {}, SmartZoneValidationError),
        (500, {}, SmartZoneAPIError),
    ],
)
def test_error_status_mapping(
    respx_mock: respx.MockRouter,
    controller_url: str,
    status: int,
    body: dict,
    expected: type,
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/aps").mock(return_value=httpx.Response(status, json=body))

    client = SmartZoneClient(controller_url, "admin", "pw")
    with pytest.raises(expected):
        client.get("aps")


def test_persistent_401_raises_after_single_refresh(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    login = respx_mock.post(f"{BASE}/serviceTicket").mock(
        side_effect=[
            httpx.Response(200, json={"serviceTicket": "t-1"}),
            httpx.Response(200, json={"serviceTicket": "t-2"}),
        ]
    )
    aps = respx_mock.get(f"{BASE}/aps").mock(return_value=httpx.Response(401, json={}))

    client = SmartZoneClient(controller_url, "admin", "pw")
    with pytest.raises(SmartZoneAuthenticationError):
        client.get("aps")

    assert login.call_count == 2  # initial plus one refresh
    assert aps.call_count == 2


def test_connection_error_wrapped(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/aps").mock(
        side_effect=httpx.ConnectError("connection refused")
    )

    client = SmartZoneClient(controller_url, "admin", "pw")
    with pytest.raises(SmartZoneConnectionError):
        client.get("aps")
