"""Offline tests for the spec validator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_spec  # noqa: E402

MINIMAL_SWAGGER_2 = {
    "swagger": "2.0",
    "info": {"title": "Virtual SmartZone - High Scale", "version": "v13_1"},
    "paths": {},
}


def test_validates_minimal_swagger2(tmp_path, monkeypatch):
    raw = tmp_path / "all.json"
    raw.write_text(json.dumps(MINIMAL_SWAGGER_2))
    monkeypatch.setattr(validate_spec, "RAW_SPEC_PATH", raw)

    validate_spec.main()  # does not raise on a valid document


def test_missing_spec_exits(tmp_path, monkeypatch):
    import pytest

    monkeypatch.setattr(validate_spec, "RAW_SPEC_PATH", tmp_path / "absent.json")
    with pytest.raises(SystemExit):
        validate_spec.main()
