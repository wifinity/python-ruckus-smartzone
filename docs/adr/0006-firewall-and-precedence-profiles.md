# 0006. Firewall and precedence profile resource wrappers

Date: 2026-09-14
Status: Accepted

## Context

A WLAN body references a firewall profile and a precedence profile by id
(`firewallProfileId`, `precedenceProfileId`). Those ids are per-controller: the
same logical profile (e.g. the stock "System Default") has a different id on each
controller, and the WLAN API accepts an unknown id without error while leaving the
profile unset. Callers that hold a profile **name** and target more than one
controller therefore need to resolve the name to that controller's id.

Both profiles are global to the controller (not zone-scoped). The `v13_1` spec
shapes the surface as:

- `GET /firewallProfiles` — list, `index`/`listSize` paging, items carrying `id` +
  `name`; `GET /firewallProfiles/{id}` — detail.
- `GET /precedence` — list over the same paged shape, items carrying `id` + `name`;
  `GET /precedence/{id}` — detail. The `/precedence` list response also carries an
  extra top-level key beyond `{totalCount, hasMore, firstIndex, list}`, which the
  paginator ignores.

## Decision

- A `FirewallProfilesResource` reached as `client.firewall_profiles` and a
  `PrecedenceProfilesResource` reached as `client.precedence_profiles`, each dict-first
  with `list` / `get` / `find_by_name`, over `/firewallProfiles` and `/precedence`
  respectively.
- `find_by_name` reuses the shared `find_one_by_name` helper (as zones and WLANs do):
  an exact `name` match returning the single item, `SmartZoneNotFoundError` when none
  matches, `ValueError` when more than one does.
- Read-only surface. These profiles are managed elsewhere; the wrappers exist to
  resolve a name to an id for a WLAN body, so create/modify/delete are omitted rather
  than speculatively added.

## Consequences

- A caller resolves a profile id with e.g.
  `client.firewall_profiles.find_by_name("System Default")["id"]`, against whichever
  controller the client is bound to, so one name works across controllers whose ids
  differ.
- The profiles are global, so `find_by_name` needs no zone scope, unlike the WLAN and
  AP-group name lookups.
- If a controller carries two profiles with the same name, `find_by_name` raises rather
  than guessing; a caller that needs one of several same-named profiles must list and
  choose.
