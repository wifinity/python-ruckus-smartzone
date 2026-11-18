"""Tests for the switch group wrapper."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from ruckus_smartzone.exceptions import SmartZoneNotFoundError
from tests.switchm_support import SWITCHM, sent_json

BY_DOMAIN = f"{SWITCHM}/group/ids/byDomain/d-1"


def by_domain(*labels: str) -> httpx.Response:
    items = [
        {"id": f"id-{label}", "label": label, "type": "Ruckus"} for label in labels
    ]
    return httpx.Response(
        200,
        json={"success": True, "data": {"totalCount": len(items), "list": items}},
    )


def test_list_unwraps_envelope(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.get(BY_DOMAIN).mock(return_value=by_domain("Staging Group", "a"))

    groups = sz.switchm.groups.list("d-1")

    assert [g["label"] for g in groups] == ["Staging Group", "a"]
    assert "showStagingGroup" not in route.calls[0].request.url.params


def test_list_passes_staging_flag(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    route = respx_mock.get(BY_DOMAIN).mock(return_value=by_domain())

    assert sz.switchm.groups.list("d-1", show_staging_group=False) == []
    assert route.calls[0].request.url.params["showStagingGroup"] == "false"


def test_find_by_name_returns_full_group(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(BY_DOMAIN).mock(return_value=by_domain("a", "b"))
    respx_mock.get(f"{SWITCHM}/group/id-b").mock(
        return_value=httpx.Response(200, json={"id": "id-b", "name": "b"})
    )

    assert sz.switchm.groups.find_by_name("d-1", "b") == {"id": "id-b", "name": "b"}


def test_find_by_name_miss_and_duplicate(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(BY_DOMAIN).mock(return_value=by_domain("a", "a"))

    with pytest.raises(SmartZoneNotFoundError):
        sz.switchm.groups.find_by_name("d-1", "z")
    with pytest.raises(ValueError):
        sz.switchm.groups.find_by_name("d-1", "a")


def test_create_update_delete(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    create = respx_mock.post(f"{SWITCHM}/group").mock(return_value=httpx.Response(204))
    patch = respx_mock.patch(f"{SWITCHM}/group/g").mock(
        return_value=httpx.Response(200, json={"id": "audit"})
    )
    delete = respx_mock.delete(f"{SWITCHM}/group/g").mock(
        return_value=httpx.Response(200, json={"id": "audit"})
    )

    sz.switchm.groups.create({"name": "SITE01", "domainId": "d-1", "description": None})
    sz.switchm.groups.update("g", {"description": "x"})
    sz.switchm.groups.delete("g")

    assert sent_json(create) == {"name": "SITE01", "domainId": "d-1"}
    assert sent_json(patch) == {"description": "x"}
    assert delete.called


def test_create_refuses_unknown_field(sz: SmartZoneClient) -> None:
    with pytest.raises(ValueError):
        sz.switchm.groups.create({"name": "x", "colour": "red"})
