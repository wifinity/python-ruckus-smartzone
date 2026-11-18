"""Validate the fetched Swagger 2.0 specifications."""

from __future__ import annotations

import json
from pathlib import Path

try:  # openapi-spec-validator >= 0.7 exposes validate(); older exposes validate_spec()
    from openapi_spec_validator import validate as _validate
except ImportError:  # pragma: no cover
    from openapi_spec_validator import validate_spec as _validate

RAW_DIR = Path("spec/raw")
SPEC_FILES = ("all.json", "switchm.json")


def main() -> None:
    present = [RAW_DIR / name for name in SPEC_FILES if (RAW_DIR / name).exists()]
    if not present:
        raise SystemExit(f"No spec found in {RAW_DIR}. Run make spec-fetch first.")
    for path in present:
        _validate(json.loads(path.read_text(encoding="utf-8")))
        print(f"Validated {path}")


if __name__ == "__main__":
    main()
