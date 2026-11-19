"""Tests for the config backup, configuration history and job wrappers."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from tests.switchm_support import MAC, SWITCHM, page, sent_json


def test_backups_list_switch_uses_extra_filter(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switchconfig").mock(
        return_value=page([{"id": "b1"}], total=1)
    )

    assert sz.switchm.config_backups.list_switch("020000aabb01") == [{"id": "b1"}]
    body = sent_json(route)
    assert body["extraFilters"] == [{"type": "SWITCH", "value": MAC}]
    assert "filters" not in body


def test_backup_sends_switch_list_and_master_flag(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/switchconfig/backup").mock(
        return_value=httpx.Response(204)
    )

    sz.switchm.config_backups.backup(["020000aabb01"])
    sz.switchm.config_backups.backup([MAC], master=True)

    assert sent_json(route, 0) == [MAC]
    assert "master" not in route.calls[0].request.url.params
    assert route.calls[1].request.url.params["master"] == "true"
    with pytest.raises(ValueError):
        sz.switchm.config_backups.backup([])


def test_backup_content_delete_and_alerts(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/switchconfig/download/b1").mock(
        return_value=httpx.Response(
            200,
            text="ver 10.0.20\n!\n",
            headers={"content-type": "application/json;charset=UTF-8"},
        )
    )
    delete = respx_mock.delete(f"{SWITCHM}/switchconfig/b1").mock(
        return_value=httpx.Response(204)
    )
    respx_mock.get(f"{SWITCHM}/switchconfig/backup/master/alert").mock(
        return_value=page([{"switchId": MAC}], total=1, has_more=True)
    )
    respx_mock.get(f"{SWITCHM}/switchconfig/backup/master/alert/{MAC}").mock(
        return_value=httpx.Response(200, json={"diff": ""})
    )

    assert sz.switchm.config_backups.content("b1") == "ver 10.0.20\n!\n"
    sz.switchm.config_backups.delete("b1")
    assert sz.switchm.config_backups.master_alerts() == [{"switchId": MAC}]
    assert sz.switchm.config_backups.master_alert(MAC) == {"diff": ""}
    assert delete.called


def test_backup_content_error_is_mapped(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/switchconfig/download/zz").mock(
        return_value=httpx.Response(404, json={"errorCode": 211})
    )

    with pytest.raises(SmartZoneNotFoundError):
        sz.switchm.config_backups.content("zz")


def test_history_query_and_details(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    history = respx_mock.post(f"{SWITCHM}/configurationHistory/query/g").mock(
        return_value=page([{"transactionId": "t1"}], total=1)
    )
    detail = respx_mock.post(f"{SWITCHM}/configurationHistory/detail/query").mock(
        return_value=page([{"transactionId": "t1", "clis": "x"}], total=1)
    )

    assert sz.switchm.config_history.query("g") == [{"transactionId": "t1"}]
    assert sz.switchm.config_history.details("t1")[0]["clis"] == "x"

    assert sent_json(history) == {"page": 1, "limit": 100}
    assert sent_json(detail)["filters"] == [{"type": "transactionId", "value": "t1"}]


def test_jobs(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    route = respx_mock.post(f"{SWITCHM}/job").mock(return_value=page([], total=0))
    respx_mock.get(f"{SWITCHM}/job/j1").mock(
        return_value=httpx.Response(200, json={"id": "j1"})
    )

    assert sz.switchm.jobs.list_switch("020000aabb01") == []
    assert sz.switchm.jobs.get("j1") == {"id": "j1"}
    assert sent_json(route)["extraFilters"] == [{"type": "SWITCH", "value": MAC}]
