"""Tests for the pre-flight zone guard on update, replace and move."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient, SmartZoneZoneMismatchError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
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


def test_update_proceeds_when_zone_matches(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z1")
    route = respx_mock.patch(f"{BASE}/aps/{MAC}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.update(MAC, {"description": "ok"}, expected_zone_id="z1")

    assert route.called


def test_update_refuses_on_zone_mismatch(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z2")
    route = respx_mock.patch(f"{BASE}/aps/{MAC}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneZoneMismatchError) as exc:
            client.access_points.update(
                MAC, {"description": "no"}, expected_zone_id="z1"
            )

    assert exc.value.mismatches == {MAC: "z2"}
    assert not route.called


def test_replace_refuses_on_zone_mismatch(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z2")
    route = respx_mock.put(f"{BASE}/aps/{MAC}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneZoneMismatchError):
            client.access_points.replace(
                MAC, {"name": "x", "zoneId": "z1"}, expected_zone_id="z1"
            )

    assert not route.called


def test_move_refuses_before_any_write_on_mismatch(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    register_ap_zone(respx_mock, "z2")
    move_route = respx_mock.post(f"{BASE}/aps/move").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneZoneMismatchError):
            client.access_points.move([MAC], target_zone_id="z9", expected_zone_id="z1")

    assert not move_route.called
