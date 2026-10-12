"""Tests for the DPSK key resource wrapper."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneAPIError, SmartZoneNotFoundError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
DPSK = f"{BASE}/rkszones/z1/wlans/w1/dpsk"
DELETE_EXPIRED = f"{BASE}/rkszones/z1/deleteExpiredDpsk"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def page(items: list, *, has_more: bool, total: int) -> httpx.Response:
    return httpx.Response(
        200, json={"totalCount": total, "hasMore": has_more, "list": items}
    )


def test_list_follows_pagination(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(DPSK).mock(
        side_effect=[
            page([{"id": "k1"}], has_more=True, total=2),
            page([{"id": "k2"}], has_more=False, total=2),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        keys = client.dpsk.list("z1", "w1")

    assert [k["id"] for k in keys] == ["k1", "k2"]
    assert route.call_count == 2


def test_list_zone_hits_zone_path(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{BASE}/rkszones/z1/dpsk").mock(
        return_value=page([{"id": "k1"}], has_more=False, total=1)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        keys = client.dpsk.list_zone("z1")

    assert keys == [{"id": "k1"}]
    assert route.called


def test_get_unwraps_single_item_list(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{DPSK}/k1").mock(
        return_value=page(
            [{"id": "k1", "userName": "room-101"}], has_more=False, total=1
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        key = client.dpsk.get("z1", "w1", "k1")

    assert key == {"id": "k1", "userName": "room-101"}


def test_get_returns_plain_object_unchanged(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{DPSK}/k1").mock(
        return_value=httpx.Response(200, json={"id": "k1", "userName": "room-101"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        key = client.dpsk.get("z1", "w1", "k1")

    assert key == {"id": "k1", "userName": "room-101"}


def test_get_empty_list_raises_not_found(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{DPSK}/k1").mock(return_value=page([], has_more=False, total=0))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.dpsk.get("z1", "w1", "k1")


def test_get_error_code_211_maps_to_not_found(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{DPSK}/missing").mock(
        return_value=httpx.Response(403, json={"errorCode": 211, "message": "nope"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.dpsk.get("z1", "w1", "missing")


def test_generate_maps_supplied_kwargs_only(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    result = {"resultCount": 3, "dpskInfoList": [{"id": "a"}, {"id": "b"}, {"id": "c"}]}
    route = respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(201, json=result)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        out = client.dpsk.generate(
            "z1", "w1", amount=3, user_name="student", vlan_id=20, group_dpsk=False
        )

    assert out == result
    assert json.loads(route.calls.last.request.content) == {
        "amount": 3,
        "userName": "student",
        "vlanId": 20,
        "groupDpsk": False,
    }


def test_generate_sends_passphrase_list_and_role(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(201, json={"resultCount": 2, "dpskInfoList": []})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.dpsk.generate(
            "z1", "w1", passphrases=("pass-one-1", "pass-two-2"), user_role_id="r1"
        )

    assert json.loads(route.calls.last.request.content) == {
        "passphraseList": ["pass-one-1", "pass-two-2"],
        "userRoleId": "r1",
    }


def test_create_posts_single_key_and_returns_it(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(
            201,
            json={
                "resultCount": 1,
                "dpskInfoList": [{"id": "k1", "userName": "room-101"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        key = client.dpsk.create(
            "z1", "w1", user_name="room-101", passphrase="secret-pass", vlan_id=101
        )

    assert key == {"id": "k1", "userName": "room-101"}
    assert json.loads(route.calls.last.request.content) == {
        "amount": 1,
        "passphraseList": ["secret-pass"],
        "userName": "room-101",
        "vlanId": 101,
    }


def test_create_without_passphrase_omits_passphrase_list(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(
            201, json={"resultCount": 1, "dpskInfoList": [{"id": "k1"}]}
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.dpsk.create("z1", "w1", user_name="room-101")

    assert json.loads(route.calls.last.request.content) == {
        "amount": 1,
        "userName": "room-101",
    }


def test_create_group_key_sends_group_flag(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(
            201,
            json={"resultCount": 1, "dpskInfoList": [{"id": "g1", "groupDpsk": True}]},
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        key = client.dpsk.create(
            "z1",
            "w1",
            user_name="residents",
            passphrase="group-pass",
            vlan_id=103,
            group_dpsk=True,
        )

    assert key["groupDpsk"] is True
    assert json.loads(route.calls.last.request.content) == {
        "amount": 1,
        "passphraseList": ["group-pass"],
        "userName": "residents",
        "vlanId": 103,
        "groupDpsk": True,
    }


def test_create_raises_when_no_key_returned(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(f"{DPSK}/batchGenUnbound").mock(
        return_value=httpx.Response(201, json={"resultCount": 0, "dpskInfoList": []})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneAPIError):
            client.dpsk.create("z1", "w1", user_name="room-101")


def test_update_patches_user_name_only(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{DPSK}/k1").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.dpsk.update("z1", "w1", "k1", user_name="room-102")

    assert json.loads(route.calls.last.request.content) == {"userName": "room-102"}


def test_delete_many_posts_id_list(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(DPSK).mock(
        return_value=httpx.Response(200, json={"resultCount": 2})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        count = client.dpsk.delete_many("z1", "w1", ["k1", "k2"])

    assert count == 2
    assert route.calls.last.request.method == "POST"
    assert json.loads(route.calls.last.request.content) == {"idList": ["k1", "k2"]}


def test_delete_many_empty_makes_no_request(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(DPSK).mock(
        return_value=httpx.Response(200, json={"resultCount": 0})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        count = client.dpsk.delete_many("z1", "w1", [])

    assert count == 0
    assert not route.called


def test_delete_sends_one_item_id_list(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(DPSK).mock(
        return_value=httpx.Response(200, json={"resultCount": 1})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        count = client.dpsk.delete("z1", "w1", "k1")

    assert count == 1
    assert json.loads(route.calls.last.request.content) == {"idList": ["k1"]}


def test_upload_sends_multipart_csv(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    result = {"resultCount": 1, "dpskInfoList": [{"id": "k1"}]}
    route = respx_mock.post(f"{DPSK}/upload").mock(
        return_value=httpx.Response(201, json=result)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        out = client.dpsk.upload("z1", "w1", "User Name,Passphrase\nroom-101,pw\n")

    request = route.calls.last.request
    body = request.content
    assert out == result
    assert request.headers["content-type"].startswith("multipart/form-data")
    assert b'name="uploadFile"; filename="dpsk.csv"' in body
    assert b"room-101,pw" in body


def test_upload_accepts_bytes_and_filename(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{DPSK}/upload").mock(
        return_value=httpx.Response(201, json={"resultCount": 0, "dpskInfoList": []})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.dpsk.upload("z1", "w1", b"a,b\n", filename="keys.csv")

    assert b'filename="keys.csv"' in route.calls.last.request.content


def test_find_by_user_name_returns_match(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(DPSK).mock(
        return_value=page(
            [
                {"id": "k1", "userName": "room-101"},
                {"id": "k2", "userName": "room-102"},
            ],
            has_more=False,
            total=2,
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        key = client.dpsk.find_by_user_name("z1", "w1", "room-102")

    assert key["id"] == "k2"


def test_find_by_user_name_missing_raises_not_found(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(DPSK).mock(return_value=page([], has_more=False, total=0))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.dpsk.find_by_user_name("z1", "w1", "room-101")


def test_find_by_user_name_duplicate_raises_value_error(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(DPSK).mock(
        return_value=page(
            [{"id": "k1", "userName": "dup"}, {"id": "k2", "userName": "dup"}],
            has_more=False,
            total=2,
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.dpsk.find_by_user_name("z1", "w1", "dup")


def test_get_delete_expired(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    respx_mock.get(DELETE_EXPIRED).mock(
        return_value=httpx.Response(200, json={"deleteExpiredDpsk": "Never"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        setting = client.dpsk.get_delete_expired("z1")

    assert setting == {"deleteExpiredDpsk": "Never"}


def test_set_delete_expired_puts_interval(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.put(DELETE_EXPIRED).mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.dpsk.set_delete_expired("z1", "AfterOneDay")

    assert json.loads(route.calls.last.request.content) == {
        "deleteExpiredDpsk": "AfterOneDay"
    }


def test_set_delete_expired_rejects_unknown_interval(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.put(DELETE_EXPIRED).mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.dpsk.set_delete_expired("z1", "Weekly")

    assert not route.called
