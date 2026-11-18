"""Offline tests for the spec fetch tool (no live controller)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import fetch_spec  # noqa: E402

CONTROLLER = "https://192.0.2.10:8443"  # TEST-NET-1, never a real controller

SPEC_PAYLOAD = {
    "swagger": "2.0",
    "info": {"title": "Virtual SmartZone - High Scale", "version": "v13_1"},
    "host": "192.0.2.10:8443",
    "basePath": "/wsg/api/public/v13_1",
    "schemes": ["https"],
    "definitions": {
        "WLAN": {
            "type": "object",
            "properties": {
                "enabled": {"type": "boolean", "default": "false"},
                "port": {"type": "integer", "default": "514"},
                "mode": {
                    "type": "string",
                    "enum": ["INCLUDE", "EXCLUDE"],
                    "default": "AND",
                },
            },
        }
    },
    "paths": {
        "/download": {"get": {"responses": {"200": {"schema": {"type": "file"}}}}},
        "/upload": {
            "post": {"parameters": [{"name": "f", "in": "formData", "type": "file"}]}
        },
        "/cluster/{id:.+}": {
            "delete": {
                "parameters": [
                    {"name": "id:.+", "in": "path", "required": True, "type": "string"}
                ],
                "responses": {"200": {"description": "ok"}},
            }
        },
    },
}


def _fake_loader(calls: list[str]):
    def _load(url: str, *, verify: bool = True) -> bytes:
        calls.append(url)
        return json.dumps(SPEC_PAYLOAD).encode("utf-8")

    return _load


def _redirect_outputs(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    manifest = raw_dir / "manifest.json"
    monkeypatch.setattr(fetch_spec, "RAW_DIR", raw_dir)
    monkeypatch.setattr(fetch_spec, "MANIFEST_PATH", manifest)
    return raw_dir / "all.json", manifest


def test_host_is_sanitized(tmp_path, monkeypatch):
    calls: list[str] = []
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader(calls))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    spec = json.loads(raw.read_text())
    assert spec["host"] == fetch_spec.HOST_PLACEHOLDER
    assert calls == [f"{CONTROLLER}/wsg/apiDoc/openapi"]


def test_manifest_fields(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    _, manifest = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    data = json.loads(manifest.read_text())["wsg"]
    assert data["source"] == "controller"
    assert data["spec_info_version"] == "v13_1"
    assert len(data["spec_sha256"]) == 64


def test_outputs_do_not_leak_controller_host(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, manifest = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    assert "192.0.2.10" not in raw.read_text()
    assert "192.0.2.10" not in manifest.read_text()


def test_raw_bytes_are_deterministic(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])
    first = raw.read_bytes()
    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    assert raw.read_bytes() == first


def test_file_response_schema_is_normalized(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    spec = json.loads(raw.read_text())
    download = spec["paths"]["/download"]["get"]["responses"]["200"]["schema"]
    assert download == {"type": "string", "format": "binary"}
    # A formData file parameter is left untouched (valid Swagger 2.0).
    param = spec["paths"]["/upload"]["post"]["parameters"][0]
    assert param["type"] == "file"


def test_typed_defaults_and_enum_defaults_are_normalized(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    props = json.loads(raw.read_text())["definitions"]["WLAN"]["properties"]
    assert props["enabled"]["default"] is False
    assert props["port"]["default"] == 514
    # A default outside its own enum is dropped.
    assert "default" not in props["mode"]


def test_regex_path_template_is_normalized(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "wsg"])

    paths = json.loads(raw.read_text())["paths"]
    assert "/cluster/{id}" in paths
    assert "/cluster/{id:.+}" not in paths
    # The regex suffix is stripped from the path parameter name too.
    assert paths["/cluster/{id}"]["delete"]["parameters"][0]["name"] == "id"


def test_base_url_required(monkeypatch):
    monkeypatch.delenv("SMARTZONE_BASE_URL", raising=False)
    monkeypatch.delenv("SMARTZONE_OPENAPI_URL", raising=False)

    with pytest.raises(SystemExit):
        fetch_spec.main([])


def test_fetches_every_spec_by_default(tmp_path, monkeypatch):
    calls: list[str] = []
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader(calls))
    raw, manifest = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--base-url", CONTROLLER])

    assert calls == [
        f"{CONTROLLER}/wsg/apiDoc/openapi",
        f"{CONTROLLER}/switchm/api/openapi",
    ]
    switchm = raw.parent / "switchm.json"
    assert json.loads(switchm.read_text())["host"] == fetch_spec.HOST_PLACEHOLDER
    assert "192.0.2.10" not in switchm.read_text()
    assert set(json.loads(manifest.read_text())) == {"wsg", "switchm"}


def test_single_spec_keeps_other_manifest_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader([]))
    raw, manifest = _redirect_outputs(tmp_path, monkeypatch)
    manifest.parent.mkdir(parents=True)
    legacy = {
        "source": "controller",
        "spec_info_version": "v13_1",
        "spec_sha256": "a" * 64,
        "fetched_at": "2026-01-01T00:00:00Z",
    }
    manifest.write_text(json.dumps(legacy))

    fetch_spec.main(["--base-url", CONTROLLER, "--spec", "switchm"])

    data = json.loads(manifest.read_text())
    assert data["wsg"] == legacy
    assert data["switchm"]["spec_info_version"] == "v13_1"
    assert not raw.exists()


def test_explicit_url_needs_one_spec(monkeypatch):
    monkeypatch.delenv("SMARTZONE_BASE_URL", raising=False)

    with pytest.raises(SystemExit):
        fetch_spec.main(["--url", "https://192.0.2.10/spec"])


def test_explicit_url_with_one_spec(tmp_path, monkeypatch):
    monkeypatch.delenv("SMARTZONE_BASE_URL", raising=False)
    calls: list[str] = []
    monkeypatch.setattr(fetch_spec, "_load_url", _fake_loader(calls))
    raw, _ = _redirect_outputs(tmp_path, monkeypatch)

    fetch_spec.main(["--url", "https://192.0.2.10/spec", "--spec", "switchm"])

    assert calls == ["https://192.0.2.10/spec"]
    assert (raw.parent / "switchm.json").exists()


def test_repeated_mimes_and_parameters_are_collapsed():
    spec = {
        "paths": {
            "/group/{id}": {
                "patch": {
                    "produces": ["application/json", "application/json"],
                    "parameters": [
                        {"name": "serviceTicket", "in": "query", "type": "string"},
                        {"name": "serviceTicket", "in": "query", "type": "string"},
                        {"name": "id", "in": "path", "type": "string"},
                        {"$ref": "#/parameters/shared"},
                    ],
                }
            }
        }
    }

    op = fetch_spec.sanitize_spec(spec)["paths"]["/group/{id}"]["patch"]

    assert op["produces"] == ["application/json"]
    assert [p.get("name") for p in op["parameters"]] == ["serviceTicket", "id", None]
