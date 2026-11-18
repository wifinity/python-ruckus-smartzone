"""Offline tests for the model generator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import generate_models  # noqa: E402


def _write_spec(path: Path, names: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    definitions = {name: {"type": "object"} for name in names}
    path.write_text(json.dumps({"swagger": "2.0", "definitions": definitions}))


def _load(path: Path) -> dict:
    namespace: dict = {}
    exec(compile(path.read_text(), path.name, "exec"), namespace)  # noqa: S102
    return namespace


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    models_dir = tmp_path / "models"
    monkeypatch.setattr(generate_models, "RAW_DIR", raw_dir)
    monkeypatch.setattr(generate_models, "MODELS_DIR", models_dir)
    return raw_dir, models_dir


def test_generates_both_schema_indexes(dirs):
    raw_dir, models_dir = dirs
    _write_spec(raw_dir / "all.json", ["WLAN", "Zone"])
    _write_spec(raw_dir / "switchm.json", ["vlanConfig_VlanConfig"])

    generate_models.main([])

    assert set(_load(models_dir / "schema_index.py")["SCHEMA_INDEX"]) == {
        "WLAN",
        "Zone",
    }
    switchm = _load(models_dir / "switchm_schema_index.py")
    assert set(switchm["SWITCHM_SCHEMA_INDEX"]) == {"vlanConfig_VlanConfig"}
    init = (models_dir / "__init__.py").read_text()
    assert "SCHEMA_INDEX as SCHEMA_INDEX" in init
    assert "SWITCHM_SCHEMA_INDEX as SWITCHM_SCHEMA_INDEX" in init


def test_single_spec_leaves_other_index_alone(dirs):
    raw_dir, models_dir = dirs
    _write_spec(raw_dir / "switchm.json", ["group_switchGroup"])
    models_dir.mkdir(parents=True)
    (models_dir / "schema_index.py").write_text("SCHEMA_INDEX: dict = {}\n")

    generate_models.main(["--spec", "switchm"])

    assert (models_dir / "schema_index.py").read_text() == "SCHEMA_INDEX: dict = {}\n"
    init = (models_dir / "__init__.py").read_text()
    assert "from .schema_index import" in init
    assert "from .switchm_schema_index import" in init


def test_init_skips_missing_modules(dirs):
    raw_dir, models_dir = dirs
    _write_spec(raw_dir / "switchm.json", ["group_switchGroup"])

    generate_models.main(["--spec", "switchm"])

    init = (models_dir / "__init__.py").read_text()
    assert "from .schema_index import" not in init


def test_missing_spec_exits(dirs):
    with pytest.raises(SystemExit):
        generate_models.main(["--spec", "wsg"])
