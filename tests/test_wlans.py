"""Tests for the zone WLAN resource wrapper."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
WLANS = f"{BASE}/rkszones/z1/wlans"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def test_list_returns_all_wlans(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(WLANS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "w1", "name": "Guest"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        wlans = client.wlans.list("z1")

    assert [w["name"] for w in wlans] == ["Guest"]


def test_get_returns_one_wlan(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{WLANS}/w1").mock(
        return_value=httpx.Response(200, json={"id": "w1", "name": "Guest"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        wlan = client.wlans.get("z1", "w1")

    assert wlan == {"id": "w1", "name": "Guest"}


def test_create_posts_body(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.post(WLANS).mock(
        return_value=httpx.Response(201, json={"id": "w9"})
    )
    payload = {"name": "Guest", "ssid": "guest-ssid"}

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        created = client.wlans.create("z1", payload)

    assert created == {"id": "w9"}
    assert route.calls.last.request.method == "POST"
    assert json.loads(route.calls.last.request.content) == payload


def test_update_patches(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{WLANS}/w1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlans.update("z1", "w1", {"name": "Guest2"})

    assert route.calls.last.request.method == "PATCH"


def test_replace_puts(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.put(f"{WLANS}/w1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlans.replace("z1", "w1", {"name": "Guest"})

    assert route.calls.last.request.method == "PUT"


def test_delete_deletes(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{WLANS}/w1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlans.delete("z1", "w1")

    assert route.calls.last.request.method == "DELETE"


def test_find_by_name_found(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    respx_mock.get(WLANS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "w1", "name": "Guest"},
                    {"id": "w2", "name": "Staff"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        wlan = client.wlans.find_by_name("z1", "Staff")

    assert wlan["id"] == "w2"


def test_find_by_name_not_found(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(WLANS).mock(
        return_value=httpx.Response(
            200,
            json={"totalCount": 0, "hasMore": False, "list": []},
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.wlans.find_by_name("z1", "Nope")
