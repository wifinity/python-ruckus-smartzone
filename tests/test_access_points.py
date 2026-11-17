"""Tests for the access-point resource wrapper (CRUD and reads)."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
MAC = "8C:0C:90:2B:8B:90"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def test_list_returns_all_aps(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(
            200,
            json={
                "totalCount": 2,
                "hasMore": False,
                "firstIndex": 0,
                "list": [{"mac": MAC}, {"mac": "AA:BB:CC:DD:EE:FF"}],
            },
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        aps = client.access_points.list()

    assert [ap["mac"] for ap in aps] == [MAC, "AA:BB:CC:DD:EE:FF"]


def test_list_passes_zone_filter(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{BASE}/aps").mock(
        return_value=httpx.Response(
            200, json={"totalCount": 0, "hasMore": False, "list": []}
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.list(zone_id="z1")

    assert route.calls.last.request.url.params["zoneId"] == "z1"


def test_get_normalizes_mac_into_url(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(f"{BASE}/aps/{MAC}").mock(
        return_value=httpx.Response(200, json={"mac": MAC, "zoneId": "z1"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        ap = client.access_points.get("8c0c902b8b90")

    assert ap == {"mac": MAC, "zoneId": "z1"}
    assert route.called


def test_create_posts_body_and_returns_id(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps").mock(
        return_value=httpx.Response(201, json={"mac": MAC})
    )
    payload = {"mac": MAC, "zoneId": "z1", "name": "AP-1"}

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        created = client.access_points.create(payload)

    assert created == {"mac": MAC}
    assert json.loads(route.calls.last.request.content) == payload


def test_update_patches(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.patch(f"{BASE}/aps/{MAC}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.update(MAC, {"description": "edge"})

    assert route.calls.last.request.method == "PATCH"


def test_replace_puts(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.put(f"{BASE}/aps/{MAC}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.replace(MAC, {"name": "AP-1", "zoneId": "z1"})

    assert route.calls.last.request.method == "PUT"


def test_delete_deletes(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{BASE}/aps/{MAC}").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.delete(MAC, validate_mesh=True)

    assert route.calls.last.request.method == "DELETE"
    assert route.calls.last.request.url.params["validateMesh"] == "true"


def test_operational_summary_reads_status(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{BASE}/aps/{MAC}/operational/summary").mock(
        return_value=httpx.Response(
            200, json={"mac": MAC, "registrationState": "Approved"}
        )
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        summary = client.access_points.operational_summary(MAC)

    assert summary == {"mac": MAC, "registrationState": "Approved"}


def test_clear_radio_wlan_group_deletes_ap_override(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(
        f"{BASE}/aps/{MAC}/radioConfig/radio24g/wlanGroupId"
    ).mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.clear_radio_wlan_group("8c-0c-90-2b-8b-90", "radio24g")

    assert route.calls.last.request.method == "DELETE"


@pytest.mark.parametrize(
    "radio", ["radio24g", "radio5g", "radio5gLower", "radio5gUpper", "radio6g"]
)
def test_clear_radio_wlan_group_accepts_every_radio(
    respx_mock: respx.MockRouter, controller_url: str, radio: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{BASE}/aps/{MAC}/radioConfig/{radio}/wlanGroupId").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.clear_radio_wlan_group(MAC, radio)

    assert route.called


def test_clear_radio_wlan_group_rejects_unknown_radio(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(url__regex=rf"{BASE}/aps/.*/radioConfig/.*").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError):
            client.access_points.clear_radio_wlan_group(MAC, "radio7g")

    assert not route.called


def test_clear_radio_wlan_group_propagates_not_found(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.delete(f"{BASE}/aps/{MAC}/radioConfig/radio5g/wlanGroupId").mock(
        return_value=httpx.Response(404, json={"message": "AP not found"})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(SmartZoneNotFoundError):
            client.access_points.clear_radio_wlan_group(MAC, "radio5g")
