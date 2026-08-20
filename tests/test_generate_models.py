"""Offline tests for the model generator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import generate_models  # noqa: E402


def test_generates_schema_index(tmp_path, monkeypatch):
    raw = tmp_path / "raw" / "all.json"
    raw.parent.mkdir(parents=True)
    raw.write_text(
        json.dumps(
            {
                "swagger": "2.0",
                "definitions": {"WLAN": {"type": "object"}, "Zone": {"type": "object"}},
            }
        )
    )
    models_dir = tmp_path / "models"
    monkeypatch.setattr(generate_models, "RAW_SPEC_PATH", raw)
    monkeypatch.setattr(generate_models, "MODELS_DIR", models_dir)
    monkeypatch.setattr(generate_models, "MODELS_FILE", models_dir / "schema_index.py")

    generate_models.main()

    content = (models_dir / "schema_index.py").read_text()
    assert "SCHEMA_INDEX" in content

    namespace: dict = {}
    exec(compile(content, "schema_index.py", "exec"), namespace)  # noqa: S102
    assert set(namespace["SCHEMA_INDEX"].keys()) == {"WLAN", "Zone"}


def test_missing_spec_exits(tmp_path, monkeypatch):
    import pytest

    monkeypatch.setattr(generate_models, "RAW_SPEC_PATH", tmp_path / "absent.json")
    with pytest.raises(SystemExit):
        generate_models.main()
