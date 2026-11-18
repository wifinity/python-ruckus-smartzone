"""Tests for the switch wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from tests.switchm_support import MAC, SWITCHM, page, sent_json


def test_list_group_filters_on_switch_group(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switch").mock(
        return_value=page([{"id": MAC}], total=1)
    )

    assert sz.switchm.switches.list_group("g") == [{"id": MAC}]
    assert sent_json(route)["filters"] == [{"type": "SWITCH_GROUP", "value": "g"}]


def test_find_by_serial_keeps_exact_match(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switch").mock(
        return_value=page(
            [
                {"id": "A", "serialNumber": "SER123X"},
                {"id": "B", "serialNumber": "SER123"},
            ],
            total=2,
        )
    )

    found = sz.switchm.switches.find_by_serial("SER123")

    assert found["id"] == "B"
    assert sent_json(route)["fullTextSearch"] == {"type": "AND", "value": "SER123"}


def test_find_by_serial_miss_and_duplicate(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.post(f"{SWITCHM}/switch").mock(
        side_effect=[
            page([{"serialNumber": "OTHER"}], total=1),
            page([{"serialNumber": "S"}, {"serialNumber": "S"}], total=2),
        ]
    )

    with pytest.raises(SmartZoneNotFoundError):
        sz.switchm.switches.find_by_serial("S")
    with pytest.raises(ValueError):
        sz.switchm.switches.find_by_serial("S")


def test_get_and_delete_normalise_mac(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    get = respx_mock.get(f"{SWITCHM}/switch/{MAC}").mock(
        return_value=httpx.Response(200, json={"id": MAC})
    )
    delete = respx_mock.delete(f"{SWITCHM}/switch/{MAC}").mock(
        return_value=httpx.Response(200, json={"id": "audit"})
    )

    sz.switchm.switches.get("020000aabb01")
    sz.switchm.switches.delete("02-00-00-aa-bb-01")

    assert get.called and delete.called


def test_move_sends_normalised_mac_list(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.put(f"{SWITCHM}/switch/move/g").mock(
        return_value=httpx.Response(204)
    )

    sz.switchm.switches.move("g", ["020000aabb01"])

    assert sent_json(route) == [MAC]


def test_move_refuses_empty_or_bad_mac(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.switches.move("g", [])
    with pytest.raises(ValueError):
        sz.switchm.switches.move("g", ["not-a-mac"])


def test_port_details_uses_switch_extra_filter(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switch/ports/details").mock(
        return_value=page(
            [{"portIdentifier": "1/1/1", "neighborName": "uplink"}], total=1
        )
    )

    ports = sz.switchm.switches.port_details("020000aabb01")

    assert ports[0]["neighborName"] == "uplink"
    body = sent_json(route)
    assert body["extraFilters"] == [{"type": "SWITCH", "value": MAC}]
    assert "filters" not in body
