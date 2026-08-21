# Ruckus SmartZone Python Client

A Python client library for the Ruckus SmartZone (vSZ) public REST API, targeting
API version `v13_1`.

## Features

- **Service-ticket authentication**: acquires one ticket, reuses it for its
  lifetime, refreshes it on a 401, and releases it on close
- **Pluggable ticket cache**: an in-memory store by default, behind a seam that a
  shared/Redis-backed store can slot into
- **Credential masking**: the ticket travels as a URL query parameter and is
  masked wherever a request URL is logged
- **Transport resilience**: reactive 429 backoff (via `RateLimit-Reset`) and retry
  on a busy/config-lock controller response
- **Pagination helper**: walks `index`/`listSize` list endpoints and concatenates
  the results
- **Typed exceptions**: a `SmartZoneAPIError` hierarchy mapped from HTTP status and
  vendor error codes
- **Dict-first API**: methods return the controller's JSON payloads as dicts
- **Python 3.10+**: synchronous, built on `httpx`

## Installation

From source:

```bash
git clone https://github.com/wifinity/python-ruckus-smartzone.git
cd python-ruckus-smartzone
pip install -e ".[dev]"
```

## Quick Start

```python
from ruckus_smartzone import SmartZoneClient

# Pass the controller root; the /wsg/api/public/v13_1 path is appended for you.
with SmartZoneClient(
    "https://controller.example:8443",
    username="admin",
    password="secret",
    verify=False,  # self-signed controller
) as client:
    print(client.controller_version)

    # Page through every access point (handles index/listSize paging).
    aps = client.paginate("aps", page_size=1000)
    print(f"Found {len(aps)} access points")

    # Any endpoint via the low-level verbs.
    zone = client.get("rkszones/{zoneId}/wlans", params={"zoneId": "..."})
# The service ticket is released (DELETE /serviceTicket) on exit.
```

## Usage

### Client initialization

```python
from ruckus_smartzone import SmartZoneClient

client = SmartZoneClient(
    "https://controller.example:8443",  # controller root
    username="admin",
    password="secret",
    verify=True,        # TLS verification; False for a self-signed controller
    timeout=30.0,       # per-request timeout in seconds
    max_retries=3,      # shared budget for rate-limit and busy backoff
    log_level="DEBUG",  # optional; configures the ruckus_smartzone logger
)
```

### Context manager

Use the client as a context manager so the service ticket is logged off on exit.
Otherwise, call `close()` yourself (a `finally` block is the safe place):

```python
with SmartZoneClient("https://controller.example:8443", "admin", "secret") as client:
    aps = client.paginate("aps")
    # Ticket released automatically here.
```

### Service ticket lifecycle

The ticket is acquired lazily on the first request and reused for its lifetime; a
401 triggers a single refresh-and-retry. `GET /sessionManagement` reports
interactive admin (GUI) logins — an API service-ticket session is not listed
there, so to check whether a ticket is still valid, make a request with it and
observe the status.

To supply a different ticket store (for example a shared cache across processes),
pass any `TicketCache` implementation:

```python
from ruckus_smartzone import SmartZoneClient, TicketCache


class MyCache(TicketCache):
    def get(self): ...
    def set(self, ticket): ...
    def clear(self): ...


client = SmartZoneClient(
    "https://controller.example:8443", "admin", "secret", ticket_cache=MyCache()
)
```

### Low-level API access

The client exposes the HTTP verbs directly. Paths are relative to the versioned
public API root; parameters go in `params`, request bodies in `json`. Each returns
the parsed JSON body as a dict.

```python
result = client.get("aps", params={"zoneId": "..."})
created = client.post("rkszones/{zoneId}/wlans", json={"name": "..."})
updated = client.patch("rkszones/{zoneId}/wlangroups/{id}", json={"name": "..."})
client.delete("rkszones/{zoneId}/wlans/{id}")
```

For paged list endpoints, `paginate()` fetches every page and returns the combined
`list` entries:

```python
# page_size defaults to 100 and is clamped to the API maximum of 1000
aps = client.paginate("aps", page_size=1000)
```

### Resource wrappers

For zones, WLANs, WLAN groups, access points and AP groups the client exposes
dict-first resource wrappers on top of the low-level verbs, reached as
`client.zones`, `client.wlans`, `client.wlan_groups`, `client.access_points` and
`client.ap_groups`. They handle paths and pagination; `create`/`replace` take a
request-body dict and every method returns the controller's JSON as a dict.

```python
# Zones (/rkszones). A zone is named from its site code.
zones = client.zones.list()
zone = client.zones.find_by_name("SITE01")
zid = zone["id"]
client.zones.update(zid, {"description": "..."})   # PATCH: partial edit
client.zones.get(zid)
```

```python
# Zone WLANs (/rkszones/{zoneId}/wlans). Creation bodies vary by WLAN type,
# so create/replace stay dict-first.
wlans = client.wlans.list(zid)
wlan = client.wlans.create(zid, {"name": "Guest", "ssid": "guest-ssid"})
client.wlans.update(zid, wlan["id"], {"description": "..."})  # PATCH: partial edit
client.wlans.find_by_name(zid, "Guest")
```

```python
# WLAN groups (/rkszones/{zoneId}/wlangroups) — {name, description} only.
group = client.wlan_groups.create(zid, "Commissioning", description="...")
gid = group["id"]

# Rename reaches only 'name'; membership is a separate collection and is untouched.
client.wlan_groups.rename(zid, gid, "All Areas - Wireless")

# get-by-name -> create-or-update (POST or PATCH; never PUT).
client.wlan_groups.upsert_by_name(zid, "Commissioning", description="...")

# Members are a first-class collection, addressed by WLAN id.
client.wlan_groups.add_member(zid, gid, wlan["id"], accessVlan=10)
client.wlan_groups.list_members(zid, gid)       # read from the group detail
client.wlan_groups.modify_member(zid, gid, wlan["id"], {"accessVlan": 20})  # PATCH
client.wlan_groups.remove_member(zid, gid, wlan["id"])
```

```python
# Access points (/aps) — keyed on a global MAC namespace, not fenced by zone.
# MACs are normalised to colon-uppercase (8C:0C:90:2B:8B:90) for every request.
aps = client.access_points.list(zone_id=zid)          # filter by zone
ap = client.access_points.get("8c0c902b8b90")         # any written form accepted
client.access_points.create({"mac": mac, "zoneId": zid, "name": "AP-1"})
client.access_points.update(mac, {"description": "..."}, expected_zone_id=zid)  # PATCH
client.access_points.delete(mac)
client.access_points.operational_summary(ap["mac"])   # live check-in / applied state
states = client.access_points.query()                 # bulk state via POST /query/ap

# Move whole sites without knowing the 50-MAC cap: move() chunks and reports
# per-batch outcomes. targetZoneId is required even for an AP-group move.
result = client.access_points.move(
    macs, target_zone_id=dest, target_ap_group_id=group, expected_zone_id=origin
)
if not result.all_succeeded:
    print("failed:", result.failed_macs)
```

```python
# AP groups (/rkszones/{zoneId}/apgroups) — a group pre-points its radios at
# WLAN groups, so moving an AP into a group sets what it broadcasts.
group = client.ap_groups.create(zid, "Wireless", description="...")
agid = group["id"]
client.ap_groups.set_radio_wlan_group(zid, agid, "radio5g", gid)  # point 5G radio
client.ap_groups.upsert_by_name(zid, "Wireless")                  # get-by-name -> POST/PATCH

# Switching an AP's group is a repeatable broadcast-profile change, distinct from
# zone placement (access_points.move). The AP must already be in this zone; if it
# is elsewhere the switch is refused with SmartZoneZoneMismatchError before any
# write. Membership is keyed on the global AP MAC namespace.
client.ap_groups.add_member(zid, agid, "8c0c902b8b90")
client.ap_groups.remove_member(zid, agid, "8c0c902b8b90")
client.ap_groups.clear_radio_wlan_group(zid, agid, "radio5g")     # drop the override
```

**Pre-flight zone guard.** `move`, `update` and `replace` accept an
`expected_zone_id`. When set, each AP's current zone is checked first and the call
is refused with `SmartZoneZoneMismatchError` — before any write — if an AP is
elsewhere. This is what makes the unfenced, MAC-keyed AP calls safe against a
production controller. `move` reports controller-side batch failures in its
`MoveResult` rather than raising, so partial success stays visible.

WLAN-group and AP-group names are validated locally against the controller's
constraints (2–32 printable characters, no leading/trailing space) before
create/rename, so an invalid name raises `SmartZoneValidationError` without a
round trip.

**`update` (PATCH) vs `replace` (PUT).** Use `update` for a partial edit — it sends
only the fields you pass. On zones, WLANs and AP groups, `replace` (PUT) is a
full-object replace that the controller validates against required business fields
(e.g. a zone PUT needs `apMgmtVlan`, a WLAN PUT needs `radiusOptions`), so a partial
body is rejected; prefer `update` unless you are supplying a complete object. WLAN
groups have no PUT at all — `update`/`rename` (PATCH) is the only modify.

### Error handling

```python
from ruckus_smartzone import (
    SmartZoneClient,
    SmartZoneAuthenticationError,
    SmartZoneNotFoundError,
    SmartZonePermissionError,
    SmartZoneValidationError,
    SmartZoneRateLimitError,
    SmartZoneBusyError,
    SmartZoneConnectionError,
    SmartZoneAPIError,
)

try:
    zone = client.get("rkszones/{zoneId}", params={"zoneId": "..."})
except SmartZoneNotFoundError:
    print("Not found (includes a 403 with vendor errorCode 211)")
except SmartZoneAuthenticationError:
    print("Logon failed — check the username and password")
except SmartZonePermissionError:
    print("Permission denied")
except SmartZoneValidationError:
    print("Business-rule violation (422)")
except SmartZoneRateLimitError as e:
    print(f"Rate limited; retry after {e.retry_after}s")
except SmartZoneBusyError:
    print("Controller busy serialising a configuration change")
except SmartZoneConnectionError:
    print("Could not reach the controller")
except SmartZoneAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

### Rate limiting and busy retry

The client retries within `max_retries` on two transient conditions:

- **429**: it waits the number of seconds in the `RateLimit-Reset` header, then
  retries; once the budget is exhausted it raises `SmartZoneRateLimitError`.
- **Controller busy** (SmartZone serialises configuration writes): it retries with
  exponential backoff, then raises `SmartZoneBusyError`.

### Logging

Set the log level when constructing the client, or with the module-level function:

```python
from ruckus_smartzone import set_log_level

set_log_level("DEBUG")
```

At `DEBUG` the client logs each request line with the status code. Because the
service ticket rides in the URL, it is masked as `serviceTicket=***`, and the
`httpx`/`httpcore` loggers are silenced so the raw URL is not emitted.

## Spec-driven models

Model metadata is generated from the controller's Swagger 2.0 document rather than
hand-written:

```bash
make spec-fetch-controller SMARTZONE_BASE_URL=https://<controller>:8443
make generate-models
make spec-validate
```

The controller address is never committed — the fetch step replaces the spec's
`host` with a placeholder. See [spec/README.md](spec/README.md).

## Development

```bash
make venv     # create .venv and install dependencies (uv)
make tests    # lint, type-check and unit tests
make format   # apply black formatting
```

## Scope

Zones, WLANs, WLAN groups and their members, access points, and AP groups and
their members.
