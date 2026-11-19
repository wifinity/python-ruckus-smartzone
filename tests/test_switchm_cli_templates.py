"""Tests for the CLI template wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from tests.switchm_support import MAC, SWITCHM, page, sent_json


def test_list_passes_group_and_pages(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.get(f"{SWITCHM}/clitemplate/provision").mock(
        return_value=page([{"id": "t1", "cliTemplateConfigId": "c1"}], total=1)
    )

    items = sz.switchm.cli_templates.list("provision", "g")

    assert items[0]["id"] == "t1"
    assert route.calls[0].request.url.params["switchGroupId"] == "g"


def test_unknown_kind_refused(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.cli_templates.list("startup", "g")


def test_get_uses_config_id(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    respx_mock.get(f"{SWITCHM}/clitemplate/update/c1").mock(
        return_value=httpx.Response(200, json={"cli": "x"})
    )

    assert sz.switchm.cli_templates.get("update", "c1") == {"cli": "x"}


def test_create_provision_joins_models(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/clitemplate/provision").mock(
        return_value=httpx.Response(200, json={"id": "c1"})
    )

    result = sz.switchm.cli_templates.create_provision(
        "g", "baseline", "ver 10.0.20\n", ["ICX8200-48P", "ICX8100-24P"]
    )

    assert result == {"id": "c1"}
    assert sent_json(route) == {
        "groupId": "g",
        "name": "baseline",
        "cli": "ver 10.0.20\n",
        "models": "ICX8200-48P,ICX8100-24P",
    }


def test_create_update_joins_normalised_switches(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.post(f"{SWITCHM}/clitemplate/update").mock(
        return_value=httpx.Response(200, json={"id": "c2"})
    )

    sz.switchm.cli_templates.create_update(
        "g",
        "stp",
        "spanning-tree 802-1w priority 4096\n",
        ["020000aabb01", "02:00:00:AA:BB:02"],
        reload=False,
    )

    body = sent_json(route)
    assert body["switches"] == f"{MAC},02:00:00:AA:BB:02"
    assert body["reload"] is False
    assert "pushTimeType" not in body


def test_create_update_needs_a_switch(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.cli_templates.create_update("g", "n", "cli", [])


def test_replace_validates_against_kind(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/clitemplate/provision/c1").mock(
        return_value=httpx.Response(
            200, json={"id": "c1", "name": "baseline", "cli": "x", "models": "M"}
        )
    )
    route = respx_mock.put(f"{SWITCHM}/clitemplate/provision/c1").mock(
        return_value=httpx.Response(204)
    )

    sz.switchm.cli_templates.replace("provision", "c1", {"cli": "y"})

    assert sent_json(route) == {"name": "baseline", "cli": "y", "models": "M"}
    with pytest.raises(ValueError):
        sz.switchm.cli_templates.replace("provision", "c1", {"switches": "x"})


def test_delete_uses_list_entry_id(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.delete(f"{SWITCHM}/clitemplate/update/t1").mock(
        return_value=httpx.Response(204)
    )

    sz.switchm.cli_templates.delete("update", "t1")

    assert route.called
