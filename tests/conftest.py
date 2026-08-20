"""Pytest configuration and fixtures."""

import pytest
import respx


@pytest.fixture
def base_url() -> str:
    """Base URL for the SmartZone public API."""
    return "https://smartzone.example:8443/wsg/api/public/v13_1"


@pytest.fixture
def service_ticket() -> str:
    """Sample SmartZone service ticket."""
    return "test-service-ticket-12345"


@pytest.fixture
def mocked_api(respx_mock: respx.MockRouter) -> respx.MockRouter:
    """Router for mocking HTTP API calls; no test performs real network I/O."""
    return respx_mock
