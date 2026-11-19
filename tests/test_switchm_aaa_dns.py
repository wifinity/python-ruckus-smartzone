"""Tests for the AAA server/settings and DNS wrappers."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from tests.switchm_support import SWITCHM, page, sent_json

AAA = f"{SWITCHM}/group/g/aaaServers"


def test_aaa_list_get(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    respx_mock.get(AAA).mock(return_value=page([{"id": "a1"}], total=1))
    respx_mock.get(f"{AAA}/a1").mock(
        return_value=httpx.Response(200, json={"id": "a1"})
    )

    assert sz.switchm.aaa_servers.list("g") == [{"id": "a1"}]
    assert sz.switchm.aaa_servers.get("g", "a1") == {"id": "a1"}


def test_aaa_create_update_delete(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    create = respx_mock.post(AAA).mock(return_value=httpx.Response(204))
    respx_mock.get(f"{AAA}/a1").mock(
        return_value=httpx.Response(
            200, json={"id": "a1", "name": "radius-1", "authPort": 1812}
        )
    )
    update = respx_mock.put(f"{AAA}/a1").mock(return_value=httpx.Response(204))
    delete = respx_mock.delete(f"{AAA}/a1").mock(return_value=httpx.Response(204))
    bulk = respx_mock.delete(AAA).mock(return_value=httpx.Response(204))
    fields = {
        "name": "radius-1",
        "serverType": "RADIUS",
        "ip": "192.0.2.1",
        "authPort": 1812,
        "secret": "s",
    }

    sz.switchm.aaa_servers.create("g", fields)
    sz.switchm.aaa_servers.update("g", "a1", {"secret": "t"})
    sz.switchm.aaa_servers.delete("g", "a1")
    sz.switchm.aaa_servers.delete_many("g", ["a1"])
    assert sz.switchm.aaa_servers.delete_many("g", []) is None

    assert sent_json(create) == fields
    assert sent_json(update) == {"name": "radius-1", "authPort": 1812, "secret": "t"}
    assert delete.called
    assert bulk.call_count == 1 and sent_json(bulk) == {"idList": ["a1"]}


def test_aaa_refuses_unknown_field(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.aaa_servers.create("g", {"name": "x", "id": "a1"})


def test_aaa_settings(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    respx_mock.get(f"{SWITCHM}/group/g/aaaSettings").mock(
        return_value=httpx.Response(
            200, json={"authentication": {}, "accounting": {"x": 1}, "altoId": None}
        )
    )
    put = respx_mock.put(f"{SWITCHM}/group/g/aaaSettings").mock(
        return_value=httpx.Response(204)
    )

    assert sz.switchm.aaa_servers.get_settings("g")["authentication"] == {}
    sz.switchm.aaa_servers.update_settings(
        "g", {"authentication": {"firstPref": "RADIUS"}}
    )

    assert sent_json(put) == {
        "authentication": {"firstPref": "RADIUS"},
        "accounting": {"x": 1},
    }


def test_dns(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    get = respx_mock.get(f"{SWITCHM}/dnsConfig/g").mock(
        return_value=httpx.Response(200, json={"dns": {"ip": ""}})
    )
    create = respx_mock.post(f"{SWITCHM}/dnsConfig").mock(
        return_value=httpx.Response(204)
    )
    update = respx_mock.put(f"{SWITCHM}/dnsConfig/g").mock(
        return_value=httpx.Response(204)
    )
    delete = respx_mock.delete(f"{SWITCHM}/dnsConfig/g").mock(
        return_value=httpx.Response(204)
    )

    assert sz.switchm.dns.get("g") == {"dns": {"ip": ""}}
    sz.switchm.dns.create("g", "192.0.2.53")
    sz.switchm.dns.update("g", "192.0.2.54")
    sz.switchm.dns.delete("g")

    assert get.called and delete.called
    assert sent_json(create) == {"id": "g", "dns": {"ip": "192.0.2.53"}}
    assert sent_json(update) == {"dns": {"ip": "192.0.2.54"}}
