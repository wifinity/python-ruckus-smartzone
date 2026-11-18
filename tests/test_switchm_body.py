"""Tests for Switch Manager write-body building."""

import pytest

from ruckus_smartzone.switchm.base import (
    AUTHENTICATION_TYPES,
    build_body,
    check_authentication_type,
    join_macs,
)


def test_drops_none_and_keeps_set_fields() -> None:
    body = build_body(
        "portSettings_UpdatePortSettings",
        {"portName": "uplink", "poeEnabled": False, "lldpQosList": None},
    )

    assert body == {"portName": "uplink", "poeEnabled": False}


def test_unknown_field_is_refused() -> None:
    with pytest.raises(ValueError, match="createdTime"):
        build_body(
            "portSettings_UpdatePortSettings", {"portName": "x", "createdTime": 1}
        )


def test_get_body_is_refused() -> None:
    get_body = {"id": "p1", "port": "1/1/1", "switchId": "AA", "portName": "x"}

    with pytest.raises(ValueError):
        build_body("portSettings_UpdatePortSettings", get_body)


def test_authentication_types_are_the_accepted_values() -> None:
    assert AUTHENTICATION_TYPES == ("802.1x", "macauth", "802.1x_and_macauth")
    for value in AUTHENTICATION_TYPES:
        check_authentication_type({"authenticationType": value})
    check_authentication_type({})


@pytest.mark.parametrize("value", ["802.1X", "dot1x", "MACAUTH", ""])
def test_other_authentication_types_are_refused(value: str) -> None:
    with pytest.raises(ValueError):
        check_authentication_type({"authenticationType": value})


def test_join_macs_normalises_and_joins() -> None:
    assert join_macs(["020000aabb01", "02-00-00-AA-BB-02"]) == (
        "02:00:00:AA:BB:01,02:00:00:AA:BB:02"
    )
    assert join_macs("0200.00aa.bb01") == "02:00:00:AA:BB:01"
    with pytest.raises(ValueError):
        join_macs([])
