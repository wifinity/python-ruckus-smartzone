"""Tests for POST /query/ap page/limit pagination."""

import json
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
    return respx_mock.post(f"{BASE}/query/ap").mock(
        side_effect=[httpx.Response(200, json=page) for page in pages]
    )


def test_query_pages_with_has_more(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [
            {"totalCount": 3, "hasMore": True, "list": [{"i": 1}, {"i": 2}]},
            {"totalCount": 3, "hasMore": False, "list": [{"i": 3}]},
        ],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.access_points.query(page_size=2)

    assert [item["i"] for item in items] == [1, 2, 3]
    assert route.call_count == 2
    first = json.loads(route.calls[0].request.content)
    second = json.loads(route.calls[1].request.content)
    assert (first["page"], first["limit"]) == (1, 2)
    assert second["page"] == 2


def test_query_single_page_stops(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [{"totalCount": 1, "hasMore": False, "list": [{"i": 1}]}],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        items = client.access_points.query(page_size=100)

    assert items == [{"i": 1}]
    assert route.call_count == 1


def test_query_pages_using_total_count_when_has_more_absent(
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
        items = client.access_points.query(page_size=2)

    assert [item["i"] for item in items] == [1, 2, 3]
    assert route.call_count == 2


def test_query_merges_criteria_into_body(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = register_pages(
        respx_mock,
        [{"totalCount": 0, "hasMore": False, "list": []}],
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.query(
            {"filters": [{"type": "ZONE", "value": "z1"}]}, page_size=100
        )

    body = json.loads(route.calls.last.request.content)
    assert body["filters"] == [{"type": "ZONE", "value": "z1"}]
    assert body["limit"] == 100
