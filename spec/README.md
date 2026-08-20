# Spec store

The SmartZone client is spec-driven: model metadata is generated from the
controller's Swagger 2.0 document rather than hand-written.

## Pipeline

```
make spec-fetch-controller SMARTZONE_BASE_URL=https://<controller>:8443
make generate-models
make spec-validate
```

- `spec-fetch` / `spec-fetch-controller` — download `{base}/wsg/apiDoc/openapi`,
  overwrite the baked-in `host` with a placeholder, and write `raw/all.json` plus
  `raw/manifest.json`.
- `generate-models` — read `raw/all.json` `definitions` and write the committed
  schema index under `ruckus_smartzone/generated/models/`.
- `spec-validate` — validate `raw/all.json`.

## Layout

| Path | Contents |
|------|----------|
| `raw/all.json` | Fetched spec, `host` sanitised (committed once fetched) |
| `raw/manifest.json` | `source`, `spec_info_version`, `spec_sha256`, `fetched_at` — never the host |

## Sanitisation and normalisation

The controller address is never committed: `host` is replaced with a
host-agnostic placeholder on fetch, and the SDK supplies the real base URL at
runtime.

The fetch step also normalises a defined set of vendor-spec conformance quirks
in place so the checked-in spec validates: `type: file` response schemas become
binary bodies, string defaults on numeric/boolean fields are coerced to their
type, a default outside its own `enum` is dropped, and `{name:regex}` path
templates (and their parameter names) are reduced to `{name}`.

`raw/` is empty until a spec is fetched from a controller.
