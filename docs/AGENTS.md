# Agent guide — python-ruckus-smartzone

## What this repo is

Python client library for the Ruckus SmartZone (vSZ) public REST API. Targets
API version `v13_1`. The client surface covers zones, WLANs, WLAN groups and
their members, access points, and AP groups and their members.

Build tooling, the spec-driven pipeline, the test harness, the exception/logging
foundation, and the HTTP client with its service-ticket session lifecycle and
transport resilience are in place. Zone, WLAN, WLAN-group, access-point, and
AP-group resource wrappers are implemented (reached via `client.zones`,
`client.wlans`, `client.wlan_groups`, `client.access_points`, `client.ap_groups`).

## Spec-driven models

The controller serves a Swagger 2.0 document at `/wsg/apiDoc/openapi`. Model
metadata is generated from it rather than hand-written:

| Step | Tool | Reads → writes |
|------|------|----------------|
| fetch | `tools/fetch_spec.py` | controller → `spec/raw/all.json` + `spec/raw/manifest.json` |
| generate | `tools/generate_models.py` | `spec/raw/all.json` → `ruckus_smartzone/generated/models/` |
| validate | `tools/validate_spec.py` | `spec/raw/all.json` |

`fetch_spec.sanitize_spec()` overwrites the spec's `host` with a placeholder (so
no controller address is committed and the checked-in spec is host-independent)
and normalises a defined set of vendor conformance quirks in place — `type: file`
response schemas, typed string defaults, out-of-enum defaults, and `{name:regex}`
path templates — so the spec validates. The runtime base URL is supplied by the
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
| `ruckus_smartzone/resources/` | Dict-first zone/WLAN/WLAN-group/access-point/AP-group resource wrappers |
| `ruckus_smartzone/generated/models/` | Generated schema index (committed artifact) |

Repo root: `tools/`, `spec/`, `tests/`, `Makefile`, `pyproject.toml`.

## Conventions

- **Distribution** `ruckus-smartzone`; **import** `ruckus_smartzone`.
- **Entry point:** `from ruckus_smartzone import SmartZoneClient`, used as a context
  manager so the ticket is released on exit.
- **Public API is dict-first**; the generated schema index is an internal artifact.
- **Errors** derive from `SmartZoneAPIError`, carrying `status_code` and `response_data`.
- **HTTP transport** is synchronous `httpx`-based. The service ticket rides as a URL
  query parameter and is masked wherever a URL is logged.

## Testing

- Full suite: `make tests` (`lint`, `type-check`, `unit-tests`).
- Tests in `tests/` use `pytest` with `respx` for HTTP isolation; pipeline tools
  are tested offline with inline spec fixtures (no live controller).

## Where to look

- **Index:** [INDEX.md](INDEX.md)
- **Decision records:** [adr/](adr/) — API version (0001), auth/transport (0002),
  zone/WLAN/group wrappers (0003), access points (0004), AP groups (0005)
- **Memory:** [.agents/memory/python-ruckus-smartzone-repository-memory.md](../.agents/memory/python-ruckus-smartzone-repository-memory.md)
