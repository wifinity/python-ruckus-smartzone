"""Tests for the VLAN wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from tests.switchm_support import MAC, SWITCHM, page, sent_json


def test_list_group_and_switch_filters(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/vlans/query").mock(
        return_value=page([{"vlanId": 1}], total=1)
    )

    sz.switchm.vlans.list_group("g")
    sz.switchm.vlans.list_switch("020000aabb01")

    assert sent_json(route, 0)["filters"] == [{"type": "SWITCH_GROUP", "value": "g"}]
    assert sent_json(route, 1)["filters"] == [{"type": "switchId", "value": MAC}]


def test_get_and_default_vlan(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/vlans/v1").mock(
        return_value=httpx.Response(200, json={"id": "v1"})
    )
    respx_mock.get(f"{SWITCHM}/vlans/defaultvlan/{MAC}").mock(
        return_value=httpx.Response(200, json={"vlanId": 1})
    )

    assert sz.switchm.vlans.get("v1") == {"id": "v1"}
    assert sz.switchm.vlans.default_vlan(MAC) == {"vlanId": 1}


def test_create_and_update_send_only_set_fields(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    create = respx_mock.post(f"{SWITCHM}/vlans").mock(return_value=httpx.Response(204))
    respx_mock.get(f"{SWITCHM}/vlans/v1").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "v1",
                "vlanId": 91,
                "groupId": "g",
                "name": "HN",
                "igmpSnooping": "PASSIVE",
                "ports": None,
            },
        )
    )
    update = respx_mock.put(f"{SWITCHM}/vlans/v1").mock(
        return_value=httpx.Response(200, json={})
    )

    sz.switchm.vlans.create({"groupId": "g", "vlanId": 91, "name": "HN", "ports": None})
    sz.switchm.vlans.update("v1", {"name": "HN-2"})

    assert sent_json(create) == {
        "groupId": "g",
        "vlanId": 91,
        "name": "HN",
        "pushTimeType": "NOW",
    }
    assert sent_json(update) == {"name": "HN-2", "igmpSnooping": "PASSIVE"}


def test_update_refuses_create_only_field(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.vlans.update("v1", {"vlanId": 92})


def test_delete_and_delete_many(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    one = respx_mock.delete(f"{SWITCHM}/vlans/v1").mock(
        return_value=httpx.Response(204)
    )
    many = respx_mock.delete(f"{SWITCHM}/vlans").mock(return_value=httpx.Response(204))

    sz.switchm.vlans.delete("v1")
    sz.switchm.vlans.delete_many(["v1", "v2"])
    assert sz.switchm.vlans.delete_many([]) is None

    assert one.called
    assert many.call_count == 1
    assert sent_json(many) == {"idList": ["v1", "v2"]}


def test_create_keeps_caller_push_time_type(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    create = respx_mock.post(f"{SWITCHM}/vlans").mock(return_value=httpx.Response(204))

    sz.switchm.vlans.create({"groupId": "g", "vlanId": 91, "pushTimeType": "SCHEDULE"})

    assert sent_json(create)["pushTimeType"] == "SCHEDULE"
