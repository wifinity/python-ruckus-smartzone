# Spec store

The SmartZone client is spec-driven: model metadata is generated from the
controller's Swagger 2.0 documents rather than hand-written. The controller
serves two, both unauthenticated:

| Spec | Served at | Raw file | Schema index |
|------|-----------|----------|--------------|
| `wsg` (public API) | `/wsg/apiDoc/openapi` | `raw/all.json` | `generated/models/schema_index.py` |
| `switchm` (Switch Manager) | `/switchm/api/openapi` | `raw/switchm.json` | `generated/models/switchm_schema_index.py` |

## Pipeline

```
make spec-fetch-controller SMARTZONE_BASE_URL=https://<controller>:8443
make generate-models
make spec-validate
```

- `spec-fetch` / `spec-fetch-controller` — download each spec, overwrite the
  baked-in `host` with a placeholder, and write the raw files plus
  `raw/manifest.json`. Pass `SPEC_FETCH_ARGS="--spec switchm ..."` to
  `spec-fetch` to fetch one spec only.
- `generate-models` — read each raw spec's `definitions` and write its committed
  schema index under `ruckus_smartzone/generated/models/`. The tool takes
  `--spec` too.
- `spec-validate` — validate every raw spec present.

## Layout

| Path | Contents |
|------|----------|
| `raw/all.json` | Fetched `wsg` spec, `host` sanitised |
| `raw/switchm.json` | Fetched `switchm` spec, `host` sanitised |
| `raw/manifest.json` | One entry per spec: `source`, `spec_info_version`, `spec_sha256`, `fetched_at` — never the host |

## Sanitisation and normalisation

The controller address is never committed: `host` is replaced with a
host-agnostic placeholder on fetch, and the SDK supplies the real base URL at
runtime.

The fetch step also normalises a defined set of vendor-spec conformance quirks
in place so the checked-in specs validate:

- `type: file` response schemas become binary bodies.
- String defaults on numeric/boolean fields are coerced to their type.
- A default outside its own `enum` is dropped.
- `{name:regex}` path templates (and their parameter names) are reduced to
  `{name}`.
- Repeated `produces`/`consumes` entries are collapsed.
- A parameter repeated in one `parameters` list is collapsed.
