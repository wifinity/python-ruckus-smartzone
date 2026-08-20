"""Tests for service-ticket acquisition, reuse, refresh and release."""

import httpx
import pytest
import respx

from ruckus_smartzone import InMemoryTicketCache, SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneAuthenticationError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def register_login(
    respx_mock: respx.MockRouter,
    ticket: str,
    version: str = "7.1.1.0.551",
) -> respx.Route:
    return respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(
            200, json={"serviceTicket": ticket, "controllerVersion": version}
        )
    )


def register_logout(respx_mock: respx.MockRouter) -> respx.Route:
    return respx_mock.delete(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(204)
    )


def register_aps(respx_mock: respx.MockRouter) -> respx.Route:
    return respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(200, json={"list": []})
    )


def test_acquires_ticket_on_first_call(
    respx_mock: respx.MockRouter, controller_url: str, service_ticket: str
) -> None:
    login = register_login(respx_mock, service_ticket)
    aps = register_aps(respx_mock)
    register_logout(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.get("aps")
        assert client.controller_version == "7.1.1.0.551"

    assert login.call_count == 1
    assert aps.calls.last.request.url.params["serviceTicket"] == service_ticket


def test_reuses_ticket_across_calls(
    respx_mock: respx.MockRouter, controller_url: str, service_ticket: str
) -> None:
    login = register_login(respx_mock, service_ticket)
    register_aps(respx_mock)
    register_logout(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.get("aps")
        client.get("aps")
        client.get("aps")

    assert login.call_count == 1


def test_refreshes_ticket_on_401(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    login = respx_mock.post(f"{BASE}/serviceTicket").mock(
        side_effect=[
            httpx.Response(200, json={"serviceTicket": "ticket-1"}),
            httpx.Response(200, json={"serviceTicket": "ticket-2"}),
        ]
    )
    register_logout(respx_mock)
    aps = respx_mock.get(f"{BASE}/aps").mock(
        side_effect=[
            httpx.Response(401, json={}),
            httpx.Response(200, json={"list": [{"mac": "AA"}]}),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.get("aps")

    assert result == {"list": [{"mac": "AA"}]}
    assert login.call_count == 2
    assert aps.call_count == 2
    assert aps.calls.last.request.url.params["serviceTicket"] == "ticket-2"


def test_releases_ticket_on_close(
    respx_mock: respx.MockRouter, controller_url: str, service_ticket: str
) -> None:
    register_login(respx_mock, service_ticket)
    logout = register_logout(respx_mock)
    register_aps(respx_mock)

    client = SmartZoneClient(controller_url, "admin", "pw")
    client.get("aps")
    client.close()

    assert logout.call_count == 1
    assert logout.calls.last.request.url.params["serviceTicket"] == service_ticket


def test_close_without_ticket_does_not_logoff(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    client = SmartZoneClient(controller_url, "admin", "pw")
    client.close()

    assert not respx_mock.calls


def test_context_manager_releases_ticket(
    respx_mock: respx.MockRouter, controller_url: str, service_ticket: str
) -> None:
    register_login(respx_mock, service_ticket)
    logout = register_logout(respx_mock)
    register_aps(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.get("aps")

    assert logout.call_count == 1


def test_logon_failure_raises_authentication_error(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(401, json={})
    )
    client = SmartZoneClient(controller_url, "admin", "pw")

    with pytest.raises(SmartZoneAuthenticationError):
        client.get("aps")


def test_logon_without_ticket_raises(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"controllerVersion": "7.1.1.0.551"})
    )
    client = SmartZoneClient(controller_url, "admin", "pw")

    with pytest.raises(SmartZoneAuthenticationError):
        client.get("aps")


def test_custom_ticket_cache_is_used(
    respx_mock: respx.MockRouter, controller_url: str, service_ticket: str
) -> None:
    register_login(respx_mock, service_ticket)
    register_logout(respx_mock)
    register_aps(respx_mock)
    cache = InMemoryTicketCache()

    with SmartZoneClient(controller_url, "admin", "pw", ticket_cache=cache) as client:
        client.get("aps")
        assert cache.get() == service_ticket


def test_in_memory_ticket_cache_roundtrip() -> None:
    cache = InMemoryTicketCache()
    assert cache.get() is None
    cache.set("ticket")
    assert cache.get() == "ticket"
    cache.clear()
    assert cache.get() is None
