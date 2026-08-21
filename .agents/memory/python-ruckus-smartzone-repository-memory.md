# python-ruckus-smartzone Repository Memory

## 1) Purpose and Overview

`python-ruckus-smartzone` is a Python client library for the Ruckus SmartZone
(virtual SmartZone / vSZ) public REST API. It targets API version `v13_1` and
provides a typed, resource-oriented wrapper over the endpoints needed to manage
zones, WLANs, WLAN groups (and their members), access points, and AP groups (and
their members).

A single client object owns an `httpx` session and composes resource objects. The
public API is dict-first.

## 2) Current state

In place:

- Package skeleton (`ruckus_smartzone/`) with version and public exports.
- Exception hierarchy (`SmartZoneAPIError` and subclasses, plus
  `SmartZoneRateLimitError`/`SmartZoneBusyError`) with `raise_for_response()`
  mapping HTTP status and vendor `errorCode` 211 (403 → not found).
- Logging configuration: log-level control, sensitive-header masking, and
  `mask_url()` redacting the `serviceTicket` query parameter.
- `SmartZoneClient` (`client.py`): synchronous `httpx` transport, low-level verbs,
  `paginate()`, 429 and controller-busy backoff, and context-manager lifecycle.
- Service-ticket auth (`auth.py` + `ticket_cache.py`): acquire, reuse, refresh on
  401, release on close, behind the pluggable `TicketCache` seam
  (`InMemoryTicketCache` only).
- Spec-driven pipeline (`tools/`, `spec/`, `ruckus_smartzone/generated/`).
- Build/test tooling: `pyproject.toml`, `Makefile`, `.flake8`, CI workflow.
- Test harness: `pytest` + `respx` for HTTP isolation.
- Resource wrappers for zones, WLANs, and WLAN groups with their members
  (`ruckus_smartzone/resources/`, reached as `client.zones`, `client.wlans`,
  `client.wlan_groups`), plus client-side WLAN-group name validation
  (`validation.py`). See ADR 0003 for the design and live verification.
- Access-point resource wrapper (`resources/access_points.py`, reached as
  `client.access_points`): list/get/create/update/replace/delete,
  `operational_summary`, bulk `query` (POST `/query/ap`, page/limit paging), and a
  chunked `move` returning per-batch `MoveResult`. A MAC module (`mac.py`,
  `normalize_mac`) validates and normalises to colon-uppercase. `move`/`update`/
  `replace` take an optional `expected_zone_id` pre-flight guard that raises
  `SmartZoneZoneMismatchError` before any write. See ADR 0004.
- AP-group resource wrapper (`resources/ap_groups.py`, reached as
  `client.ap_groups`): list/get/get_default/create/update/replace/delete,
  `find_by_name`/`upsert_by_name`, `add_member`/`remove_member`, and
  `set_radio_wlan_group`/`clear_radio_wlan_group` for the per-radio WLAN-group
  overrides. `create`/`update`/`replace` mirror the zone wrapper's dict-first
  PATCH-partial / PUT-full split; names reuse `validate_group_name`. Placement
  (`access_points.move`) and group switching are kept separate: `add_member`
  refuses an AP not already in the group's zone. See ADR 0005.

Live verification of the AP-group layer is complete (physical test AP, `v13_1`
controller): CRUD, the radio-override round-trip, and membership all confirmed;
`add_member` auto-removes an AP from its previous group (one AP group per zone)
and the zone guard refuses a cross-zone AP; a partial `PUT` is rejected (HTTP 500
on the missing required `name`); and `create` is zone-dependent (a minimal body
succeeds in some zones and 500s in others by AP firmware/template). See ADR 0005.

Live verification of the AP layer is complete (physical test AP, `v13_1`
controller): `move` is the adoption trigger and propagates to
`operational/summary` in under two seconds each way, the pre-flight zone guard
fires, the `query` paginator walks the full inventory, and `delete` is the only
operation that frees an AP's capacity license — see ADR 0004. See ADR 0002 for the
auth/session/transport design and its live verification (logon, multi-page AP
pagination, URL masking, and release-on-close all confirmed; the controller-busy
signal remains an assumption keyed on HTTP 423/503).

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
- `POST /aps/move` is capped at 50 MACs per call; `targetZoneId` is required even
  when moving to an AP group (`targetApGroupId`).
- `POST /query/ap` returns bulk AP state and pages by `page`/`limit` in the POST
  body (not the GET `index`/`listSize`), over the same `{totalCount, hasMore,
  firstIndex, list}` shape.
- `GET /aps/{apMac}` returns the AP config including its `zoneId`, which the
  pre-flight zone guard reads.
- MAC addresses are colon-separated uppercase (e.g. `8C:0C:90:2B:8B:90`).
- AP groups live under `/rkszones/{zoneId}/apgroups` (with a `/default` sibling).
  Each group carries a `radioConfig` whose `radio{24g,5g,5gLower,5gUpper,6g}`
  entries hold a `wlanGroupId`; a radio override is set through the group PATCH
  and cleared via `DELETE …/apgroups/{id}/radioConfig/{radio}/wlanGroupId`.
- AP-group membership is `POST`/`DELETE …/apgroups/{id}/members/{apMac}`, keyed on
  the global AP MAC namespace (like `POST /aps/move`); an AP belongs to one AP
  group per zone, so adding it to a group removes it from its previous one.
- AP-group name is `common_normalName` (2-32 printable, no leading/trailing
  space), the same constraint as zone and WLAN-group names.
- AP-group `PUT` is a full-object replace (partial body rejected); `create`
  body requirements vary by zone/AP-firmware, so a minimal body is not portable.

## 5) Conventions

- Distribution name `ruckus-smartzone`; import name `ruckus_smartzone`.
- Public methods and resource wrappers return `dict` payloads from the API.
- All errors derive from `SmartZoneAPIError` with `status_code` and
  `response_data` attributes.
- The pinned API version lives as a single constant in the transport layer.
- **Keep `README.md` current.** Any change to public functionality (new client
  methods, constructor arguments, exceptions, or behaviour) updates the
  `README.md` usage sections in the same change.
- **This is a public repository.** Docs must not name internal hosts, IP
  addresses, credentials, other repositories, ticket systems, or any
  organisation-specific infrastructure. Use placeholders (e.g.
  `controller.example`) in examples and verification notes.

## 6) Testing

- `make tests` runs `lint` (flake8 + black check), `type-check` (mypy), and
  `unit-tests` (pytest).
- HTTP is isolated with `respx`; the pipeline tools are tested offline with inline
  spec fixtures and monkeypatched path constants — no test performs real network
  I/O and no controller is required.
