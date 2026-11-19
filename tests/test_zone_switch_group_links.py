"""Tests for the zone switch group link resource wrapper."""

import json

import httpx
import pytest
import respx

from ruckus_smartzone import SmartZoneClient

BASE = "https://smartzone.example:8443/wsg/api/public/v13_1"
LINKS = f"{BASE}/zoneSwitchGroupLinks"

ZONE = "00000000-0000-0000-0000-00000000000a"
OTHER_ZONE = "00000000-0000-0000-0000-00000000000b"
GROUP = "00000000-0000-0000-0000-0000000000g1"
LINK_ID = "00000000-0000-0000-0000-0000000000l1"


def register_session(respx_mock: respx.MockRouter) -> None:
    respx_mock.post(f"{BASE}/serviceTicket").mock(
        return_value=httpx.Response(200, json={"serviceTicket": "t-1"})
    )
    respx_mock.delete(f"{BASE}/serviceTicket").mock(return_value=httpx.Response(204))


def page(*items: dict) -> httpx.Response:
    return httpx.Response(
        200, json={"totalCount": len(items), "hasMore": False, "list": list(items)}
    )


def record(zone_id: str = ZONE, link: bool = True) -> dict:
    return {"id": LINK_ID, "zoneId": zone_id, "switchGroupId": GROUP, "link": link}


def test_list_sends_only_given_filters(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(LINKS).mock(return_value=page(record()))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        links = client.zone_switch_group_links.list(zone_id=ZONE, domain_id="d1")

    assert links == [record()]
    params = route.calls.last.request.url.params
    assert params["zoneId"] == ZONE
    assert params["domainId"] == "d1"
    assert "switchGroupId" not in params
    assert params["index"] == "0"


def test_list_without_filters_follows_pagination(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(LINKS).mock(
        side_effect=[
            httpx.Response(
                200, json={"totalCount": 2, "hasMore": True, "list": [record()]}
            ),
            httpx.Response(
                200,
                json={"totalCount": 2, "hasMore": False, "list": [record(OTHER_ZONE)]},
            ),
        ]
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        links = client.zone_switch_group_links.list()

    assert [link["zoneId"] for link in links] == [ZONE, OTHER_ZONE]
    assert route.call_count == 2
    first = route.calls[0].request.url.params
    assert not {"zoneId", "switchGroupId", "domainId"} & set(first)


def test_get_returns_one_link(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{LINKS}/{LINK_ID}").mock(
        return_value=httpx.Response(200, json=record())
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        link = client.zone_switch_group_links.get(LINK_ID)

    assert link == record()


def test_find_filters_by_both_ids_and_returns_the_match(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.get(LINKS).mock(
        return_value=page(record(OTHER_ZONE), record(ZONE))
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        link = client.zone_switch_group_links.find(ZONE, GROUP)

    assert link == record(ZONE)
    params = route.calls.last.request.url.params
    assert params["zoneId"] == ZONE
    assert params["switchGroupId"] == GROUP


def test_find_returns_unlinked_record(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(LINKS).mock(return_value=page(record(link=False)))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        link = client.zone_switch_group_links.find(ZONE, GROUP)

    assert link is not None
    assert link["link"] is False


def test_find_returns_none_when_no_link(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(LINKS).mock(return_value=page())

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        assert client.zone_switch_group_links.find(ZONE, GROUP) is None


def test_find_raises_on_duplicate_links(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(LINKS).mock(return_value=page(record(), {**record(), "id": "l2"}))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError, match="Multiple links"):
            client.zone_switch_group_links.find(ZONE, GROUP)


def test_create_posts_link_body(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(LINKS).mock(
        return_value=httpx.Response(200, json={"id": LINK_ID})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        result = client.zone_switch_group_links.create(ZONE, GROUP)

    assert result == {"id": LINK_ID}
    assert json.loads(route.calls.last.request.content) == {
        "zoneId": ZONE,
        "switchGroupId": GROUP,
        "link": True,
    }


def test_create_can_send_link_false(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    route = respx_mock.post(LINKS).mock(
        return_value=httpx.Response(200, json={"id": LINK_ID})
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zone_switch_group_links.create(ZONE, GROUP, link=False)

    assert json.loads(route.calls.last.request.content)["link"] is False


def test_update_merges_fields_into_full_put_body(
    respx_mock: respx.MockRouter, controller_url: str
) -> None:
    register_session(respx_mock)
    respx_mock.get(f"{LINKS}/{LINK_ID}").mock(
        return_value=httpx.Response(200, json=record())
    )
    route = respx_mock.put(f"{LINKS}/{LINK_ID}").mock(return_value=httpx.Response(204))

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zone_switch_group_links.update(LINK_ID, {"zoneId": OTHER_ZONE})

    assert json.loads(route.calls.last.request.content) == {
        "zoneId": OTHER_ZONE,
        "switchGroupId": GROUP,
        "link": True,
    }


@pytest.mark.parametrize(
    ("fields", "message"),
    [({}, "at least one field"), ({"id": "x"}, "Unknown link fields")],
)
def test_update_rejects_bad_fields_without_a_request(
    respx_mock: respx.MockRouter, controller_url: str, fields: dict, message: str
) -> None:
    register_session(respx_mock)
    get_route = respx_mock.get(f"{LINKS}/{LINK_ID}")
    put_route = respx_mock.put(f"{LINKS}/{LINK_ID}")

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        with pytest.raises(ValueError, match=message):
            client.zone_switch_group_links.update(LINK_ID, fields)

    assert not get_route.called
    assert not put_route.called


def test_delete_sends_delete(respx_mock: respx.MockRouter, controller_url: str) -> None:
    register_session(respx_mock)
    route = respx_mock.delete(f"{LINKS}/{LINK_ID}").mock(
        return_value=httpx.Response(204)
    )

    with SmartZoneClient(controller_url, "admin", "pw") as client:
        client.zone_switch_group_links.delete(LINK_ID)

    assert route.called
