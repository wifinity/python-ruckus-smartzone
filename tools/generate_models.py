"""Generate lightweight internal model metadata from the fetched spec.

Reads the Swagger 2.0 ``definitions`` block and writes a stable, committed
schema index. Generated artifacts stay internal while the public API remains
dict-first.
"""

from __future__ import annotations

import json
from pathlib import Path
from pprint import pformat

import black

RAW_SPEC_PATH = Path("spec/raw/all.json")
MODELS_DIR = Path("ruckus_smartzone/generated/models")
MODELS_FILE = MODELS_DIR / "schema_index.py"


def main() -> None:
    if not RAW_SPEC_PATH.exists():
        raise SystemExit(f"Missing spec at {RAW_SPEC_PATH}. Run make spec-fetch first.")

    spec = json.loads(RAW_SPEC_PATH.read_text(encoding="utf-8"))
    definitions = spec.get("definitions", {})

    schema_index = {name: definitions[name] for name in sorted(definitions.keys())}
    content = (
        '"""Auto-generated schema index from the Swagger 2.0 spec.\n'
        "Do not edit manually.\n"
        '"""\n\n'
        f"SCHEMA_INDEX: dict[str, dict] = {pformat(schema_index, width=88)}\n"
    )

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    (MODELS_DIR / "__init__.py").write_text(
        '"""Generated internal model helpers."""\n\n'
        "from .schema_index import SCHEMA_INDEX as SCHEMA_INDEX\n",
        encoding="utf-8",
    )
    formatted_content = black.format_str(content, mode=black.Mode())
    MODELS_FILE.write_text(formatted_content, encoding="utf-8")
    print(f"Generated {MODELS_FILE} ({len(schema_index)} definitions)")


if __name__ == "__main__":
    main()
