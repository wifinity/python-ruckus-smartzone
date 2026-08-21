# 0004. Access point resource wrapper

Date: 2026-08-20
Status: Accepted

## Context

The access-point surface is the last part of the client. Unlike zones, WLANs and
WLAN groups — all fenced under `/rkszones/{zoneId}/…` — APs are addressed by a
**global MAC namespace**. `POST /aps/move` and the `/aps/{apMac}` verbs are the
only calls in the whole SDK not scoped to a zone, so a wrong MAC reaches an AP on
any zone of a production controller.

The `v13_1` spec shapes the surface as:

- `GET /aps` — list, filterable by `zoneId`/`domainId`, `index`/`listSize` paging.
- `GET /aps/{apMac}` — returns `ap_apConfiguration`, which carries `zoneId`.
- `POST /aps` — `ap_createAP` (requires `mac` and `zoneId`).
- `PATCH`/`PUT /aps/{apMac}` — `ap_modifyAP` (partial / full replace).
- `DELETE /aps/{apMac}` — optional `validateMesh` flag.
- `POST /aps/move` — `{apMacs (max 50), targetZoneId (required), targetApGroupId}`.
- `POST /query/ap` — bulk state; pages by **`page`/`limit` in the POST body**.
- `GET /aps/{apMac}/operational/summary` — live check-in / applied-config state.

Two constraints the caller should not have to carry: the 50-MAC move cap, and the
danger of writing to an AP that is not where the caller believes it is.

## Decision

- An `AccessPointsResource` dict-first wrapper reached as `client.access_points`,
  with `list`/`get`/`create`/`update`/`replace`/`delete`, `operational_summary`,
  `query`, and `move`. Create and replace stay pass-through dict bodies, matching
  zones/WLANs.
- **MAC normalisation** (`ruckus_smartzone/mac.py`, `normalize_mac`): every MAC in
  an identifier position is normalised to SmartZone's colon-uppercase form
  (`8C:0C:90:2B:8B:90`) and validated, turning malformed input into a local
  `ValueError`. It accepts colon, hyphen, dotted-quad and bare-hex input and is
  stdlib-only — colon-uppercase is not the `macaddress` library's output, so no
  dependency is added.
- **Chunking in `move`**: MACs are split into batches of at most 50 (`MAX_MOVE_BATCH`)
  and each `POST /aps/move` is one batch. A failed batch is recorded and the
  remaining batches are still attempted; the return value is a `MoveResult` of per-
  batch `MoveBatchResult`s (`all_succeeded`, `moved_macs`, `failed_macs`), so
  partial success is visible rather than swallowed. `targetZoneId` is always sent
  (the endpoint requires it even for an AP-group move); `targetApGroupId` is sent
  when given.
- **Pre-flight zone guard**: `move`, `update` and `replace` take an optional
  `expected_zone_id`. When set, each AP's current `zoneId` is read via
  `GET /aps/{apMac}` and, if any AP is elsewhere, `SmartZoneZoneMismatchError` is
  raised **before any write** — for a batch move, no move call is issued at all.
  The error carries a `{mac: actual_zone}` map.
- **`query` paginator**: `/query/ap` pages by `page`/`limit` in the POST body, not
  the GET `index`/`listSize` that `client.paginate()` walks, so it has its own
  loop over the same `{totalCount, hasMore, firstIndex, list}` response shape.

## Consequences

- The guard is opt-in per call; callers working against production pass
  `expected_zone_id`, and every later workflow inherits the same safety by using
  these methods.
- `move` never raises on a controller-side batch failure — callers must inspect
  `MoveResult`. Only client-side refusal (the guard) and malformed MACs raise.
- The guard costs one `GET` per AP before a write; for large moves this is a read
  per AP ahead of the batched writes.

## Live verification

Verified against a SmartZone `7.1.1.0.551` controller (API `v13_1`) with a
physical AP, 2026-08-21, using non-customer test zones:

- **`move` is the adoption trigger.** Moving a discovered, unapproved AP into a
  real zone both placed it and flipped `registrationState` `Pending → Approved` in
  one call — there is no separate approve step over the API.
- **Move propagation is sub-2s** each way (measured from the `move` call returning
  to `operational/summary` reflecting the new `zoneId`), so propagation lag is
  negligible in practice. A move nonetheless returns HTTP 200 even when it
  cannot apply (e.g. no AP-capacity license), so callers must confirm via
  `operational/summary` rather than trust the move's status.
- **Pre-flight guard fires live:** `move` with a wrong `expected_zone_id` raised
  `SmartZoneZoneMismatchError` and left the AP's zone unchanged — no write issued.
- **`query` paginator** walked the full controller inventory (~1800 APs over
  several `page`/`limit` pages) correctly.
- **CRUD + delete** confirmed; `delete` returns 204 and is the only operation that
  frees the AP's capacity license (an offline or moved-back AP keeps it).

The AP config-sync field `configState` walks `null → newConfig → fwApplied →
configApplied → completed` (terminal `completed`); `connectionState` +
`lastSeenTime` are the liveness signals (`uptime` reads `-1` even when adopted).
