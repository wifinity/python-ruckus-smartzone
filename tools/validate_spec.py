"""Validate the fetched Swagger 2.0 specification."""

from __future__ import annotations

import json
from pathlib import Path

try:  # openapi-spec-validator >= 0.7 exposes validate(); older exposes validate_spec()
    from openapi_spec_validator import validate as _validate
except ImportError:  # pragma: no cover
    from openapi_spec_validator import validate_spec as _validate

RAW_SPEC_PATH = Path("spec/raw/all.json")


def main() -> None:
    if not RAW_SPEC_PATH.exists():
        raise SystemExit(f"Missing spec at {RAW_SPEC_PATH}. Run make spec-fetch first.")
    spec = json.loads(RAW_SPEC_PATH.read_text(encoding="utf-8"))
    _validate(spec)
    print(f"Validated {RAW_SPEC_PATH}")


if __name__ == "__main__":
    main()
