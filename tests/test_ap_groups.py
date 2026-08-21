"""Tests for the AP group resource wrapper and its members collection."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import (
    SmartZoneNotFoundError,
    SmartZoneValidationError,
    SmartZoneZoneMismatchError,
)

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
GROUPS = f"{BASE}/rkszones/z1/apgroups"
MAC = "8C:0C:90:2B:8B:90"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def register_ap_zone(respx_mock: respx.MockRouter, zone_id: str) -> None:
    respx_mock.get(f"{BASE}/aps/{MAC}").mock(
        return_value=httpx.Response(200, json={"mac": MAC, "zoneId": zone_id})
    )


def test_create_posts_name(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        created = client.ap_groups.create("z1", "All Areas")

    assert created == {"id": "g1"}
    assert json.loads(route.calls.last.request.content) == {"name": "All Areas"}


def test_create_passes_description_and_extra_fields(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )
    radio_config = {"radio5g": {"wlanGroupId": "wg1"}}

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.create(
            "z1", "All Areas", description="temp", radioConfig=radio_config
        )

    assert json.loads(route.calls.last.request.content) == {
        "name": "All Areas",
        "description": "temp",
        "radioConfig": radio_config,
    }


def test_create_rejects_short_name_without_calling_api(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "g1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.ap_groups.create("z1", "x")

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
            client.ap_groups.create("z1", "n" * 33)

    assert not route.called


def test_create_rejects_leading_space(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(GROUPS).mock(return_value=httpx.Response(201, json={"id": "g1"}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.ap_groups.create("z1", " leading")


def test_create_accepts_boundary_length_names(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(GROUPS).mock(return_value=httpx.Response(201, json={"id": "g1"}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.create("z1", "ab")
        client.ap_groups.create("z1", "n" * 32)


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
                "list": [{"id": "g1", "name": "All Areas"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        groups = client.ap_groups.list("z1")

    assert [g["name"] for g in groups] == ["All Areas"]


def test_list_follows_pagination(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    pages = [
        httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": True,
                "firstIndex": 0,
                "list": [{"id": "g1", "name": "A"}],
            },
        ),
        httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "firstIndex": 1,
                "list": [{"id": "g2", "name": "B"}],
            },
        ),
    ]
    route = respx_mock.get(GROUPS).mock(side_effect=pages)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        groups = client.ap_groups.list("z1")

    assert [g["id"] for g in groups] == ["g1", "g2"]
    assert route.calls[0].request.url.params["index"] == "0"
    assert int(route.calls[1].request.url.params["index"]) > 0


def test_get_returns_detail(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{GROUPS}/g1").mock(
        return_value=httpx.Response(200, json={"id": "g1", "name": "All Areas"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        detail = client.ap_groups.get("z1", "g1")

    assert detail == {"id": "g1", "name": "All Areas"}


def test_get_default_reads_default_group(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{GROUPS}/default").mock(
        return_value=httpx.Response(200, json={"id": "gd", "name": "default"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        default = client.ap_groups.get_default("z1")

    assert default == {"id": "gd", "name": "default"}
    assert route.called


def test_update_patches_changes(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.update("z1", "g1", {"description": "edge"})

    assert route.calls.last.request.method == "PATCH"
    assert json.loads(route.calls.last.request.content) == {"description": "edge"}


def test_update_requires_a_field(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.ap_groups.update("z1", "g1", {})


def test_update_rejects_invalid_name_without_calling_api(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneValidationError):
            client.ap_groups.update("z1", "g1", {"name": "x"})

    assert not route.called


def test_replace_puts_full_body(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.put(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))
    body = {"name": "All Areas", "description": "full"}

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.replace("z1", "g1", body)

    assert route.calls.last.request.method == "PUT"
    assert json.loads(route.calls.last.request.content) == body


def test_delete_deletes(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.delete("z1", "g1")

    assert route.calls.last.request.method == "DELETE"


def test_find_by_name_raises_when_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200, json={"totalCount": 0, "hasMore": False, "list": []}
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.ap_groups.find_by_name("z1", "Missing")


def test_find_by_name_returns_single_match(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 1,
                "hasMore": False,
                "list": [{"id": "g1", "name": "All Areas"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        found = client.ap_groups.find_by_name("z1", "All Areas")

    assert found == {"id": "g1", "name": "All Areas"}


def test_find_by_name_raises_on_multiple(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(GROUPS).mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "list": [
                    {"id": "g1", "name": "All Areas"},
                    {"id": "g2", "name": "All Areas"},
                ],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.ap_groups.find_by_name("z1", "All Areas")


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
        result = client.ap_groups.upsert_by_name("z1", "All Areas")

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
                "list": [{"id": "g1", "name": "All Areas"}],
            },
        )
    )
    patch = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))
    create = respx_mock.post(GROUPS).mock(
        return_value=httpx.Response(201, json={"id": "gX"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.upsert_by_name("z1", "All Areas", description="updated")

    assert patch.called
    assert not create.called
    assert json.loads(patch.calls.last.request.content) == {"description": "updated"}


def test_add_member_posts_to_normalized_mac_when_zone_matches(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z1")
    route = respx_mock.post(f"{GROUPS}/g1/members/{MAC}").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.add_member("z1", "g1", "8c0c902b8b90")

    assert route.called
    assert route.calls.last.request.content == b""


def test_add_member_refuses_on_zone_mismatch(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z2")
    route = respx_mock.post(f"{GROUPS}/g1/members/{MAC}").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneZoneMismatchError) as exc:
            client.ap_groups.add_member("z1", "g1", MAC)

    assert exc.value.mismatches == {MAC: "z2"}
    assert not route.called


def test_remove_member_deletes_normalized_mac(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{GROUPS}/g1/members/{MAC}").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.remove_member("z1", "g1", "8c0c902b8b90")

    assert route.calls.last.request.method == "DELETE"


def test_set_radio_wlan_group_patches_radio_config(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.set_radio_wlan_group("z1", "g1", "radio5g", "wg1")

    assert json.loads(route.calls.last.request.content) == {
        "radioConfig": {"radio5g": {"wlanGroupId": "wg1"}}
    }


def test_set_radio_wlan_group_rejects_unknown_radio(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{GROUPS}/g1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.ap_groups.set_radio_wlan_group("z1", "g1", "radio7g", "wg1")

    assert not route.called


def test_clear_radio_wlan_group_deletes_override(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{GROUPS}/g1/radioConfig/radio5g/wlanGroupId").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.ap_groups.clear_radio_wlan_group("z1", "g1", "radio5g")

    assert route.calls.last.request.method == "DELETE"


def test_clear_radio_wlan_group_rejects_unknown_radio(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.ap_groups.clear_radio_wlan_group("z1", "g1", "radio7g")
