# 0001. API version to pin and controller spec availability

Date: 2026-08-20
Status: Accepted

## Context

`python-ruckus-smartzone` is a Python client library for the Ruckus SmartZone
(vSZ) public API. Two questions had to be settled against a live controller
before any client code is written, because both shape how the SDK is built:

1. Which API versions does the controller serve, and which one does the SDK pin?
2. Does the controller expose a machine-readable spec (Swagger/OpenAPI)? If it
   does, model metadata can be generated from it; if not, resources are written
   by hand.

Both were answered by reading a production controller directly rather than
trusting the 7.1.1 reference guide. The vendor's `dev` instance runs vSZ 6 and
does not serve `v13_1`, so a production controller is the only usable
verification target. Its address is supplied at runtime and is **not recorded in
this repository**.

### Live reads (2026-08-20)

`GET {base}/wsg/api/public/apiInfo` (identical on both cluster nodes):

```json
{"apiSupportVersions":["v11_0","v11_1","v12_0","v13_0","v13_1"]}
```

`POST {base}/wsg/api/public/v13_1/serviceTicket` succeeded, returning
`{"controllerVersion":"7.1.1.0.551", ...}` — a live `v13_1` session, not just a
version listed in `apiInfo`.

`GET {base}/wsg/api/public/v13_1/controller` reports a two-node vSZ-H cluster
(Leader + Follower), both running:

- SmartZone software version `7.1.1.0.551`
- AP version `7.1.1.0.830`

Spec probe — the controller **does** serve a machine-readable spec, at
`/wsg/apiDoc/openapi`:

| Path | Result |
|------|--------|
| `/wsg/apiDoc/openapi` | **200**, Swagger 2.0 JSON, ~1.6 MB, unauthenticated |
| `/wsg/apiDoc/` | 200, HTML (Swagger-UI index) |
| `/wsg/api/public/swagger.json`, `/openapi.json`, `/wsg/api/public/v13_1/swagger.json`, `.../openapi.json` | 404 |
| `/wsg/api/public/api-docs`, `/wsg/api/public/v13_1/api-docs` | 404 |
| `/wsg/apiDoc/openapi.json`, `/wsg/apiDoc/swagger.json`, `/v2/api-docs`, `/swagger-ui.html`, `/apidocs` | 404 |

The document at `/wsg/apiDoc/openapi` is a valid Swagger 2.0 (OpenAPI 2) spec:

- `info.version: v13_1`, `title: Virtual SmartZone - High Scale`,
  `basePath: /wsg/api/public/v13_1`.
- **712 paths, 1116 operations, 977 definitions.**
- Covers the full SDK surface: 234 `rkszones/…` paths, 49 `wlan…`, 16
  `wlangroup…`, 95 `aps…`, 72 `apgroups…`, plus `serviceTicket`, `session`, and
  `query/ap`.
- The document embeds the source controller's `host`; this is stripped on fetch
  (see below), so no controller address is committed.

## Decision

### Pin API version `v13_1`

The SDK targets `v13_1`, confirmed served (a live service ticket was issued on
it). `v11_1` remains served, alongside `v11_0`, `v12_0`, and `v13_0`, so clients
pinned to an older version keep working while this SDK is built on `v13_1`.

### Version anchor

Everything the SDK is verified against is stamped with the SmartZone version
triple:

- **SmartZone software version:** `7.1.1.0.551` (vSZ-H)
- **API version:** `v13_1`
- **AP version (observed):** `7.1.1.0.830`

### Machine-readable spec is available — generate models from it

The controller serves a complete Swagger 2.0 document at `/wsg/apiDoc/openapi`
(unauthenticated). The SDK generates model metadata from that spec rather than
hand-writing resource models. The toolchain (in `tools/`) is:

- `fetch_spec.py` — download `/wsg/apiDoc/openapi`, sanitise the `host` field
  (below), and write `spec/raw/all.json` plus a version manifest.
- `generate_models.py` — read the spec's `definitions` and write a committed
  schema index under `ruckus_smartzone/generated/`.
- `validate_spec.py` — validate the fetched spec.

Two SmartZone-specific properties of the spec:

- It is **Swagger 2.0** (OpenAPI 2), not OpenAPI 3. The tooling handles Swagger 2
  natively — the host lives in the top-level `host` field, and schemas live under
  `definitions` (not `components.schemas`). No 2.0 → 3.0 conversion is performed.
- The document bakes the source `host` into that top-level `host` field. The fetch
  step overwrites it with a host-agnostic placeholder, so the checked-in spec
  carries no controller address and is identical regardless of which controller
  produced it. The SDK supplies the real base URL at runtime.

The published spec has a small set of conformance defects, so the fetch step
normalises them in place (meaning-preserving) rather than committing an invalid
document:

- `type: file` response schemas become `{"type": "string", "format": "binary"}`
  (`type: file` is valid only on `formData` parameters, which are left untouched).
- String `default`s on `boolean`/`integer`/`number` fields are coerced to their
  declared type.
- A `default` that is not one of its own `enum` values is dropped.
- `{name:regex}` path templates — and the matching `in: path` parameter names —
  are reduced to `{name}`.

This normalisation is part of the fetch step, not a separate patch stage; the
checked-in spec validates as a result.

### This is a public repository — no local infrastructure in git

No controller address, hostname, cluster node name, MAC, serial, or credential is
committed. The controller address is supplied at fetch/run time via the
`--base-url` flag or the `SMARTZONE_BASE_URL` environment variable, never stored.
Publishable version facts (SmartZone software version, API version) are recorded,
but nothing that identifies or locates the controller.

## Consequences

- The repo scaffolds a **spec-driven** client: a `fetch_spec` step that pulls
  `/wsg/apiDoc/openapi` from a runtime-supplied base URL and sanitises the `host`
  field, a `generate_models` step, and a `validate_spec` step. The unit suite
  (`make tests`) exercises these tools offline with inline spec fixtures; the live
  fetch is an operator step run against a controller.
- The fetched spec and its manifest are stamped with the version anchor
  (`7.1.1.0.551` / `v13_1`) via a manifest recording `source`,
  `spec_info_version`, `spec_sha256`, and `fetched_at` — never the host. A spec
  refresh re-runs the fetch and re-stamps.
- The pinned version `v13_1` lives as a single constant in the transport layer.
- The version anchor is the baseline that later verification records against. A
  compatibility matrix, if kept, uses these fields as its columns (the sanitised
  public subset only).
- No separate conformance suite is planned; verification is live checks against a
  production controller as behaviours are added.
