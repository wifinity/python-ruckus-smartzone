"""Tests for the zone resource wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def test_list_returns_all_zones(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/rkszones").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "firstIndex": 0,
                "list": [
                    {"id": "z1", "name": "SITE-A"},
                    {"id": "z2", "name": "SITE-B"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        zones = client.zones.list()

    assert [z["name"] for z in zones] == ["SITE-A", "SITE-B"]


def test_get_returns_one_zone(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{BASE}/rkszones/z1").mock(
        return_value=httpx.Response(200, json={"id": "z1", "name": "SITE-A"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        zone = client.zones.get("z1")

    assert zone == {"id": "z1", "name": "SITE-A"}
    assert route.called


def test_create_posts_body_and_returns_id(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/rkszones").mock(
        return_value=httpx.Response(201, json={"id": "z9"})
    )
    payload = {
        "name": "SITE-Z",
        "login": {"apLoginName": "admin", "apLoginPassword": "secret"},
    }

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        created = client.zones.create(payload)

    assert created == {"id": "z9"}
    import json

    assert json.loads(route.calls.last.request.content) == payload


def test_update_patches(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{BASE}/rkszones/z1").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zones.update("z1", {"description": "renamed"})

    assert route.calls.last.request.method == "PATCH"


def test_replace_puts(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.put(f"{BASE}/rkszones/z1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zones.replace("z1", {"name": "SITE-A"})

    assert route.calls.last.request.method == "PUT"


def test_delete_deletes(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{BASE}/rkszones/z1").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zones.delete("z1")

    assert route.calls.last.request.method == "DELETE"


def test_find_by_name_returns_exact_match(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/rkszones").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "z1", "name": "SITE-A"},
                    {"id": "z2", "name": "SITE-B"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        zone = client.zones.find_by_name("SITE-B")

    assert zone["id"] == "z2"


def test_find_by_name_raises_when_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/rkszones").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "z1", "name": "SITE-A"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.zones.find_by_name("SITE-X")


def test_find_by_name_raises_on_duplicate(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/rkszones").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "z1", "name": "SITE-A"},
                    {"id": "z2", "name": "SITE-A"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.zones.find_by_name("SITE-A")
