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


def test_validates_every_present_spec(tmp_path, monkeypatch, capsys):
    (tmp_path / "all.json").write_text(json.dumps(MINIMAL_SWAGGER_2))
    (tmp_path / "switchm.json").write_text(json.dumps(MINIMAL_SWAGGER_2))
    monkeypatch.setattr(validate_spec, "RAW_DIR", tmp_path)

    validate_spec.main()  # does not raise on valid documents

    out = capsys.readouterr().out
    assert "all.json" in out and "switchm.json" in out


def test_invalid_switchm_spec_raises(tmp_path, monkeypatch):
    import pytest

    bad = dict(MINIMAL_SWAGGER_2, produces=["application/json", "application/json"])
    (tmp_path / "switchm.json").write_text(json.dumps(bad))
    monkeypatch.setattr(validate_spec, "RAW_DIR", tmp_path)

    with pytest.raises(Exception):
        validate_spec.main()


def test_missing_spec_exits(tmp_path, monkeypatch):
    import pytest

    monkeypatch.setattr(validate_spec, "RAW_DIR", tmp_path / "absent")
    with pytest.raises(SystemExit):
        validate_spec.main()
