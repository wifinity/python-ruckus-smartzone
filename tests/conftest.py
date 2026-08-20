"""Pytest configuration and fixtures."""

from typing import List

import pytest
import respx


@pytest.fixture
def base_url() -> str:
    """Base URL for the SmartZone public API."""
    return "https://smartzone.example:8443/wsg/api/public/v13_1"


@pytest.fixture
def controller_url() -> str:
    """Controller root URL, as a caller would pass to the client."""
    return "https://smartzone.example:8443"


@pytest.fixture
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> List[float]:
    """Capture backoff sleeps instead of blocking; returns the waited seconds."""
    waits: List[float] = []
    monkeypatch.setattr(
        "ruckus_smartzone.client.time.sleep", lambda seconds: waits.append(seconds)
    )
    return waits


@pytest.fixture
def service_ticket() -> str:
    """Sample SmartZone service ticket."""
    return "test-service-ticket-12345"


@pytest.fixture
def mocked_api(respx_mock: respx.MockRouter) -> respx.MockRouter:
    """Router for mocking HTTP API calls; no test performs real network I/O."""
    return respx_mock
