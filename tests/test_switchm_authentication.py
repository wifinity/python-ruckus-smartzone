"""Tests for switch authentication and flex-auth profile wrappers."""

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient
from tests.switchm_support import MAC, SWITCHM, page, sent_json

PROFILES = f"{SWITCHM}/flexibleAuthenticationProfile"


def test_switch_auth_get_and_update(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    respx_mock.get(f"{SWITCHM}/authentication/{MAC}").mock(
        return_value=httpx.Response(200, json={"authEnable": False})
    )
    put = respx_mock.put(f"{SWITCHM}/authentication/{MAC}").mock(
        return_value=httpx.Response(204)
    )

    assert sz.switchm.authentication.get("020000aabb01") == {"authEnable": False}
    sz.switchm.authentication.update("020000aabb01", enabled=True, default_vlan=4000)

    assert sent_json(put) == {"authEnable": True, "authDefaultVlan": 4000}


def test_profiles_query_and_list_group(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    query = respx_mock.post(f"{PROFILES}/query").mock(
        return_value=page([{"id": "f1"}], total=1)
    )
    respx_mock.get(f"{PROFILES}/query/g").mock(
        return_value=page([{"id": "f2"}], total=1)
    )

    assert sz.switchm.flex_auth_profiles.query({"filters": []}) == [{"id": "f1"}]
    assert sz.switchm.flex_auth_profiles.list_group("g") == [{"id": "f2"}]
    assert sent_json(query) == {"filters": [], "page": 1, "limit": 100}


def test_profiles_crud(respx_mock: respx.MockRouter, sz: SmartZoneClient) -> None:
    create = respx_mock.post(PROFILES).mock(return_value=httpx.Response(204))
    respx_mock.get(f"{PROFILES}/f1").mock(
        return_value=httpx.Response(200, json={"id": "f1"})
    )
    update = respx_mock.put(f"{PROFILES}/f1").mock(return_value=httpx.Response(204))
    delete = respx_mock.delete(f"{PROFILES}/f1").mock(return_value=httpx.Response(204))

    sz.switchm.flex_auth_profiles.create(
        {"groupId": "g", "profileName": "hn", "authenticationType": "macauth"}
    )
    assert sz.switchm.flex_auth_profiles.get("f1") == {"id": "f1"}
    sz.switchm.flex_auth_profiles.update("f1", {"authDefaultVlan": 91})
    sz.switchm.flex_auth_profiles.delete("f1")

    assert sent_json(create)["authenticationType"] == "macauth"
    assert sent_json(update) == {"authDefaultVlan": 91}
    assert delete.called


def test_profiles_refuse_bad_auth_type(
    respx_mock: respx.MockRouter, sz: SmartZoneClient
) -> None:
    create = respx_mock.post(PROFILES)
    update = respx_mock.put(f"{PROFILES}/f1")

    with pytest.raises(ValueError):
        sz.switchm.flex_auth_profiles.create({"authenticationType": "802.1X"})
    with pytest.raises(ValueError):
        sz.switchm.flex_auth_profiles.update("f1", {"authenticationType": "mab"})
    assert not create.called and not update.called
