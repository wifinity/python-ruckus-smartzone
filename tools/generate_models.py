"""Generate lightweight internal model metadata from the fetched specs.

Reads each Swagger 2.0 spec's ``definitions`` block and writes a stable,
committed schema index per spec. Generated artifacts stay internal while the
public API remains dict-first.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from pprint import pformat

import black

RAW_DIR = Path("spec/raw")
MODELS_DIR = Path("ruckus_smartzone/generated/models")

# Spec name -> (raw spec file under RAW_DIR, module name, index constant).
SPECS: dict[str, tuple[str, str, str]] = {
    "wsg": ("all.json", "schema_index", "SCHEMA_INDEX"),
    "switchm": ("switchm.json", "switchm_schema_index", "SWITCHM_SCHEMA_INDEX"),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the internal schema index from the fetched specs."
    )
    parser.add_argument(
        "--spec",
        action="append",
        choices=sorted(SPECS),
        help="Spec to generate from; repeatable. Defaults to every spec.",
    )
    return parser.parse_args(argv)


def render_index(spec: dict, constant: str) -> str:
    """Return the black-formatted module source for one spec's schema index."""
    definitions = spec.get("definitions", {})
    schema_index = {name: definitions[name] for name in sorted(definitions.keys())}
    content = (
        '"""Auto-generated schema index from the Swagger 2.0 spec.\n'
        "Do not edit manually.\n"
        '"""\n\n'
        f"{constant}: dict[str, dict] = {pformat(schema_index, width=88)}\n"
    )
    return black.format_str(content, mode=black.Mode())


def write_package_init() -> None:
    """Export the index constant of every generated module that exists."""
    lines = ['"""Generated internal model helpers."""', ""]
    for _, module, constant in SPECS.values():
        if (MODELS_DIR / f"{module}.py").exists():
            lines.append(f"from .{module} import {constant} as {constant}")
    (MODELS_DIR / "__init__.py").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    names = [name for name in SPECS if name in set(args.spec or SPECS)]

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for name in names:
        raw_file, module, constant = SPECS[name]
        raw_path = RAW_DIR / raw_file
        if not raw_path.exists():
            raise SystemExit(f"Missing spec at {raw_path}. Run make spec-fetch first.")
        spec = json.loads(raw_path.read_text(encoding="utf-8"))
        target = MODELS_DIR / f"{module}.py"
        target.write_text(render_index(spec, constant), encoding="utf-8")
        print(f"Generated {target} ({len(spec.get('definitions', {}))} definitions)")

    write_package_init()


if __name__ == "__main__":
    main()
