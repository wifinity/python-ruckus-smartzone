"""Tests for the port settings wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from ruckus_smartzone.switchm.ports import BULK_IGNORABLE, BULK_PLACEHOLDERS
from tests.switchm_support import MAC, SWITCHM, page, sent_json

QUERY = f"{SWITCHM}/portSettings/query"


def test_list_switch_filters_on_switch_id(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(QUERY).mock(return_value=page([{"id": "p1"}], total=1))

    assert sz.switchm.port_settings.list_switch("020000aabb01") == [{"id": "p1"}]
    assert sent_json(route)["filters"] == [{"type": "switchId", "value": MAC}]


def test_find_by_port_identifier(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.post(QUERY).mock(
        return_value=page(
            [{"id": "p1", "port": "1/1/1"}, {"id": "p10", "port": "1/1/10"}], total=2
        )
    )

    assert sz.switchm.port_settings.find(MAC, "1/1/10")["id"] == "p10"
    with pytest.raises(SmartZoneNotFoundError):
        sz.switchm.port_settings.find(MAC, "1/1/48")


def test_get(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    respx_mock.get(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json={"id": "p1"})
    )

    assert sz.switchm.port_settings.get("p1") == {"id": "p1"}


CURRENT = {
    "id": "p1",
    "port": "1/1/10",
    "switchId": MAC,
    "createdTime": 1,
    "portEnabled": True,
    "poeEnabled": True,
    "lldpEnabled": True,
    "portName": "",
    "untaggedVlans": "1",
    "lldpQosList": None,
    "pppoeIa": {"enabled": False},
}


def test_update_merges_changes_into_full_body(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json=CURRENT)
    )
    route = respx_mock.put(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json={})
    )

    sz.switchm.port_settings.update(
        "p1",
        {
            "flexibleAuthenticationEnabled": True,
            "authenticationType": "802.1x_and_macauth",
            "authDefaultVlan": 91,
            "portName": None,
        },
    )

    assert sent_json(route) == {
        "portEnabled": True,
        "poeEnabled": True,
        "lldpEnabled": True,
        "portName": "",
        "untaggedVlans": "1",
        "flexibleAuthenticationEnabled": True,
        "authenticationType": "802.1x_and_macauth",
        "authDefaultVlan": 91,
    }


def test_update_sends_pppoe_ia_only_when_set(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json=CURRENT)
    )
    route = respx_mock.put(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json={})
    )

    sz.switchm.port_settings.update("p1", {"pppoeIa": {"enabled": True}})

    assert sent_json(route)["pppoeIa"] == {"enabled": True}


def test_update_refuses_bad_auth_type_before_request(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    get = respx_mock.get(f"{SWITCHM}/portSettings/p1")
    put = respx_mock.put(f"{SWITCHM}/portSettings/p1")

    with pytest.raises(ValueError):
        sz.switchm.port_settings.update("p1", {"authenticationType": "dot1x"})
    assert not get.called and not put.called


def test_update_refuses_get_body(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/portSettings/p1").mock(
        return_value=httpx.Response(200, json=CURRENT)
    )
    put = respx_mock.put(f"{SWITCHM}/portSettings/p1")

    with pytest.raises(ValueError):
        sz.switchm.port_settings.update("p1", {"id": "p1", "portName": "x"})
    assert not put.called


GROUP = "g1"
BULK = f"{SWITCHM}/portSettings/bulk"


def _ports(*settings: dict) -> httpx.Response:
    return page(list(settings), total=len(settings))


def test_bulk_update_body(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    query = respx_mock.post(QUERY).mock(
        return_value=_ports(
            {"port": "1/1/1", "portEnabled": False, "isStormControlUnitKbps": True},
            {"port": "1/1/2", "portEnabled": False, "isStormControlUnitKbps": True},
        )
    )
    route = respx_mock.post(BULK).mock(return_value=httpx.Response(204))

    sz.switchm.port_settings.bulk_update(
        "020000aabb01", GROUP, ["1/1/1", "1/1/2"], {"untaggedVlans": "20"}
    )

    body = sent_json(route)
    assert query.called
    assert body["idList"] == ["1/1/1", "1/1/2"]
    assert body["switchId"] == MAC and body["groupId"] == GROUP
    assert body["untaggedVlans"] == "20"
    assert body["portEnabled"] is False
    assert set(body["ignoreList"]) == set(BULK_IGNORABLE) - {"untaggedVlans"}
    assert set(BULK_PLACEHOLDERS) <= set(body)
    assert "pppoeIa" not in body


def test_bulk_update_port_name_and_enabled_skip_read(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    query = respx_mock.post(QUERY)
    route = respx_mock.post(BULK).mock(return_value=httpx.Response(204))

    sz.switchm.port_settings.bulk_update(
        MAC,
        GROUP,
        ["1/1/5"],
        {"portName": "ap-5", "portEnabled": True, "isStormControlUnitKbps": True},
    )

    body = sent_json(route)
    assert not query.called
    assert body["portName"] == "ap-5" and body["portEnabled"] is True
    assert "portName" not in body["ignoreList"]
    assert len(body["ignoreList"]) == len(BULK_IGNORABLE) - 1


def test_bulk_update_ports_disagree(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.post(QUERY).mock(
        return_value=_ports(
            {"port": "1/1/1", "portEnabled": True},
            {"port": "1/1/2", "portEnabled": False},
        )
    )
    route = respx_mock.post(BULK)

    with pytest.raises(ValueError):
        sz.switchm.port_settings.bulk_update(
            MAC, GROUP, ["1/1/1", "1/1/2"], {"poeEnabled": False}
        )
    with pytest.raises(SmartZoneNotFoundError):
        sz.switchm.port_settings.bulk_update(
            MAC, GROUP, ["1/1/48"], {"poeEnabled": False}
        )
    assert not route.called


@pytest.mark.parametrize(
    ("switch_id", "group_id", "ports", "fields"),
    [
        (MAC, GROUP, [], {"poeEnabled": False}),
        ("", GROUP, ["1/1/1"], {"poeEnabled": False}),
        (MAC, "", ["1/1/1"], {"poeEnabled": False}),
        (MAC, GROUP, ["1/1/1"], {"altoId": "x"}),
        (MAC, GROUP, ["1/1/1"], {"broadcastLimitPkts": 10}),
        (MAC, GROUP, ["1/1/1"], {"authenticationType": "x"}),
    ],
)
def test_bulk_update_refusals(
    respx_mock: respx.MockRouter,
    sz: SmartZoneClient,
    switch_id: str,
    group_id: str,
    ports: list,
    fields: dict,
) -> None:
    route = respx_mock.post(BULK)
    with pytest.raises(ValueError):
        sz.switchm.port_settings.bulk_update(switch_id, group_id, ports, fields)
    assert not route.called
