# 0008. Switch Manager (switchm) spec and client surface

Date: 2026-11-18
Status: Proposed

## Context

SmartZone manages Ruckus ICX switches through a separate service, the Switch
Manager ("switchm"). It has its own REST API and its own spec. The `wsg` spec
the SDK generates from today (ADR 0001) has almost no switch endpoints, so
switch support needs a second spec.

Facts read from a production `7.1.1.0.551` controller on 2026-11-18:

- **Base path** `/switchm/api/v13_1`. The API version follows the SmartZone
  version matrix (`v11_0` … `v13_1` on 7.1.1), the same as `wsg`.
- **Spec** at `GET /switchm/api/openapi`: Swagger 2.0, unauthenticated,
  `info.title: Switch Manager`, `info.version: v13_1`,
  `basePath: /switchm/api/v13_1`. 156 paths, 238 operations, 290 definitions.
  The HTML reference at `/switchm/api/doc` covers the same operations.
- **Auth.** The `wsg` service ticket works unchanged. It rides as the
  `serviceTicket` query parameter on every switchm call. There is no switchm
  logon.
- **Queries are POSTs.** Lists use `POST …/query` (or `POST /switch`,
  `POST /switchconfig`, `POST /job`) with a `{filters, extraFilters, page,
  limit}` body. The valid filter `type` differs by endpoint. For example, port
  settings and VLANs filter on `filters[].type = switchId`, while jobs need
  `extraFilters[].type = SWITCH`. An unknown filter type is a 422 that lists
  the accepted enum.
- **Response envelopes vary.** Most lists return `{totalCount, hasMore,
  firstIndex, list}`. Some (`/group/ids/byDomain/{id}`, `/registrationRules`)
  wrap that in `{success, error, data}`.
- **Errors take four shapes:**
  - 422 `{success: false, error: {message}}` for request-schema violations.
  - 500 with `error.msgKey` for business-rule refusals, e.g.
    `server.switch.portSettings.cannot.enable.flexible.auth.without.switch.authentication`.
  - A bare 400 framework error when a required query parameter is missing,
    e.g. `GET /clitemplate/{type}` without `switchGroupId`.
  - 403 `errorCode 211` for a wrong filter shape on `POST /switchconfig`.
- **Config writes deploy asynchronously.** A write such as `PUT
  /portSettings/{id}`, `PUT /authentication/{switchId}` or `POST
  /clitemplate/update` returns 200/204 at once, and the switch is configured
  later.
  - Each deployment is a transaction in `POST
    /configurationHistory/query/{groupId}` (`deployStatus` `STARTED` →
    `SUCCESS` | `FAILURE`), 17–73 s per single-switch change. One write can
    start more than one transaction (a port write with auth fields starts
    `PORT_CONFIGURATION` and `AUTHENTICATION`).
  - `POST /configurationHistory/detail/query` (filter `transactionId`) gives
    the CLI SmartZone generated (`clis`) and, on failure, the failing line
    number and the switch's error text.
  - `/job` holds firmware and scheduled jobs. Config deployments do not appear
    there.
- **Generated CLI is a diff against the controller's own database**, not the
  switch. A SUCCESS does not prove the switch state: a diff that disables a
  feature switch-wide can remove per-port lines the database still holds.
- **Flexible-authentication `authenticationType`** has no enum in the spec. The
  controller accepts `802.1x`, `macauth` and `802.1x_and_macauth`
  (case-sensitive) and maps anything else to null ("cannot be empty").
- **CLI templates.**
  - `/clitemplate/update` applies to the running config of the switches in its
    comma-separated `switches` string, with no reload.
  - `/clitemplate/provision` runs once, on a factory switch's first approval
    into the group. It replaces the switch's startup config with the template
    and reloads it, whatever the `overwrite` flag says.
  - Template deletes take the list entry `id`, not `cliTemplateConfigId`.
- **Deleting an online switch** (`DELETE /switch/{id}`) disables the switch's
  controller agent and drops all controller-side state for it.
- **GET bodies are not PUT-safe.** A port-settings GET returns `null` for
  array fields (`lldpQosList`), which the PUT schema rejects (422). It also
  returns firmware-gated objects (`pppoeIa`) that a PUT refuses on older
  firmware (500).

## Decision

### A second spec, fetched and generated alongside `wsg`

- `tools/fetch_spec.py` fetches both documents. switchm goes to
  `spec/raw/switchm.json`, with its own entry in `spec/raw/manifest.json`
  (`source`, `spec_info_version`, `spec_sha256`, `fetched_at`, never the host).
- The same `sanitize_spec()` runs on it: `host` overwritten with the
  placeholder, vendor conformance quirks normalised in place.
- `tools/validate_spec.py` validates both documents.
- `tools/generate_models.py` writes the switchm schema index to its own module
  under `ruckus_smartzone/generated/models/`. Definition names do not collide
  with `wsg` in practice, but a separate module keeps the two specs apart.

### One client, one ticket, two base paths

- `SmartZoneClient` keeps one `httpx` session and one `ServiceTicketManager`.
- switchm calls go through a thin sub-client (`client.switchm`) that has the
  same verbs (`get`, `post`, `put`, `patch`, `delete`) but resolves paths
  against `/switchm/api/v13_1/`. The ticket, 401 refresh, retries, busy backoff
  and URL masking are shared, not duplicated.
- The pinned API version stays the single constant in `const.py`. Both base
  paths are built from it.
- `raise_for_response()` also reads `error.message` and `error.msgKey` from
  switchm bodies, so a business-rule refusal raises with its key rather than a
  bare 500.

### Deployment tracking is a first-class helper

- A helper waits for the transaction a write started. It polls group
  configuration history for entries newer than the write, then returns the
  per-switch detail (`clis`, `dispatchStatus`, `dispatchFailedReason`).
- A `FAILURE` raises with the line number and switch message.
- Callers never treat the write's own 2xx as "the switch is configured".

### Write bodies are built, never echoed

Resource wrappers send only the fields a caller sets, filtered to the
operation's request schema. They never send a GET body back as a PUT.

### Scope of the first resource layer

These wrappers are added as consumers need them, each live-verified:

- switch groups
- switches (query, get, move, delete)
- VLANs
- port settings (single and bulk)
- group AAA servers
- DNS
- switch authentication
- flexible-authentication profiles
- CLI templates (`provision`, `update`)
- config backups and drift alerts
- configuration history

Everything else in the spec stays reachable through `client.switchm` verbs
without a wrapper.

## Consequences

- The spec pipeline handles two documents. Tests cover both with inline
  fixtures, offline.
- Switch callers depend on the deployment helper for correctness. A config
  write is done only when its transaction reports `SUCCESS`.
- A failed CLI template leaves the lines before the failing one applied on the
  switch, with no rollback. Callers must keep CLI snippets idempotent and
  re-runnable.
- Errors carry `msgKey`, so callers can branch on stable keys instead of
  message text.
- Nothing that identifies a controller, switch, MAC or serial is committed
  (ADR 0001 still applies).
