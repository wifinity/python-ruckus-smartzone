"""Tests for the index/listSize pagination helper."""

from typing import List

import httpx
import respx

from ruckus_smartzone import SmartZoneClient

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def register_pages(respx_mock: respx.MockRouter, pages: List[dict]) -> respx.Route:
    return respx_mock.get(f"{BASE}/aps").mock(
        side_effect=[httpx.Response(200, json=page) for page in pages]
    )


def test_paginates_across_pages_with_has_more(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [
            {
                "totalCount": 3,
                "hasMore": True,
                "firstIndex": 0,
                "list": [{"i": 1}, {"i": 2}],
            },
            {
                "totalCount": 3,
                "hasMore": False,
                "firstIndex": 2,
                "list": [{"i": 3}],
            },
        ],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.paginate("aps", page_size=2)

    assert [item["i"] for item in items] == [1, 2, 3]
    assert route.call_count == 2
    assert route.calls[0].request.url.params["index"] == "0"
    assert route.calls[0].request.url.params["listSize"] == "2"
    assert route.calls[1].request.url.params["index"] == "2"


def test_single_page_stops_immediately(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [{"totalCount": 1, "hasMore": False, "firstIndex": 0, "list": [{"i": 1}]}],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.paginate("aps", page_size=100)

    assert items == [{"i": 1}]
    assert route.call_count == 1


def test_paginates_using_total_count_when_has_more_absent(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [
            {"totalCount": 3, "list": [{"i": 1}, {"i": 2}]},
            {"totalCount": 3, "list": [{"i": 3}]},
        ],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.paginate("aps", page_size=2)

    assert [item["i"] for item in items] == [1, 2, 3]
    assert route.call_count == 2


def test_page_size_clamped_to_maximum(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [{"totalCount": 0, "hasMore": False, "list": []}],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.paginate("aps", page_size=5000)

    assert items == []
    assert route.calls.last.request.url.params["listSize"] == "1000"
