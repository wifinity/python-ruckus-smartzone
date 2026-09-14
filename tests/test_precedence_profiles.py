"""Tests for the precedence profile resource wrapper."""

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


def test_list_tolerates_extra_top_level_keys(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    # The controller's /precedence response carries an extra top-level key beyond the
    # standard paged shape; pagination keys off list/hasMore/totalCount and ignores it.
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/precedence").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "firstIndex": 0,
                "extra": {"something": "vendor-specific"},
                "list": [
                    {
                        "id": "00000000-0000-0000-0000-0000000000d1",
                        "name": "System Default",
                    },
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        profiles = client.precedence_profiles.list()

    assert [p["name"] for p in profiles] == ["System Default"]


def test_get_returns_one_profile(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{BASE}/precedence/pr1").mock(
        return_value=httpx.Response(200, json={"id": "pr1", "name": "System Default"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        profile = client.precedence_profiles.get("pr1")

    assert profile == {"id": "pr1", "name": "System Default"}
    assert route.called


def test_find_by_name_returns_exact_match(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/precedence").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "pr1", "name": "System Default"},
                    {"id": "pr2", "name": "Custom"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        profile = client.precedence_profiles.find_by_name("System Default")

    assert profile["id"] == "pr1"


def test_find_by_name_raises_when_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/precedence").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "pr2", "name": "Custom"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.precedence_profiles.find_by_name("System Default")


def test_find_by_name_raises_on_duplicate(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/precedence").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "pr1", "name": "System Default"},
                    {"id": "pr2", "name": "System Default"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.precedence_profiles.find_by_name("System Default")
