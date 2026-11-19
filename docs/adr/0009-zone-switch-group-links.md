# 0009. Zone switch group links

Date: 2026-11-19
Status: Proposed

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

## Decision

- A `ZoneSwitchGroupLinksResource` reached as `client.zone_switch_group_links`,
  dict-first, in `ruckus_smartzone/resources/` beside the other `wsg` wrappers.
  It stays off `client.switchm` because the endpoints are public-API ones and
  use the public-API base path and paging.
- `list(*, zone_id, switch_group_id, domain_id)` sends only the filters given
  and walks every page with `client.paginate`.
- `find(zone_id, switch_group_id)` lists with both filters and then matches both
  ids client-side, returning the record whatever its `link` flag, or `None`.
  More than one record for the pair raises `ValueError` rather than guessing.
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
- The controller's behaviour (whether the list filters are honoured, whether a
  pair can hold more than one record, what a `link: false` record means in the
  UI) is not yet confirmed against a live controller; `find` tolerates filters
  being ignored by matching both ids itself.
