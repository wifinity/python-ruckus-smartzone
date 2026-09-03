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
- **Membership is set via the AP's `apGroupId`, not the `/members` endpoint.**
  `add_member(zone_id, group_id, ap_mac)` sets the AP's `apGroupId` through
  `access_points.update(mac, {"apGroupId": group_id}, expected_zone_id=zone_id)`;
  the controller mirrors that into the group's member list. `remove_member`
  returns the AP to the zone's `default` group (resolved via `get_default`) the
  same way. Both reuse `update`'s `expected_zone_id` pre-flight, so an AP-group
  switch never moves an AP between zones and refuses with
  `SmartZoneZoneMismatchError` — before any write — if the AP is elsewhere. The
  `POST`/`DELETE .../members/{apMac}` calls and folding a group into
  `access_points.move` (`targetApGroupId`) are **not** used: live testing found
  they half-apply — recording a member row without re-homing the AP's `apGroupId`
  — which then wedges further member calls (see Live verification).
- **Radio WLAN-group overrides.** `set_radio_wlan_group` sends a PATCH carrying
  only `{"radioConfig": {radio: {"wlanGroupId": ...}}}`; `clear_radio_wlan_group`
  issues the dedicated per-radio DELETE. Both reject an unknown radio locally.
- Names are validated locally against `common_normalName` before create/modify,
  turning an invalid name into a local `SmartZoneValidationError` with no round
  trip.

## Consequences

- Setting membership costs one `PATCH /aps/{apMac}` plus the pre-flight
  `GET /aps/{apMac}`, and requires zone placement to have happened first — which
  matches the intended split between placement (`access_points.move`) and
  broadcast-profile switching. `remove_member` additionally reads
  `GET .../apgroups/default`.
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
  group switch is a single call, not a remove-then-add.
- **Zone guard fires live.** `add_member` for an AP in another zone raised
  `SmartZoneZoneMismatchError` (carrying `{mac: actual_zone}`) and issued no
  write. Placing the AP in the zone first (via `access_points.move`) let the same
  call succeed — confirming placement and group-switch are separate steps.
- **Partial `PUT` is rejected**, as assumed, but the failure mode differs from
  zones/WLANs: instead of the business-rule `errorCode` 302, an AP-group PUT
  missing `name` returned HTTP 500 from the backend (a null-key error on the
  required `name`). The conclusion is the same — PUT is a full-object replace and
  needs a complete, curated body; use `update` (PATCH) for partial edits.

### Fresh-adoption placement half-applies via `/members` and `move` (2026-09-03)

A later live test (a first-time-onboarded AP that should have landed in
`Commissioning`) exposed the failure the current design avoids. When placement was
folded into the adoption move — `access_points.move(target_zone_id, target_ap_group_id)`
— the controller re-homed the AP into the zone's `default` group and only wrote a
`members` row for the target group; the AP's own `apGroupId` (both config body and
`operational/summary`) stayed `default`. HTTP 200, half-applied. The stray member
row then wedged the `/members` endpoint: `POST` returned 422 `errorCode 302` ("AP …
already exist") and `DELETE` returned HTTP 500 ("current AP Group are inconsistent
for AP … data in database and data sent from Web UI").

Setting the AP's `apGroupId` directly — `access_points.update(mac, {"apGroupId": …})`
— re-homed the AP and reconciled the member list, with both `apGroupId` sources
reflecting the target within seconds. So `move`'s `target_ap_group_id` was removed
and `add_member`/`remove_member` were re-pointed at the `apGroupId` PATCH. The AP's
`apGroupId` is the single source of truth for placement; the `/members` sub-resource
and `move(targetApGroupId)` are not written.

### AP-group create is zone-dependent (drift note)

A minimal `create` body (`{name, description}`) succeeded in one test zone but
returned HTTP 500 (`NullPointerException`) in another. AP-group creation is
sensitive to the zone's AP-firmware/template: some zones require a fuller body.
The wrapper stays dict-first and passes extra create fields through unchanged, so
a caller supplies whatever the target zone requires; the SDK does not assume a
minimal body works everywhere.
