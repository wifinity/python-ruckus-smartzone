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
- **ICX switches**: Switch Manager API wrappers with a deployment waiter that
  reports the failing CLI line
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

For zones, WLANs, WLAN groups, access points, AP groups, firewall and
precedence profiles, and DPSK keys the client exposes dict-first resource wrappers
on top of the low-level verbs, reached as `client.zones`, `client.wlans`,
`client.wlan_groups`, `client.access_points`, `client.ap_groups`,
`client.firewall_profiles`, `client.precedence_profiles` and `client.dpsk`. They handle paths and pagination; `create`/`replace`
take a request-body dict and every method returns the controller's JSON as a dict.

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
# An AP-level radio wlanGroupId wins over the AP group's; clearing it makes the
# radio inherit from the AP group again (radio24g/5g/5gLower/5gUpper/6g).
client.access_points.clear_radio_wlan_group(mac, "radio24g", expected_zone_id=zid)
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

```python
# Firewall (/firewallProfiles) and precedence (/precedence) profiles are global to
# the controller. A WLAN body takes firewallProfileId / precedenceProfileId as plain
# ids with no name form, and those ids differ per controller, so resolve by name
# against the target controller before building the body.
fw_id = client.firewall_profiles.find_by_name("System Default")["id"]
pr_id = client.precedence_profiles.find_by_name("System Default")["id"]
client.firewall_profiles.list()
```

```python
# DPSK keys (/rkszones/{zoneId}/wlans/{wlanId}/dpsk) on a DPSK-enabled WLAN.
# The WLAN is created as plain WPA2 and then switched to DPSK with a PATCH; a
# create body carrying a dpsk block fails with HTTP 500.
wid = client.wlans.create(zid, {"name": "Res", "ssid": "Res", "encryption": {
    "method": "WPA2", "algorithm": "AES", "passphrase": "...", "mfp": "disabled"}})["id"]
client.wlans.update(zid, wid, {"dpsk": {"dpskEnabled": True}})
# There is no single-key create or per-key DELETE in the API: create() is the
# one-key form of generate() (batchGenUnbound), and deletes POST an idList.
key = client.dpsk.create(zid, wid, user_name="room-101", passphrase="...", vlan_id=101)
client.dpsk.create(zid, wid, user_name="residents", passphrase="...", group_dpsk=True)
client.dpsk.generate(zid, wid, amount=3, user_name="student")  # student_0..2
client.dpsk.list(zid, wid)
client.dpsk.list_zone(zid)                                      # every WLAN in the zone
client.dpsk.find_by_user_name(zid, wid, "room-101")
client.dpsk.update(zid, wid, key["id"], user_name="room-102")   # userName only
client.dpsk.upload(zid, wid, csv_text)                          # multipart CSV
client.dpsk.delete_many(zid, wid, [key["id"]])                  # returns deleted count
client.dpsk.set_delete_expired(zid, "AfterSixMonths")           # zone-wide setting
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

### Switch Manager (ICX switches)

SmartZone manages ICX switches through its Switch Manager service, a separate
REST API at `/switchm/api/v13_1`. `client.switchm` reaches it with the same
service ticket, retries and URL masking. Its verbs (`get`, `post`, `put`,
`patch`, `delete`) take paths relative to that root, `query()` pages a POST
query body, and these wrappers cover the common operations:

| Attribute | Covers |
|-----------|--------|
| `groups` | switch groups of a domain: list, get, `find_by_name`, create, update, delete |
| `switches` | query, `list_group`, get, `find_by_serial`, `move` (approve), delete, `port_details` (LLDP neighbours) |
| `vlans` | group or switch VLANs: list, get, `default_vlan`, create, update, delete |
| `port_settings` | per-port settings: `list_switch`, `find`, get, update, `bulk_update` |
| `aaa_servers` | group AAA servers and AAA settings |
| `dns` | group DNS server |
| `authentication` | switch-level authentication (auth-default VLAN) |
| `flex_auth_profiles` | flexible-authentication profiles |
| `cli_templates` | `provision` and `update` CLI templates |
| `config_backups` | backups, content, master-backup drift alerts |
| `config_history` | deployment transactions and their per-switch detail |
| `jobs` | firmware and scheduled jobs |
| `deployments` | wait for a write's deployment to finish |

A switch's id is its MAC (`02:00:00:AA:BB:01`); MACs are normalised for every
request.

```python
sm = client.switchm

# Find a newly registered switch by serial and approve it into the site group.
switch = sm.switches.find_by_serial("FNG0000X000")
group = sm.groups.find_by_name(switch["domainId"], "SITE01")
sm.switches.move(group["id"], [switch["id"]])

# Port flexible authentication needs switch-level authentication first.
sm.authentication.update(switch["id"], enabled=True, default_vlan=4000)
```

**Writes deploy asynchronously.** A Switch Manager write returns at once; the
switch is configured later, in one or more transactions in the group's
configuration history. Wrap writes in `deployments` to wait for them and get
the generated CLI back:

```python
port = sm.port_settings.find(switch["id"], "1/1/10")
with sm.deployments.track(group["id"], [switch["id"]]) as tracker:
    sm.port_settings.update(
        port["id"],
        {
            "flexibleAuthenticationEnabled": True,
            "authenticationType": "802.1x_and_macauth",
            "authDefaultVlan": 91,
        },
    )
done = tracker.wait(timeout=300)   # [{"transaction": ..., "details": [{"clis": ...}]}]

# Or in one call: result, done = sm.deployments.run(group_id, lambda: ..., switch_ids=[...])
```

`wait()` raises `SmartZoneDeploymentError` when a transaction reports
`FAILURE`, with `line` and `switch_message` from the switch. Lines before the
failing one stay applied; there is no rollback. `local_config_conflict` is true
when the switch refused the push because a CLI session was in config mode, which
is worth a retry. `SmartZoneDeploymentTimeoutError` is raised if the
deployment does not finish in time. A `SUCCESS` reports what the controller
sent; the controller generates CLI as a diff against its own database, so check
the switch (for example a config backup) when the outcome matters.

**Write bodies are built from your fields.** Write methods take only the fields
to change, keyed by their API names, and check them against the request schema
of the generated Switch Manager spec: an unknown field raises `ValueError`
before any request, and `None` values are dropped. Do not send a GET body back:
it is refused by that check, and the controller would reject it anyway (null
arrays give 422, firmware-gated objects such as `pppoeIa` give 500).
`authenticationType` must be one of `AUTHENTICATION_TYPES` (`802.1x`,
`macauth`, `802.1x_and_macauth`).

**CLI templates.** A `provision` template runs once, on a factory switch's first
approval into the group: it replaces the startup config and reloads the switch.
An `update` template applies to the running config of the switches you list,
with no reload. Delete a template by its list entry `id`, not its
`cliTemplateConfigId`.

**Deleting an online switch** disables its controller agent: the switch stops
talking to SmartZone until its manager is re-enabled on the switch or it is
factory-reset.

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
    SmartZoneBusinessRuleError,
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
except SmartZoneBusinessRuleError as e:
    print(f"Switch Manager refused the request: {e.msg_key}")
except SmartZoneAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

Switch Manager business-rule refusals come back as HTTP 500 with a stable
`error.msgKey` and raise `SmartZoneBusinessRuleError`; branch on `msg_key`, not
on the message. A Switch Manager `error.message` becomes the exception message.

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

Model metadata is generated from the controller's two Swagger 2.0 documents (the
public API and the Switch Manager API) rather than hand-written:

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

Zones, WLANs, WLAN groups and their members, access points, AP groups and
their members, firewall and precedence profiles, DPSK keys, and ICX switches
through the Switch Manager API.
