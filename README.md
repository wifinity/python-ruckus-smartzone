# Ruckus SmartZone Python Client

A Python client library for the Ruckus SmartZone (vSZ) public REST API,
targeting API version `v13_1`.

> **Status:** early scaffold. Build tooling, the spec-driven pipeline, the test
> harness and the exception/logging foundation are in place; the HTTP client,
> authentication and resource wrappers are not yet implemented.

## Installation

From source:

```bash
git clone https://github.com/wifinity/python-ruckus-smartzone.git
cd python-ruckus-smartzone
pip install -e ".[dev]"
```

## Development

```bash
make venv     # create .venv and install dependencies (uv)
make tests    # lint, type-check and unit tests
make format   # apply black formatting
```

## Spec-driven models

Model metadata is generated from the controller's Swagger 2.0 document rather
than hand-written:

```bash
make spec-fetch-controller SMARTZONE_BASE_URL=https://<controller>:8443
make generate-models
make spec-validate
```

The controller address is never committed — the fetch step replaces the spec's
`host` with a placeholder. See [spec/README.md](spec/README.md).

## Scope

Zones, WLANs, WLAN groups and their members, and access points.
