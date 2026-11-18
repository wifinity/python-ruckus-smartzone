"""Fetch the Ruckus SmartZone Swagger 2.0 specs and stamp a version manifest.

SmartZone serves two machine-readable documents, both Swagger 2.0 and
unauthenticated:

* ``wsg`` — the public API, at ``{base}/wsg/apiDoc/openapi``, written to
  ``spec/raw/all.json``.
* ``switchm`` — the Switch Manager API, at ``{base}/switchm/api/openapi``,
  written to ``spec/raw/switchm.json``.

There is no separate version endpoint, so the manifest anchors each spec on its
own ``info.version`` plus the fetch date. ``spec/raw/manifest.json`` holds one
entry per spec, keyed by spec name.

Source selection:

* ``--base-url URL`` (or ``SMARTZONE_BASE_URL``): each spec comes from its path
  under the controller root.
* ``--url URL`` (or ``SMARTZONE_OPENAPI_URL``): explicit spec URL override, only
  valid when a single ``--spec`` is selected.
* ``--spec NAME`` (repeatable): fetch only the named specs; all by default.

A controller base URL is required; there is no public cloud default. The raw
spec bakes the source controller into its top-level ``host`` field; the fetch
step overwrites it with a host-agnostic placeholder so a private controller
address is never committed and the baseline is identical regardless of which
controller produced it. The SDK supplies the real base URL at runtime.

The fetch step also normalises a few vendor-spec conformance quirks so the
checked-in spec validates: ``type: file`` response schemas become a binary body,
string defaults on numeric/boolean fields are coerced to their type, a default
outside its own ``enum`` is dropped, ``{name:regex}`` path templates are
reduced to ``{name}``, and repeated ``produces``/``consumes`` entries are
collapsed. Legal ``formData`` file parameters are left untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from urllib.request import Request, urlopen

USER_AGENT = "python-ruckus-smartzone/0.1.0"

# The controller bakes its own address into the Swagger 2.0 ``host`` field;
# overwrite it with a host-agnostic placeholder so a private controller address
# is never committed. ``basePath`` (the API-version path) and ``schemes`` carry
# no host identity and are kept.
HOST_PLACEHOLDER = "smartzone.example"

RAW_DIR = Path("spec/raw")
MANIFEST_PATH = RAW_DIR / "manifest.json"

# Spec name -> (path under the controller root, file name under RAW_DIR).
SPECS: dict[str, tuple[str, str]] = {
    "wsg": ("/wsg/apiDoc/openapi", "all.json"),
    "switchm": ("/switchm/api/openapi", "switchm.json"),
}


def raw_spec_path(name: str) -> Path:
    """Return where the named spec is written."""
    return RAW_DIR / SPECS[name][1]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the SmartZone Swagger 2.0 spec and stamp a version manifest."
    )
    parser.add_argument(
        "--base-url", help="Controller base URL; the spec path is derived from it."
    )
    parser.add_argument(
        "--url", help="Explicit spec URL override (requires a single --spec)."
    )
    parser.add_argument(
        "--spec",
        action="append",
        choices=sorted(SPECS),
        help="Spec to fetch; repeatable. Defaults to every spec.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS verification (self-signed controllers).",
    )
    return parser.parse_args(argv)


def _normalize_base(base_url: str) -> str:
    resolved = base_url.rstrip("/")
    if not resolved:
        raise ValueError("base_url is required")
    return resolved


def selected_specs(args: argparse.Namespace) -> list[str]:
    """Return the spec names to fetch, in ``SPECS`` order."""
    chosen = set(args.spec or SPECS)
    return [name for name in SPECS if name in chosen]


def resolve_sources(args: argparse.Namespace, env: Mapping[str, str]) -> dict[str, str]:
    """Return ``{spec_name: spec_url}`` for the selected specs.

    A controller base URL (or explicit spec URL) is required; SmartZone has no
    public cloud spec. An explicit URL names one document, so it needs exactly
    one ``--spec``.
    """
    names = selected_specs(args)
    base = args.base_url or env.get("SMARTZONE_BASE_URL")
    explicit_url = args.url or env.get("SMARTZONE_OPENAPI_URL")

    if base:
        root = _normalize_base(base)
        return {name: f"{root}{SPECS[name][0]}" for name in names}
    if explicit_url:
        if len(names) != 1:
            raise SystemExit("--url names one spec: pass exactly one --spec with it.")
        return {names[0]: explicit_url}
    raise SystemExit(
        "A controller base URL is required: pass --base-url or set SMARTZONE_BASE_URL."
    )


def resolve_verify(args: argparse.Namespace, env: Mapping[str, str]) -> bool:
    if args.insecure:
        return False
    value = env.get("SMARTZONE_VERIFY")
    if value is not None:
        return value.strip().lower() not in {"0", "false", "no", "off"}
    return True


def _load_url(url: str, *, verify: bool = True) -> bytes:
    context = None if verify else ssl._create_unverified_context()
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(
        request, timeout=60, context=context
    ) as response:  # nosec B310 - configurable controller endpoint
        return response.read()


def fetch_json(url: str, *, verify: bool = True) -> dict:
    return json.loads(_load_url(url, verify=verify).decode("utf-8"))


def _coerce_default(node: dict) -> None:
    """Coerce a string ``default`` to the field's declared numeric/boolean type.

    The controller encodes some defaults as strings (e.g. ``"false"`` on a
    ``boolean`` field, ``"514"`` on an ``integer`` field). Coerce them to the
    declared type so the default matches its schema.
    """
    declared = node.get("type")
    value = node.get("default")
    if not isinstance(value, str):
        return
    if declared == "boolean":
        lowered = value.strip().lower()
        if lowered == "true":
            node["default"] = True
        elif lowered == "false":
            node["default"] = False
    elif declared == "integer":
        if re.fullmatch(r"-?\d+", value.strip()):
            node["default"] = int(value)
    elif declared == "number":
        try:
            node["default"] = float(value)
        except ValueError:
            pass


def _dedupe_lists(node: dict) -> None:
    """Collapse repeated MIME entries and repeated (name, in) parameters."""
    for key in ("produces", "consumes"):
        mimes = node.get(key)
        if isinstance(mimes, list) and all(isinstance(m, str) for m in mimes):
            node[key] = list(dict.fromkeys(mimes))
    params = node.get("parameters")
    if not isinstance(params, list):
        return
    seen: set[tuple] = set()
    unique = []
    for param in params:
        if isinstance(param, dict) and "name" in param:
            ident = (param.get("name"), param.get("in"))
            if ident in seen:
                continue
            seen.add(ident)
        unique.append(param)
    node["parameters"] = unique


def _normalize_schema_nodes(node: object) -> None:
    """Normalise vendor-spec schema quirks so the document validates.

    - ``type: file`` in a schema object (a binary download response) is not a
      valid Swagger 2.0 type, so it becomes ``{"type": "string", "format":
      "binary"}``. ``formData`` parameters, which carry an ``in`` field and where
      ``type: file`` is valid, are left untouched.
    - A string ``default`` on a numeric/boolean field is coerced to its type.
    - A ``default`` that is not one of its own ``enum`` values is dropped.
    - A ``{name:regex}`` regex suffix is stripped from an ``in: path`` parameter
      name so it matches the normalised path template.
    - Repeated entries in a ``produces``/``consumes`` MIME list are collapsed,
      keeping the first of each.
    - A parameter repeated with the same ``name`` and ``in`` in one
      ``parameters`` list is collapsed, keeping the first.
    """
    if isinstance(node, dict):
        _dedupe_lists(node)
        if node.get("type") == "file" and "in" not in node:
            node["type"] = "string"
            node["format"] = "binary"
        if (
            node.get("in") == "path"
            and isinstance(node.get("name"), str)
            and ":" in node["name"]
        ):
            node["name"] = node["name"].split(":", 1)[0]
        _coerce_default(node)
        enum = node.get("enum")
        if isinstance(enum, list) and "default" in node and node["default"] not in enum:
            del node["default"]
        for value in list(node.values()):
            _normalize_schema_nodes(value)
    elif isinstance(node, list):
        for item in node:
            _normalize_schema_nodes(item)


def _normalize_path_templates(spec: dict) -> None:
    """Rewrite ``{name:regex}`` path templates to plain ``{name}``.

    The controller uses routing-framework regex path templates (e.g.
    ``/cluster/{id:.+}``); OpenAPI reads the ``:regex`` suffix as part of the
    parameter name, so it no longer matches the declared ``id`` parameter.
    """
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        return
    for key in list(paths.keys()):
        rewritten = re.sub(r"\{([^{}:]+):[^{}]*\}", r"{\1}", key)
        if rewritten != key:
            paths[rewritten] = paths.pop(key)


def sanitize_spec(spec: dict) -> dict:
    """Prepare the fetched spec for commit.

    - Overwrite the top-level ``host`` so no source host/IP is written.
    - Normalise vendor-spec conformance quirks (binary response bodies, typed
      defaults, out-of-enum defaults, ``{name:regex}`` path templates, repeated
      MIME entries and parameters) so the checked-in spec validates.
    """
    if "host" in spec:
        spec["host"] = HOST_PLACEHOLDER
    _normalize_path_templates(spec)
    _normalize_schema_nodes(spec)
    return spec


def build_manifest(
    *, source: str, spec_info_version: str | None, spec_sha256: str, fetched_at: str
) -> dict:
    return {
        "source": source,
        "spec_info_version": spec_info_version,
        "spec_sha256": spec_sha256,
        "fetched_at": fetched_at,
    }


def load_manifest(path: Path) -> dict:
    """Return the manifest keyed by spec name.

    A single-spec manifest (top-level ``source`` key) is read as the ``wsg``
    entry.
    """
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if "source" in data:
        return {"wsg": data}
    return data


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    sources = resolve_sources(args, os.environ)
    verify = resolve_verify(args, os.environ)

    manifest = load_manifest(MANIFEST_PATH)
    for name, spec_url in sources.items():
        spec_payload = sanitize_spec(fetch_json(spec_url, verify=verify))
        raw_bytes = (json.dumps(spec_payload, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
        raw_path = raw_spec_path(name)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw_bytes)

        manifest[name] = build_manifest(
            source="controller",
            spec_info_version=(spec_payload.get("info") or {}).get("version"),
            spec_sha256=hashlib.sha256(raw_bytes).hexdigest(),
            fetched_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        print(
            f"Fetched {name} spec -> {raw_path} "
            f"(spec_info_version={manifest[name]['spec_info_version']})"
        )

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Wrote manifest -> {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
