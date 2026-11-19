# Agent guide — python-ruckus-smartzone

## What this repo is

Python client library for the Ruckus SmartZone (vSZ) public REST API. Targets
API version `v13_1`. The client surface covers zones, WLANs, WLAN groups and
their members, access points, AP groups and their members, firewall and
precedence profiles, WLAN DPSK keys, zone-to-switch-group links, and ICX
switches through the Switch Manager ("switchm") API.

Build tooling, the spec-driven pipeline, the test harness, the exception/logging
foundation, and the HTTP client with its service-ticket session lifecycle and
transport resilience are in place. Zone, WLAN, WLAN-group, access-point,
AP-group, firewall-profile, precedence-profile, and DPSK resource wrappers are
implemented (reached via `client.zones`, `client.wlans`, `client.wlan_groups`,
`client.access_points`, `client.ap_groups`, `client.firewall_profiles`,
`client.precedence_profiles`, `client.dpsk`). Switch Manager wrappers hang off
`client.switchm` (ADR 0008); the public-API link tying a switch group to a zone
is `client.zone_switch_group_links` (ADR 0009).

## Spec-driven models

The controller serves two Swagger 2.0 documents: the public API (`wsg`) at
`/wsg/apiDoc/openapi` and the Switch Manager API (`switchm`) at
`/switchm/api/openapi`. Model metadata is generated from them rather than
hand-written:

| Step | Tool | Reads → writes |
|------|------|----------------|
| fetch | `tools/fetch_spec.py` | controller → `spec/raw/all.json`, `spec/raw/switchm.json` + `spec/raw/manifest.json` (one entry per spec) |
| generate | `tools/generate_models.py` | raw specs → `ruckus_smartzone/generated/models/` (`schema_index.py`, `switchm_schema_index.py`) |
| validate | `tools/validate_spec.py` | every raw spec present |

Each tool takes `--spec wsg|switchm` to work on one spec. The switchm schema
index is used at runtime: write bodies are checked against its request
definitions.

`fetch_spec.sanitize_spec()` overwrites the spec's `host` with a placeholder (so
no controller address is committed and the checked-in spec is host-independent)
and normalises a defined set of vendor conformance quirks in place — `type: file`
response schemas, typed string defaults, out-of-enum defaults, `{name:regex}`
path templates, repeated MIME entries and repeated parameters — so the specs
validate. The runtime base URL is supplied by the
client. `spec/raw/` is empty until a spec is fetched from a controller.

## Package layout (`ruckus_smartzone/`)

| Path | Purpose |
|------|---------|
| `ruckus_smartzone/__init__.py` | Package version and public exports |
| `ruckus_smartzone/client.py` | `SmartZoneClient`: transport, session lifecycle, retries, pagination |
| `ruckus_smartzone/auth.py` | `ServiceTicketManager`: acquire, reuse, refresh, release the ticket |
| `ruckus_smartzone/ticket_cache.py` | `TicketCache` seam + `InMemoryTicketCache` |
| `ruckus_smartzone/const.py` | Pinned API version and transport constants |
| `ruckus_smartzone/exceptions.py` | `SmartZoneAPIError` hierarchy and status/error-code mapping |
| `ruckus_smartzone/logging_config.py` | Log level control; header and URL-query masking |
| `ruckus_smartzone/validation.py` | Client-side field validation (group name constraints) |
| `ruckus_smartzone/mac.py` | MAC validation and colon-uppercase normalisation |
| `ruckus_smartzone/resources/` | Dict-first zone/WLAN/WLAN-group/access-point/AP-group/firewall-profile/precedence-profile/DPSK/zone-switch-group-link resource wrappers |
| `ruckus_smartzone/switchm/` | Switch Manager sub-client (`client.switchm`): verbs, POST-query pager, resource wrappers, body builder, deployment tracker |
| `ruckus_smartzone/generated/models/` | Generated schema indexes (committed artifacts) |

Repo root: `tools/`, `spec/`, `tests/`, `Makefile`, `pyproject.toml`.

## Conventions

- **Distribution** `ruckus-smartzone`; **import** `ruckus_smartzone`.
- **Entry point:** `from ruckus_smartzone import SmartZoneClient`, used as a context
  manager so the ticket is released on exit.
- **Public API is dict-first**; the generated schema index is an internal artifact.
- **Errors** derive from `SmartZoneAPIError`, carrying `status_code` and `response_data`.
- **HTTP transport** is synchronous `httpx`-based. The service ticket rides as a URL
  query parameter and is masked wherever a URL is logged.
- **Switch Manager** calls go through the same transport with absolute
  `/switchm/api/v13_1/` URLs. Writes build bodies from caller fields via
  `switchm.base.build_body` (never a GET body), and config writes are confirmed
  with `client.switchm.deployments`, not by their 2xx.

## Testing

- Full suite: `make tests` (`lint`, `type-check`, `unit-tests`).
- Tests in `tests/` use `pytest` with `respx` for HTTP isolation; pipeline tools
  are tested offline with inline spec fixtures (no live controller).

## Where to look

- **Index:** [INDEX.md](INDEX.md)
- **Decision records:** [adr/](adr/) — API version (0001), auth/transport (0002),
  zone/WLAN/group wrappers (0003), access points (0004), AP groups (0005),
  firewall/precedence profiles (0006), DPSK keys (0007),
  Switch Manager spec and client surface (0008), zone switch group links (0009)
- **Memory:** [.agents/memory/python-ruckus-smartzone-repository-memory.md](../.agents/memory/python-ruckus-smartzone-repository-memory.md)
