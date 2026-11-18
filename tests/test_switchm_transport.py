"""Tests for the Switch Manager sub-client transport and pager."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.switchm import switchm_base_url
from tests.switchm_support import (
    CONTROLLER,
    PUBLIC,
    SWITCHM,
    page,
    sent_json,
)


def test_base_url_is_derived_from_controller_root() -> None:
    assert (
        switchm_base_url("https://h.example:8443/wsg/api/public/v13_1/")
        == "https://h.example:8443/switchm/api/v13_1/"
    )


def test_client_exposes_switchm_root(sz: SmartZoneClient) -> None:
    assert sz.switchm.base_url == f"{SWITCHM}/"


def test_get_sends_ticket_to_switchm_path(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.get(f"{SWITCHM}/group/g-1").mock(
        return_value=httpx.Response(200, json={"id": "g-1"})
    )

    assert sz.switchm.get("/group/g-1") == {"id": "g-1"}
    assert route.calls[0].request.url.params["serviceTicket"] == "t-1"


@pytest.mark.parametrize("verb", ["post", "put", "patch", "delete"])
def test_write_verbs_send_json(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, verb: str
) -> None:
    route = respx_mock.route(method=verb.upper(), url=f"{SWITCHM}/vlans").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    result = getattr(sz.switchm, verb)("vlans", json={"a": 1})

    assert result == {"ok": True}
    assert sent_json(route) == {"a": 1}


def test_ticket_refresh_on_401_is_shared(respx_mock: respx.MockRouter) -> None:
    logon = respx_mock.post(f"{PUBLIC}/serviceTicket").mock(
        side_effect=[
            httpx.Response(200, json={"serviceTicket": "t-1"}),
            httpx.Response(200, json={"serviceTicket": "t-2"}),
        ]
    )
    respx_mock.delete(f"{PUBLIC}/serviceTicket").mock(return_value=httpx.Response(204))
    route = respx_mock.get(f"{SWITCHM}/switch/x").mock(
        side_effect=[httpx.Response(401), httpx.Response(200, json={"id": "x"})]
    )

    with SmartZoneClient(CONTROLLER, "admin", "pw") as sz:
        assert sz.switchm.get("switch/x") == {"id": "x"}

    assert logon.call_count == 2
    assert route.calls[1].request.url.params["serviceTicket"] == "t-2"


def test_busy_response_is_retried(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, no_sleep: list
) -> None:
    respx_mock.get(f"{SWITCHM}/dnsConfig/g").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json={"dns": {}})]
    )

    assert sz.switchm.get("dnsConfig/g") == {"dns": {}}
    assert no_sleep == [1.0]


def test_query_pages_by_page_and_limit(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switch").mock(
        side_effect=[
            page([{"i": 1}, {"i": 2}], total=3, has_more=True),
            page([{"i": 3}], total=3, has_more=False),
        ]
    )

    items = sz.switchm.query("switch", {"filters": []}, page_size=2)

    assert [i["i"] for i in items] == [1, 2, 3]
    assert sent_json(route, 0) == {"filters": [], "page": 1, "limit": 2}
    assert sent_json(route, 1) == {"filters": [], "page": 2, "limit": 2}


def test_query_trusts_total_count_over_has_more(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/job").mock(
        return_value=page([{"i": 1}], total=1, has_more=True)
    )

    assert sz.switchm.query("job") == [{"i": 1}]
    assert route.call_count == 1


def test_query_clamps_page_size(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switch").mock(return_value=page([], total=0))

    sz.switchm.query("switch", page_size=5000)

    assert sent_json(route)["limit"] == 1000


def test_get_pages_uses_query_parameters(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.get(f"{SWITCHM}/clitemplate/update").mock(
        side_effect=[
            page([{"i": 1}], total=2, has_more=True),
            page([{"i": 2}], total=2, has_more=False),
        ]
    )

    items = sz.switchm.get_pages(
        "clitemplate/update", params={"switchGroupId": "g"}, page_size=1
    )

    assert [i["i"] for i in items] == [1, 2]
    params = route.calls[1].request.url.params
    assert (params["switchGroupId"], params["page"], params["limit"]) == (
        "g",
        "2",
        "1",
    )
