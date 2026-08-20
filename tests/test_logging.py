"""Tests for logging configuration and credential masking."""

import logging

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneAPIError
from ruckus_smartzone.logging_config import (
    mask_sensitive_headers,
    mask_url,
    set_log_level,
)

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def test_set_log_level_accepts_str_and_int() -> None:
    set_log_level("DEBUG")
    assert logging.getLogger("ruckus_smartzone").level == logging.DEBUG
    set_log_level(logging.INFO)
    assert logging.getLogger("ruckus_smartzone").level == logging.INFO


def test_mask_sensitive_headers() -> None:
    headers = {
        "Authorization": "Bearer secret-token",
        "Cookie": "JSESSIONID=abc123",
        "Content-Type": "application/json",
    }
    masked = mask_sensitive_headers(headers)
    assert masked["Authorization"] == "Bearer ***"
    assert masked["Cookie"] == "***"
    assert masked["Content-Type"] == "application/json"


def test_mask_url_redacts_service_ticket() -> None:
    masked = mask_url(f"{BASE}/aps?serviceTicket=SECRET-TICKET&index=0&listSize=100")
    assert "SECRET-TICKET" not in masked
    assert "serviceTicket=%2A%2A%2A" in masked or "serviceTicket=***" in masked
    assert "index=0" in masked
    assert "listSize=100" in masked


def test_mask_url_is_case_insensitive() -> None:
    masked = mask_url(f"{BASE}/aps?ServiceTicket=SECRET-TICKET")
    assert "SECRET-TICKET" not in masked


def test_mask_url_without_query_is_unchanged() -> None:
    url = f"{BASE}/aps"
    assert mask_url(url) == url


def test_service_ticket_never_reaches_logs(
    respx_mock: respx.MockRouter,
    controller_url: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    secret = "top-secret-ticket-value"
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": secret})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))
    respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(200, json={"list": []})
    )

    caplog.set_level(logging.DEBUG, logger="ruckus_smartzone")
    with SmartZoneClient(controller_url, "admin", "pw", log_level="DEBUG") as client:
        client.get("aps")

    messages = "\n".join(record.getMessage() for record in caplog.records)
    assert secret not in messages
    # The request was logged (masked), proving the guarantee is not vacuous.
    assert any("/aps" in record.getMessage() for record in caplog.records)


def test_service_ticket_never_reaches_exception_message(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    secret = "top-secret-ticket-value"
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": secret})
    )
    respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(500, json={"cause": "boom"})
    )

    client = SmartZoneClient(controller_url, "admin", "pw")
    with pytest.raises(SmartZoneAPIError) as excinfo:
        client.get("aps")

    assert secret not in str(excinfo.value)
    assert secret not in (excinfo.value.message or "")
