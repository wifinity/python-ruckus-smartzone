"""Tests for the Switch Manager deployment helper."""

import json
from typing import Any, Callable, Dict, List, Optional

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import (
    SmartZoneDeploymentError,
    SmartZoneDeploymentTimeoutError,
)
from ruckus_smartzone.switchm import deployments
from tests.switchm_support import MAC, SWITCHM

OTHER = "02:00:00:AA:BB:02"


def tx(tid: str, status: str, switch: str = MAC, kind: str = "PORT_CONFIGURATION"):
    return {
        "transactionId": tid,
        "deployStatus": status,
        "switchIds": switch,
        "configType": kind,
    }


class FakeClock:
    """Monotonic clock that advances on sleep and runs a hook per sleep."""

    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: List[float] = []
        self.on_sleep: Optional[Callable[[], None]] = None

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds
        if self.on_sleep:
            self.on_sleep()


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    fake = FakeClock()
    monkeypatch.setattr(deployments, "time", fake)
    return fake


class History:
    """Group configuration history served oldest first, paged by the request."""

    def __init__(self, respx_mock: respx.MockRouter, entries: List[Dict]) -> None:
        self.entries = entries
        self.details: Dict[str, List[Dict[str, Any]]] = {}
        self.route = respx_mock.post(f"{SWITCHM}/configurationHistory/query/g").mock(
            side_effect=self._history
        )
        respx_mock.post(f"{SWITCHM}/configurationHistory/detail/query").mock(
            side_effect=self._detail
        )

    def _history(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        start = (body["page"] - 1) * body["limit"]
        items = self.entries[start : start + body["limit"]]
        return httpx.Response(
            200, json={"totalCount": len(self.entries), "hasMore": True, "list": items}
        )

    def _detail(self, request: httpx.Request) -> httpx.Response:
        tid = json.loads(request.content)["filters"][0]["value"]
        items = self.details.get(tid, [{"transactionId": tid, "clis": "x"}])
        return httpx.Response(200, json={"totalCount": len(items), "list": items})

    def set(self, tid: str, status: str) -> None:
        for entry in self.entries:
            if entry["transactionId"] == tid:
                entry["deployStatus"] = status


def test_waits_for_started_then_success(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [tx("old", "SUCCESS")])
    tracker = sz.switchm.deployments.track("g", [MAC])
    history.entries.append(tx("t1", "STARTED"))
    clock.on_sleep = lambda: history.set("t1", "SUCCESS")

    result = tracker.wait(poll_interval=5, settle=10)

    assert [r["transaction"]["transactionId"] for r in result] == ["t1"]
    assert result[0]["details"] == [{"transactionId": "t1", "clis": "x"}]
    assert clock.now >= 10


def test_waits_for_a_second_transaction(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])
    tracker = sz.switchm.deployments.track("g", [MAC])
    history.entries.append(tx("t1", "SUCCESS"))
    steps = iter(
        [
            lambda: history.entries.append(tx("t2", "STARTED", kind="AUTHENTICATION")),
            lambda: history.set("t2", "SUCCESS"),
        ]
    )
    clock.on_sleep = lambda: next(steps, lambda: None)()

    result = tracker.wait(poll_interval=5, settle=10)

    assert [r["transaction"]["transactionId"] for r in result] == ["t1", "t2"]


def test_failure_raises_with_line_and_message(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])
    tracker = sz.switchm.deployments.track("g")
    history.entries.append(tx("t1", "FAILURE", kind="CLI_UPDATE"))
    history.details["t1"] = [
        {
            "transactionId": "t1",
            "switchId": MAC,
            "dispatchStatus": "FAILED",
            "clis": "a\nbogus 42\nb",
            "dispatchFailedReason": [
                {
                    "status": "FAILED",
                    "lineNumber": "2",
                    "message": "Invalid input-&gt;bogus 42 Node doesn&#39;t exist ",
                }
            ],
        }
    ]

    with pytest.raises(SmartZoneDeploymentError) as excinfo:
        tracker.wait()

    err = excinfo.value
    assert err.transaction_id == "t1"
    assert err.switch_id == MAC
    assert err.line == 2
    assert err.switch_message == "Invalid input->bogus 42 Node doesn't exist"
    assert "line 2" in err.message and "CLI_UPDATE" in err.message
    assert err.details[0]["clis"] == "a\nbogus 42\nb"
    assert clock.sleeps == []


def test_failure_without_reason_uses_dispatch_error(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])
    tracker = sz.switchm.deployments.track("g")
    history.entries.append(tx("t1", "FAILURE"))
    history.details["t1"] = [
        {
            "switchId": MAC,
            "dispatchStatus": "FAILED",
            "dispatchError": "Failed to apply configuration due to an ongoing "
            "local configuration change on the switch",
        }
    ]

    with pytest.raises(SmartZoneDeploymentError) as excinfo:
        tracker.wait()

    assert excinfo.value.line is None
    assert excinfo.value.local_config_conflict


def test_timeout_when_nothing_appears(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    History(respx_mock, [tx("old", "SUCCESS")])
    tracker = sz.switchm.deployments.track("g")

    with pytest.raises(SmartZoneDeploymentTimeoutError) as excinfo:
        tracker.wait(timeout=20, poll_interval=5)

    assert excinfo.value.transactions == []
    assert "no transaction appeared" in excinfo.value.message


def test_timeout_while_started(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])
    tracker = sz.switchm.deployments.track("g")
    history.entries.append(tx("t1", "STARTED"))

    with pytest.raises(SmartZoneDeploymentTimeoutError) as excinfo:
        tracker.wait(timeout=20, poll_interval=5)

    assert [t["transactionId"] for t in excinfo.value.transactions] == ["t1"]


def test_ignores_other_switches(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])
    tracker = sz.switchm.deployments.track("g", ["020000aabb01"])
    history.entries.append(tx("x", "FAILURE", switch=OTHER))
    history.entries.append(tx("t1", "SUCCESS", switch=f"{OTHER},{MAC}"))

    result = tracker.wait(settle=0)

    assert [r["transaction"]["transactionId"] for r in result] == ["t1"]


def test_new_transaction_in_the_middle_of_history_is_found(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [tx("a", "SUCCESS"), tx("b", "SUCCESS")])
    tracker = sz.switchm.deployments.track("g")
    history.entries.insert(1, tx("t1", "SUCCESS"))

    result = tracker.wait(settle=0)

    assert [r["transaction"]["transactionId"] for r in result] == ["t1"]


def test_history_is_read_in_full_pages(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    size = deployments.HISTORY_PAGE_SIZE
    history = History(respx_mock, [tx(f"o{i}", "SUCCESS") for i in range(size + 5)])
    tracker = sz.switchm.deployments.track("g")
    history.entries.insert(3, tx("t1", "SUCCESS"))

    result = tracker.wait(settle=0)

    assert [r["transaction"]["transactionId"] for r in result] == ["t1"]
    bodies = [json.loads(c.request.content) for c in history.route.calls]
    assert {b["limit"] for b in bodies} == {size}
    assert [b["page"] for b in bodies[:2]] == [1, 2]


def test_run_returns_write_result_and_deployments(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])

    def write() -> Dict[str, str]:
        history.entries.append(tx("t1", "SUCCESS"))
        return {"id": "c1"}

    result, done = sz.switchm.deployments.run("g", write, switch_ids=[MAC], settle=0)

    assert result == {"id": "c1"}
    assert done[0]["transaction"]["transactionId"] == "t1"


def test_tracker_is_a_context_manager(
    respx_mock: respx.MockRouter, sz: SmartZoneClient, clock: FakeClock
) -> None:
    history = History(respx_mock, [])

    with sz.switchm.deployments.track("g") as tracker:
        history.entries.append(tx("t1", "APPLIED"))

    assert tracker.wait(settle=0)[0]["transaction"]["deployStatus"] == "APPLIED"
