"""Tests for MAC normalisation."""

import pytest

from ruckus_smartzone.mac import normalize_mac

CANONICAL = "8C:0C:90:2B:8B:90"


@pytest.mark.parametrize(
    "value",
    [
        "8C:0C:90:2B:8B:90",
        "8c:0c:90:2b:8b:90",
        "8C-0C-90-2B-8B-90",
        "8c-0c-90-2b-8b-90",
        "8c0c.902b.8b90",
        "8C0C902B8B90",
        "8c0c902b8b90",
        "  8C:0C:90:2B:8B:90  ",
    ],
)
def test_normalizes_accepted_forms_to_colon_uppercase(value: str) -> None:
    assert normalize_mac(value) == CANONICAL


@pytest.mark.parametrize(
    "value",
    [
        "",
        "8C:0C:90:2B:8B",  # too short
        "8C:0C:90:2B:8B:90:11",  # too long
        "8C:0C:90:2B:8B:9G",  # non-hex
        "8C0C902B8B9",  # 11 hex digits
        "8C0C902B8B900",  # 13 hex digits
        "8C:0C-90:2B:8B:90",  # mixed separators
        "not-a-mac",
    ],
)
def test_rejects_malformed_input(value: str) -> None:
    with pytest.raises(ValueError):
        normalize_mac(value)


def test_rejects_non_string() -> None:
    with pytest.raises(ValueError):
        normalize_mac(None)  # type: ignore[arg-type]
