"""Tests for chunked AP move and per-batch outcome reporting."""

import json
from typing import List

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def make_macs(count: int) -> List[str]:
    return [f"8C:0C:90:2B:{i // 256:02X}:{i % 256:02X}" for i in range(count)]


def test_fifty_macs_are_one_call(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps/move").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.access_points.move(make_macs(50), target_zone_id="z1")

    assert route.call_count == 1
    assert result.all_succeeded
    assert len(result.moved_macs) == 50


def test_fifty_one_macs_split_into_two_calls(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps/move").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.access_points.move(make_macs(51), target_zone_id="z1")

    assert route.call_count == 2
    first = json.loads(route.calls[0].request.content)
    second = json.loads(route.calls[1].request.content)
    assert len(first["apMacs"]) == 50
    assert len(second["apMacs"]) == 1
    assert result.all_succeeded


def test_one_hundred_one_macs_split_into_three_calls(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps/move").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.access_points.move(make_macs(101), target_zone_id="z1")

    assert route.call_count == 3
    assert [len(json.loads(c.request.content)["apMacs"]) for c in route.calls] == [
        50,
        50,
        1,
    ]
    assert len(result.moved_macs) == 101


def test_move_sends_only_target_zone(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps/move").mock(
        return_value=httpx.Response(200, json={})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.access_points.move(make_macs(1), target_zone_id="z1")

    body = json.loads(route.calls.last.request.content)
    assert body["targetZoneId"] == "z1"
    # The endpoint is zone-only: an AP group is never folded into a move (it would
    # half-apply). Placement is a separate apGroupId set (ap_groups.add_member).
    assert "targetApGroupId" not in body


def test_move_rejects_ap_group_argument(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.post(f"{BASE}/aps/move").mock(return_value=httpx.Response(200, json={}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(TypeError):
            client.access_points.move(
                make_macs(1), target_zone_id="z1", target_ap_group_id="g1"
            )


def test_per_batch_failure_is_visible_and_later_batches_attempted(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(f"{BASE}/aps/move").mock(
        side_effect=[
            httpx.Response(400, json={"errorCode": 300}),
            httpx.Response(200, json={}),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.access_points.move(make_macs(100), target_zone_id="z1")

    assert route.call_count == 2
    assert not result.all_succeeded
    assert len(result.failed_macs) == 50
    assert len(result.moved_macs) == 50
    assert result.batches[0].ok is False
    assert result.batches[0].error is not None
    assert result.batches[1].ok is True
