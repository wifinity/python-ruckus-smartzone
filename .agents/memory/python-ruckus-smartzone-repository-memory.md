# python-ruckus-smartzone Repository Memory

## 1) Purpose and Overview

`python-ruckus-smartzone` is a Python client library for the Ruckus SmartZone
(virtual SmartZone / vSZ) public REST API. It targets API version `v13_1` and
provides a typed, resource-oriented wrapper over the endpoints needed to manage
zones, WLANs, WLAN groups (and their members), and access points.

A single client object owns an `httpx` session and composes resource objects. The
public API is dict-first.

## 2) Current state

Early scaffold. In place:

- Package skeleton (`ruckus_smartzone/`) with version and public exports.
- Exception hierarchy (`SmartZoneAPIError` and subclasses).
- Logging configuration (log-level control, sensitive-header masking).
- Spec-driven pipeline (`tools/`, `spec/`, `ruckus_smartzone/generated/`).
- Build/test tooling: `pyproject.toml`, `Makefile`, `.flake8`, CI workflow.
- Test harness: `pytest` + `respx` for HTTP isolation.

Not yet implemented: the HTTP client, authentication/session lifecycle,
transport resilience, and the zone/WLAN/AP resource wrappers.

## 3) Spec-driven pipeline

The controller serves a Swagger 2.0 document at `/wsg/apiDoc/openapi` (~1.6 MB,
unauthenticated). Models are generated from it, not hand-written:

- `tools/fetch_spec.py` — download the spec, overwrite its `host` with a
  placeholder (no controller address is ever committed), and write
  `spec/raw/all.json` + `spec/raw/manifest.json`. A controller base URL is
  supplied at fetch time via `--base-url` / `SMARTZONE_BASE_URL`; never stored.
- `tools/generate_models.py` — read `spec/raw/all.json` `definitions` and write a
  committed schema index under `ruckus_smartzone/generated/models/`.
- `tools/validate_spec.py` — validate `spec/raw/all.json`.

The spec is Swagger 2.0 (OpenAPI 2), handled natively — `host` is the top-level
field stripped on fetch, and `definitions` is the schema block. The fetch step
also normalises a defined set of vendor conformance quirks in place so the
checked-in spec validates: `type: file` response schemas → binary bodies, string
defaults on numeric/boolean fields coerced to type, out-of-enum defaults dropped,
and `{name:regex}` path templates (and their parameter names) reduced to
`{name}`. There is no separate patch stage. `spec/raw/` is empty until a spec is
fetched from a controller.

## 4) API notes (SmartZone vSZ, API v13_1)

Version anchor: SmartZone software `7.1.1.0.551` (vSZ-H) + API `v13_1`
(observed AP firmware `7.1.1.0.830`).

- Authentication uses a **service ticket**: log on to obtain a ticket, pass it on
  subsequent calls, and log off to release it. Tickets are long-lived (about 24
  hours) and are intended to be reused across calls.
- Pagination uses `index` / `listSize` (default 100, max 1000); list responses
  have the shape `{totalCount, hasMore, firstIndex, list}`.
- WLAN and WLAN-group writes are scoped under `/rkszones/{zoneId}/...`.
- WLAN groups have no `PUT`; the group object is created with `POST` and updated
  with `PATCH` accepting only `{name, description}`. Membership is managed through
  a separate `/members` sub-resource.
- `POST /aps/move` is capped at 50 MACs per call and accepts a target zone or AP
  group.
- MAC addresses are colon-separated uppercase (e.g. `8C:0C:90:2B:8B:90`).

## 5) Conventions

- Distribution name `ruckus-smartzone`; import name `ruckus_smartzone`.
- Public methods and resource wrappers return `dict` payloads from the API.
- All errors derive from `SmartZoneAPIError` with `status_code` and
  `response_data` attributes.
- The pinned API version lives as a single constant in the transport layer.

## 6) Testing

- `make tests` runs `lint` (flake8 + black check), `type-check` (mypy), and
  `unit-tests` (pytest).
- HTTP is isolated with `respx`; the pipeline tools are tested offline with inline
  spec fixtures and monkeypatched path constants — no test performs real network
  I/O and no controller is required.
