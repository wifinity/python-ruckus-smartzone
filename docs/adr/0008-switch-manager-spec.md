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
  wrap that in `{success, error, data}`. `hasMore` is unreliable: some lists
  report `true` on their last page, so `totalCount` is the stop signal.
- **Switch ids are MACs.** `POST /switch` has no serial filter; a full-text
  search on the serial finds it.
- **Configuration history ignores filters and sort fields.** `POST
  /configurationHistory/query/{groupId}` lists the group's whole history in
  no time order: a new transaction can appear anywhere in the list.
- **Error text is HTML-escaped** (`&quot;`, `&gt;`, `&#39;`).
- **The served spec does not validate as-is.** One operation repeats a MIME
  type in `produces`, and another repeats the `serviceTicket` parameter.
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
  placeholder, vendor conformance quirks normalised in place. Repeated MIME
  entries and repeated parameters are collapsed, keeping the first.
- `tools/validate_spec.py` validates both documents.
- `tools/generate_models.py` writes the switchm schema index to its own module
  (`switchm_schema_index.py`, `SWITCHM_SCHEMA_INDEX`). Definition names do not
  collide with `wsg` in practice, but a separate module keeps the two specs
  apart. Each tool takes `--spec` to work on one spec.

### One client, one ticket, two base paths

- `SmartZoneClient` keeps one `httpx` session and one `ServiceTicketManager`.
- switchm calls go through a thin sub-client (`client.switchm`) that has the
  same verbs (`get`, `post`, `put`, `patch`, `delete`) but resolves paths
  against `/switchm/api/v13_1/`. The ticket, 401 refresh, retries, busy backoff
  and URL masking are shared, not duplicated. `query()` pages POST query
  bodies by `page`/`limit`; the AP query shares the same pager.
- The pinned API version stays the single constant in `const.py`. Both base
  paths are built from it.
- `raise_for_response()` also reads `error.message` and `error.msgKey` from
  switchm bodies. A body with a `msgKey` raises `SmartZoneBusinessRuleError`
  (with `msg_key`) rather than a bare 500, and `error.message` (HTML-decoded)
  becomes the exception message.

### Deployment tracking is a first-class helper

- `client.switchm.deployments.track(group_id, switch_ids)` snapshots every
  transaction id in the group history before a write. `wait()` then polls the
  whole history (1000 per page) for new transactions on those switches. It
  returns once at least one appeared, all report `SUCCESS`, and none new
  arrived for a settle period (one write can start two transactions). New
  transactions are told apart by id, not by time, so the caller's clock need
  not match the controller's.
- It returns each transaction with its per-switch detail (`clis`,
  `dispatchStatus`).
- A `FAILURE` raises `SmartZoneDeploymentError` at once, with `line` and
  `switch_message`, and `local_config_conflict` for a push refused during a
  CLI session. No result in time raises `SmartZoneDeploymentTimeoutError`.
- Callers never treat the write's own 2xx as "the switch is configured".

### Write bodies are built, never echoed

Resource wrappers send only the fields a caller sets. `build_body()` checks
them against the operation's request definition in the generated switchm
schema index, raises `ValueError` on an unknown field, and drops `None`. A GET
body fails that check (it carries read-only keys such as `id`), so it is never
sent back as a PUT. `authenticationType` is checked against the three accepted
values before any request.

Switch Manager has no PATCH for config objects (only `PATCH /group/{id}`
for name and description, and `PATCH /firmware/{version}`), and its PUTs are
full replaces: a field the body leaves out is reset or refused as empty (found
live, see below). Every update wrapper therefore uses
`SwitchmResource.merge_put()`, which GETs the object and PUTs `merge_body()`:
the GET body cut down to the update schema's properties, with nulls,
per-resource `drop` keys and `unset` markers removed, and the caller's fields
applied. This is the only way a GET body feeds a write, and only after that
projection. Per resource:

- Nested `None` values are removed everywhere, in the GET body and in the
  caller's fields; the controller rejects them.
- port settings: `pppoeIa` is dropped unless the caller sets it.
- flex-auth profiles: `restrictedVlan`/`criticalVlan` of `0` count as unset,
  because the PUT refuses them unless the fail/timeout action uses them.
- VLANs: trust ports of `""` count as unset (the PUT's port-list pattern
  refuses them).
- AAA servers: `username`/`password` of `""` count as unset. The GET never
  returns `secret`, so `update()` requires it rather than clearing it.
- CLI templates: `variables` of `[]` counts as unset. A provision config's GET
  does not return `models`, so a provision `replace()` requires it.

### Scope of the first resource layer

These wrappers are reached as `client.switchm.<name>`:

- switch groups
- switches (query, get, find by serial, move, delete, port details with LLDP
  neighbours)
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

## Live verification

Read paths, 2026-11-19, against a `7.1.1.0.551` controller and one
ICX8200-48P on `10.0.20` in a dedicated test switch group. All 30 checks
passed:

- groups: list by domain (the staging group is listed), find by name, get
- switches: find by serial, get, list by group
- port details: 52 ports, LLDP neighbours on the uplink and an access port
- port settings: list by switch (one per port), find by identifier, get
- VLANs: by switch and by group, get, default VLAN
- AAA servers and settings, DNS, switch authentication
- flex-auth profiles by group and by query
- CLI templates of both kinds
- backups: list by switch, content, master-backup alerts
- configuration history and transaction detail (including a failed one with
  its line number and message)
- jobs
- a deployment tracker snapshot with no new transactions

Two findings from this run changed the implementation:

- Group configuration history is not in time order, so the tracker reads the
  whole history rather than its tail.
- Backup content is plain text served with a JSON content type, so it is
  read as text.

Write paths, the same day, on the test switch only:

- A port-name change sent as `{portName}` alone deployed as one
  `PORT_CONFIGURATION` transaction (27 s). It also generated `disable`,
  `no inline power`, `no speed-duplex auto` and `no lldp enable` for the port:
  the PUT is a full replace.
- The port was restored through the merged `port_settings.update()` (one
  transaction, 42 s). It generated only the changed lines (`enable`,
  `inline power`, `inline power priority 3`, `lldp enable`), with no resets.
- A port-name revert deployed as one transaction (43 s) generating only
  `no port-name …`.
- An update CLI template with a bad second line made `wait()` raise
  `SmartZoneDeploymentError` after 32 s, with `line=2` and the switch's
  "Invalid input" text. The first line stayed applied.
- `no snmp-server location` without its argument is refused by the switch
  ("Incomplete command"). The undo needs the full line, and with it the
  template deployed (32 s).
- `cli_templates.delete()` by list entry `id` removed all three test
  templates.

Full-replace checks per PUT, on throwaway objects:

| PUT | Partial body | Merged `update()` |
|-----|--------------|-------------------|
| port settings | resets omitted fields (port disabled, PoE and LLDP off) | changed lines only |
| switch authentication | refused: "Auth default vlan cannot be empty" | kept VLAN, no CLI |
| flex-auth profile | refused: "Group Id cannot be empty" | kept other fields |
| VLAN | resets IGMP, DHCP snooping, STP mode and priority | kept them |
| AAA server | refused: "[serverType] : must not be null" | kept other fields |
| AAA settings | refused (nested nulls) | kept the other sections |
| CLI template (provision) | refused: "GroupId cannot be empty" | kept name, group, models |

VLAN, AAA and template checks ran in a throwaway empty switch group, created
for the test and deleted after it. DNS create, update and delete also worked
there.

- A group in CLI config mode (any CLI template ever created in it) refuses
  VLAN and AAA server writes, group-level and switch-level, with "CLI mode is
  enabled. Please do not modify the configuration". Port settings and switch
  authentication still work there.
- `POST /vlans` requires `pushTimeType`; `vlans.create()` defaults it to
  `NOW`.
