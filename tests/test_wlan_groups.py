"""Tests for the WLAN group resource wrapper and its members collection."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneValidationError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
GROUPS = f"{BASE}/rkszones/z1/wlangroups"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def test_create_posts_name_and_description(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        created = client.wlan_groups.create("z1", "Commissioning", description="temp")

    assert created == {"id": "g1"}
    assert json.loads(route.calls.last.request.content) == {
        "name": "Commissioning",
        "description": "temp",
    }


def test_create_omits_description_when_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.create("z1", "All Areas - Wireless")

    assert json.loads(route.calls.last.request.content) == {
        "name": "All Areas - Wireless"
    }


def test_rename_patches_name_only_and_never_touches_members(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.rename("z1", "g1", "All Areas - Wireless")

    body = json.loads(route.calls.last.request.content)
    assert body == {"name": "All Areas - Wireless"}
    assert "members" not in body


def test_update_requires_a_field(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.wlan_groups.update("z1", "g1")


def test_list_returns_all_groups(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "g1", "name": "Commissioning"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        groups = client.wlan_groups.list("z1")

    assert [g["name"] for g in groups] == ["Commissioning"]


def test_get_returns_detail_with_members(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{GROUPS}/g1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "g1",
                "name": "Commissioning",
                "members": [{"id": "w1"}, {"id": "w2"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        detail = client.wlan_groups.get("z1", "g1")

    assert [m["id"] for m in detail["members"]] == ["w1", "w2"]


def test_delete_deletes(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.delete("z1", "g1")

    assert route.calls.last.request.method == "DELETE"


def test_list_members_reads_group_detail(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{GROUPS}/g1").mock(
        return_value=httpx.Response(
            200,
            json={"id": "g1", "members": [{"id": "w1"}, {"id": "w2"}]},
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        members = client.wlan_groups.list_members("z1", "g1")

    assert [m["id"] for m in members] == ["w1", "w2"]


def test_add_member_posts_wlan_id(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{GROUPS}/g1/members").mock(
        return_value=httpx.Response(201, json={"id": "w1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.add_member("z1", "g1", "w1", accessVlan=10)

    assert json.loads(route.calls.last.request.content) == {
        "id": "w1",
        "accessVlan": 10,
    }


def test_modify_member_patches(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1/members/w1").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.modify_member("z1", "g1", "w1", {"accessVlan": 20})

    assert route.calls.last.request.method == "PATCH"
    assert json.loads(route.calls.last.request.content) == {"accessVlan": 20}


def test_replace_member_puts(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.put(f"{GROUPS}/g1/members/w1").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.replace_member("z1", "g1", "w1", {"accessVlan": 30})

    assert route.calls.last.request.method == "PUT"


def test_remove_member_deletes(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{GROUPS}/g1/members/w1").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.remove_member("z1", "g1", "w1")

    assert route.calls.last.request.method == "DELETE"


def test_upsert_creates_when_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200, json={"totalCount": 0, "hasMore": False, "list": []}
        )
    )
    create = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g9"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.wlan_groups.upsert_by_name("z1", "Commissioning")

    assert result == {"id": "g9"}
    assert create.called


def test_upsert_patches_when_present(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "g1", "name": "Commissioning"}],
            },
        )
    )
    patch = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))
    create = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "gX"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.upsert_by_name("z1", "Commissioning", description="updated")

    assert patch.called
    assert not create.called
    assert json.loads(patch.calls.last.request.content) == {"description": "updated"}


def test_create_rejects_short_name_without_calling_api(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.wlan_groups.create("z1", "x")

    assert not route.called


def test_create_rejects_long_name(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.wlan_groups.create("z1", "n" * 33)

    assert not route.called


def test_create_rejects_leading_space(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(GROUPS).mock(return_value=httpx.Response(201, json={"id": "g1"}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.wlan_groups.create("z1", " leading")


def test_create_accepts_boundary_length_names(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(GROUPS).mock(return_value=httpx.Response(201, json={"id": "g1"}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.wlan_groups.create("z1", "ab")
        client.wlan_groups.create("z1", "n" * 32)
