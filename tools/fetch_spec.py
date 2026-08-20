"""Fetch the Ruckus SmartZone Swagger 2.0 spec and stamp a version manifest.

SmartZone serves a single machine-readable document at
``{base}/wsg/apiDoc/openapi`` (Swagger 2.0, unauthenticated). There is no
separate version endpoint, so the manifest anchors on the spec's own
``info.version`` plus the fetch date, written alongside the raw spec.

Source selection:

* ``--base-url URL`` (or ``SMARTZONE_BASE_URL``): the spec comes from
  ``{base}/wsg/apiDoc/openapi``.
* ``--url URL`` (or ``SMARTZONE_OPENAPI_URL``): explicit spec URL override.

A controller base URL is required; there is no public cloud default. The raw
spec bakes the source controller into its top-level ``host`` field; the fetch
step overwrites it with a host-agnostic placeholder so a private controller
address is never committed and the baseline is identical regardless of which
controller produced it. The SDK supplies the real base URL at runtime.

The fetch step also normalises a few vendor-spec conformance quirks so the
checked-in spec validates: ``type: file`` response schemas become a binary body,
string defaults on numeric/boolean fields are coerced to their type, a default
outside its own ``enum`` is dropped, and ``{name:regex}`` path templates are
reduced to ``{name}``. Legal ``formData`` file parameters are left untouched.
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

SPEC_PATH_SUFFIX = "/wsg/apiDoc/openapi"
USER_AGENT = "python-ruckus-smartzone/0.1.0"

# The controller bakes its own address into the Swagger 2.0 ``host`` field;
# overwrite it with a host-agnostic placeholder so a private controller address
# is never committed. ``basePath`` (the API-version path) and ``schemes`` carry
# no host identity and are kept.
HOST_PLACEHOLDER = "smartzone.example"

RAW_SPEC_PATH = Path("spec/raw/all.json")
MANIFEST_PATH = Path("spec/raw/manifest.json")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the SmartZone Swagger 2.0 spec and stamp a version manifest."
    )
    parser.add_argument(
        "--base-url", help="Controller base URL; the spec path is derived from it."
    )
    parser.add_argument("--url", help="Explicit spec URL override.")
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


def resolve_sources(
    args: argparse.Namespace, env: Mapping[str, str]
) -> tuple[str, str]:
    """Return ``(spec_url, source_kind)``.

    A controller base URL (or explicit spec URL) is required; SmartZone has no
    public cloud spec.
    """
    base = args.base_url or env.get("SMARTZONE_BASE_URL")
    explicit_url = args.url or env.get("SMARTZONE_OPENAPI_URL")

    if base:
        spec_url = f"{_normalize_base(base)}{SPEC_PATH_SUFFIX}"
    elif explicit_url:
        spec_url = explicit_url
    else:
        raise SystemExit(
            "A controller base URL is required: pass --base-url or set SMARTZONE_BASE_URL."
        )
    return spec_url, "controller"


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
    """
    if isinstance(node, dict):
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
      defaults, out-of-enum defaults, ``{name:regex}`` path templates) so the
      checked-in spec validates.
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


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    spec_url, source = resolve_sources(args, os.environ)
    verify = resolve_verify(args, os.environ)

    spec_payload = sanitize_spec(fetch_json(spec_url, verify=verify))
    raw_bytes = (json.dumps(spec_payload, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    RAW_SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_SPEC_PATH.write_bytes(raw_bytes)

    spec_info_version = (spec_payload.get("info") or {}).get("version")
    manifest = build_manifest(
        source=source,
        spec_info_version=spec_info_version,
        spec_sha256=hashlib.sha256(raw_bytes).hexdigest(),
        fetched_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"Fetched spec from {source} -> {RAW_SPEC_PATH}")
    print(
        f"Wrote manifest -> {MANIFEST_PATH} (spec_info_version={manifest['spec_info_version']})"
    )


if __name__ == "__main__":
    main()
