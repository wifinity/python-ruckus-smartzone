# 0005. AP group resource wrapper

Date: 2026-08-21
Status: Accepted

## Context

An AP group is a zone-scoped bundle whose radios are each pre-pointed at a WLAN
group. Moving an AP into a group is therefore what changes the SSIDs that AP
broadcasts, and it is distinct from where the AP joins the controller: an AP's
zone is set once (its join placement, owned by `access_points.move`), while its
AP group is switched repeatedly (its broadcast profile). An AP belongs to one AP
group per zone.

The `v13_1` spec shapes the surface as:

- `GET /rkszones/{zoneId}/apgroups` — list, `index`/`listSize` paging.
- `POST /rkszones/{zoneId}/apgroups` — `apgroup_createAPGroup` (`name` required).
- `GET /rkszones/{zoneId}/apgroups/default` — the zone's default AP group.
- `GET /rkszones/{zoneId}/apgroups/{id}` — detail, carrying `radioConfig`.
- `PATCH /rkszones/{zoneId}/apgroups/{id}` — `apgroup_modifyAPGroup` (partial).
- `PUT /rkszones/{zoneId}/apgroups/{id}` — full replace.
- `DELETE /rkszones/{zoneId}/apgroups/{id}` — delete.
- `POST`/`DELETE /rkszones/{zoneId}/apgroups/{id}/members/{apMac}` — add/remove an
  AP, keyed on the **global AP MAC namespace** (as `POST /aps/move` is).
- `DELETE /rkszones/{zoneId}/apgroups/{id}/radioConfig/{radio}/wlanGroupId` — clear
  a radio's WLAN-group override (`radio` ∈ `radio24g`, `radio5g`, `radio5gLower`,
  `radio5gUpper`, `radio6g`).

The AP-group `name` resolves to the same `common_normalName` (2–32 printable
characters, no leading/trailing space) already enforced for zone and WLAN-group
names.

## Decision

- An `APGroupsResource` dict-first wrapper reached as `client.ap_groups`, with
  `list`/`get`/`get_default`/`create`/`update`/`replace`/`delete`,
  `find_by_name`/`upsert_by_name`, `add_member`/`remove_member`, and
  `set_radio_wlan_group`/`clear_radio_wlan_group`. It mirrors the WLAN-group
  wrapper's name-validation and `find_by_name`/`upsert_by_name` semantics and the
  zone wrapper's PATCH-partial / PUT-full split.
- **`update` (PATCH) vs `replace` (PUT).** As recorded for zones and WLANs in ADR
  0003, PUT on this controller is a full-object replace: a partial body is
  rejected with a vendor "business rule" error and an echoed-back GET detail body
  is rejected (HTTP 400). So `update` is PATCH for partial edits and `replace`
  (PUT) is used only with a complete, curated body. `create` validates the name
  and passes through any extra body fields (e.g. `radioConfig`).
- **Zone-guarded membership.** `add_member(zone_id, group_id, ap_mac)` normalises
  the MAC and, because the members endpoint is keyed on the global MAC namespace,
  first reads the AP's current zone and refuses with `SmartZoneZoneMismatchError`
  — before any write — unless the AP is already in `zone_id`. This keeps the two
  operations strictly separate: an AP-group switch never moves an AP between
  zones, and a wrong MAC cannot reach an AP in another zone. The guard reuses the
  same pre-flight the access-point wrapper uses. `remove_member` is an unguarded,
  MAC-normalised delete (detaching a member the AP does not have is a controller
  no-op).
- **Radio WLAN-group overrides.** `set_radio_wlan_group` sends a PATCH carrying
  only `{"radioConfig": {radio: {"wlanGroupId": ...}}}`; `clear_radio_wlan_group`
  issues the dedicated per-radio DELETE. Both reject an unknown radio locally.
- Names are validated locally against `common_normalName` before create/modify,
  turning an invalid name into a local `SmartZoneValidationError` with no round
  trip.

## Consequences

- The membership guard costs one `GET /aps/{apMac}` before the add, and requires
  zone placement to have happened first — which matches the intended split
  between placement (`access_points.move`) and broadcast-profile switching.
- `replace` callers must supply a complete object; partial changes go through
  `update`.
- `create` accepting pass-through fields keeps the richer AP-group body
  (radios, model policies) expressible without a typed model, consistent with the
  dict-first convention.

## Live verification

Verified against a SmartZone `7.1.1.0.551` controller (API `v13_1`) with a
physical AP, using a non-customer test zone. The test group was deleted and the
AP returned to its original zone and group afterward, leaving nothing behind.

- **CRUD confirmed.** `create` returns `{id}`; `get`/`get_default`/`list`,
  `update` (PATCH), `find_by_name` and `upsert_by_name` all behaved as designed.
- **Radio override round-trips.** `set_radio_wlan_group` on `radio5g` was
  reflected in the group's `radioConfig.radio5g.wlanGroupId` on read-back, and
  `clear_radio_wlan_group` reset it to `null`.
- **`add_member` auto-removes from the previous group.** Adding an AP resident in
  the zone to a second AP group moved it out of its former group in one call —
  the former group's `members` no longer listed it and the AP's `apGroupId`
  became the new group. `remove_member` returned the AP to the zone's `default`
  AP group. This confirms an AP belongs to exactly one AP group per zone, so a
  group switch is a single `add_member`, not a remove-then-add.
- **Zone guard fires live.** `add_member` for an AP in another zone raised
  `SmartZoneZoneMismatchError` (carrying `{mac: actual_zone}`) and issued no
  write. Placing the AP in the zone first (via `access_points.move`) let the same
  call succeed — confirming placement and group-switch are separate steps.
- **Partial `PUT` is rejected**, as assumed, but the failure mode differs from
  zones/WLANs: instead of the business-rule `errorCode` 302, an AP-group PUT
  missing `name` returned HTTP 500 from the backend (a null-key error on the
  required `name`). The conclusion is the same — PUT is a full-object replace and
  needs a complete, curated body; use `update` (PATCH) for partial edits.

### AP-group create is zone-dependent (drift note)

A minimal `create` body (`{name, description}`) succeeded in one test zone but
returned HTTP 500 (`NullPointerException`) in another. AP-group creation is
sensitive to the zone's AP-firmware/template: some zones require a fuller body.
The wrapper stays dict-first and passes extra create fields through unchanged, so
a caller supplies whatever the target zone requires; the SDK does not assume a
minimal body works everywhere.
