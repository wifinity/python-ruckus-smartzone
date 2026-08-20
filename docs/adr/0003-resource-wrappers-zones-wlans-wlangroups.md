# 0003. Resource wrappers for zones, WLANs and WLAN groups

Date: 2026-08-20
Status: Accepted

## Context

On top of the low-level verbs and `paginate()` from ADR 0002, the client needs a
resource layer for the core configuration surface: zones, the WLANs within a
zone, and WLAN groups with their members.

The `v13_1` spec shapes these three differently:

- **Zones** (`/rkszones`) carry a large configuration body; create requires
  `name` plus an AP `login`.
- **WLANs** (`/rkszones/{zoneId}/wlans`) have twelve typed create variants
  (open, 802.1X, hotspot, …), each with its own body.
- **WLAN groups** (`/rkszones/{zoneId}/wlangroups`) are only `{name, description}`
  and have **no PUT**. There is no `wlanGroupId`-level write that carries
  membership: a group's WLAN members live in a separate `/members` sub-resource
  (`POST`, `PATCH`/`PUT`/`DELETE` per member). Group names follow `common_normalName`
  (2–32 printable characters, no leading/trailing space).

A tempting but wrong model is to treat a WLAN group as one upsertable object and
write it back with `PUT` — an endpoint that does not exist on this API. The
consequence worth proving is structural: because membership is not part of any
writable group body, **renaming a group cannot disturb its membership**.

## Decision

- A `resources/` package of **dict-first** wrappers, one class per resource,
  each holding the owning client and reusing its verbs and `paginate()`. They are
  reached as `client.zones`, `client.wlans`, `client.wlan_groups`.
- **Zones and WLANs stay pass-through**: `create`/`replace` take a full request
  body dict, because the controller's own bodies are large and (for WLANs)
  type-dependent. Each exposes `list`/`get`/`create`/`update`/`replace`/`delete`
  and a `find_by_name` lookup (callers commonly resolve a zone by its name).
- **WLAN groups get a typed convenience** matching the narrow body:
  `create(name, description)`, `update(name=…, description=…)`, `rename(name)`,
  `delete`, and `upsert_by_name` (get-by-name → POST-or-PATCH, never PUT). Group names are
  validated locally (`validation.validate_group_name`) before create/rename, so a
  bad name raises `SmartZoneValidationError` without a round trip.
- **Members are a first-class collection** on the group resource:
  `add_member(wlan_id, **fields)`, `modify_member`, `replace_member`,
  `remove_member`, and `list_members` (read from the group detail's `members`
  array). A member is addressed by its WLAN id.

The group `update`/`rename` body carries only the fields passed, so a rename
reaches only `name`; membership is untouched by construction.

## Consequences

- The "upsert the whole group object" shortcut is deliberately not offered; the
  no-PUT shape is exposed directly, and the partial-clobber risk cannot arise.
- Resource wrappers add no transport logic of their own — pagination, the ticket
  lifecycle, retries and error mapping all remain in the client.
- WLAN and zone creation remain the caller's responsibility to shape; the SDK does
  not model every typed WLAN body.

## Live verification

Verified against a SmartZone `v13_1` controller (SmartZone software `7.1.1.0.551`)
on 2026-08-20, inside a non-production test zone, using a throwaway WLAN group:

- **Read paths.** `zones.list()` paged the full zone list; `wlans.list(zone)` and
  `wlan_groups.list(zone)` returned the zone's WLANs and groups. Request logs
  rendered the ticket as `serviceTicket=%2A%2A%2A` throughout.
- **Full create chain.** `zones.create({name, countryCode, login})` returned a new
  zone id; `wlans.create(zone, {name, ssid})` added a standard-open WLAN in it;
  `wlan_groups.create(zone, name)` added a group; `add_member(zone, group, wlan_id)`
  put the new WLAN into the group, read back via `list_members`. Tearing down with
  group / WLAN / zone `delete` left nothing behind — a `zones.get` on the deleted
  zone raised `SmartZoneNotFoundError`. This exercised the dict-first zone and WLAN
  create/replace bodies against the live controller.
- **Group create + members.** `create(zone, name, description=…)` returned the new
  group id (201); two `add_member(zone, group, wlan_id)` calls (201 each) produced
  a membership of exactly those two WLAN ids, read back via `list_members`.
- **Rename preserves membership (the key proof).** `rename(zone, group, new_name)`
  issued a single `PATCH` (204); the group detail then showed the new name with
  the **identical** member set — confirming that a rename cannot disturb
  membership by live evidence, not just by spec shape.
- **Lookup + delete.** `find_by_name` resolved the renamed group back to its id;
  `remove_member` (204 each) then `delete` (204) removed the throwaway objects,
  and a subsequent `find_by_name` raised `SmartZoneNotFoundError`. No production
  objects were modified.
- **Remaining methods.** `wlans.get`/`update`/`find_by_name`, `zones.update`,
  `wlan_groups.upsert_by_name` (both the update-existing and create-new branches),
  and member `modify_member` (PATCH) / `replace_member` (PUT) were each exercised
  and confirmed. Deleting a zone cascade-removed its WLANs and groups; a `get` on
  the deleted zone returned a 403 with vendor `errorCode` 211, correctly mapped to
  `SmartZoneNotFoundError`.

### Zone and WLAN PUT are full-object replaces (drift note)

`zones.replace` and `wlans.replace` (PUT) are documented in the spec with no
required fields, but the controller rejects a partial body with an `errorCode` 302
"Business rule violation": a zone PUT reported `apMgmtVlan cannot be empty` and a
WLAN PUT `radiusOptions may not be null`. Echoing a GET detail body straight back
also fails (the read model carries fields the modify body rejects — HTTP 400). PUT
is therefore a genuine full-object replace requiring a complete, curated body;
partial edits must use `update` (PATCH). The `replace` wrappers issue the PUT and
map the response correctly — the constraint is the controller's, not the SDK's.
A successful PUT is covered by `replace_member` (204).
