# 0009. Zone switch group links

Date: 2026-11-19
Status: Accepted

## Context

A site has a zone (public API, `client.zones`) and a Switch Manager switch group
(`client.switchm.groups`). The controller ties the two together with a link
record, and that record lives in the public `wsg` API, not in Switch Manager.
The `v13_1` spec (tag "Zone Switch Group Link") shapes it as:

- `GET /zoneSwitchGroupLinks` — `index`/`listSize` paging over
  `{totalCount, hasMore, list}` (plus `rawDataTotalCount`), filtered by optional
  `domainId`, `zoneId` and `switchGroupId` query parameters. Items are
  `{id, zoneId, switchGroupId, link}`.
- `POST /zoneSwitchGroupLinks` — body `{zoneId, switchGroupId, link}`, returns
  `{id}`.
- `GET`, `PUT` and `DELETE /zoneSwitchGroupLinks/{id}`. The PUT body is the same
  `{zoneId, switchGroupId, link}` record as the create.

`link` is a boolean on the record, so a record can exist for a pair without the
pair being linked.

Read on a production `7.1.1.0.551` controller on 2026-11-19 (read-only; the
controller held no link records):

- The list accepts **at most one filter**. `zoneId` together with
  `switchGroupId` returns HTTP 500 with `"At most 1 parameter"`.
- A `switchGroupId` filter naming an unknown group returns HTTP 500 (`"User has
  no permission to access zone null or switch group …"`). Unknown `zoneId`
  values and a real `domainId` return an empty list.
- `GET /zoneSwitchGroupLinks/{id}` for an unknown id returns no body, which the
  client surfaces as `None`, not `SmartZoneNotFoundError`.

## Decision

- A `ZoneSwitchGroupLinksResource` reached as `client.zone_switch_group_links`,
  dict-first, in `ruckus_smartzone/resources/` beside the other `wsg` wrappers.
  It stays off `client.switchm` because the endpoints are public-API ones and
  use the public-API base path and paging.
- `list(*, zone_id, switch_group_id, domain_id)` sends the one filter given and
  walks every page with `client.paginate`. Two or more filters raise
  `ValueError` before any request.
- `find(zone_id, switch_group_id)` lists by `zoneId` only, because a zone
  filter tolerates unknown ids, and matches the switch group client-side. It
  returns the record whatever its `link` flag, or `None`. More than one record
  for the pair raises `ValueError` rather than guessing.
- `create(zone_id, switch_group_id, link=True)` posts the full record.
- `update(id, fields)` is read-merge-PUT, as in Switch Manager (ADR 0008): it
  reads the record, keeps `zoneId`, `switchGroupId` and `link`, overlays the
  given fields and PUTs the result. Fields outside those three, or an empty
  change, raise `ValueError` before any request.
- `get(id)` and `delete(id)` map straight onto the item endpoints.

## Consequences

- A caller links a site's group to its zone by resolving the zone
  (`client.zones.find_by_name`), the group
  (`client.switchm.groups.find_by_name(zone["domainId"], name)`), then calling
  `find` and `create` or `update` as needed.
- `update` costs a GET before each PUT, and a caller cannot clear a field by
  leaving it out.
- Only reads have been exercised live. Create, update and delete, whether a
  pair can hold more than one record, and what a `link: false` record means in
  the UI are not yet confirmed against a controller.
