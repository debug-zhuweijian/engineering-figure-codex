#!/usr/bin/env python3
"""Build a Codex Desktop image-generation prompt from a figure brief."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_PATH = ROOT / "assets" / "prompt_templates.json"

REQUIRED_FIELDS = {
    "title",
    "mode",
    "language",
    "audience",
    "background",
    "must_include",
    "style_constraints",
    "negative_constraints",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_list(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def validate_brief(brief: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(brief))
    if missing:
        raise SystemExit(f"Brief is missing required fields: {', '.join(missing)}")

    mode = brief["mode"]
    if mode not in {"concept", "mixed"}:
        raise SystemExit("build_prompt.py only supports concept or mixed briefs.")

    language = brief["language"]
    if language not in {"zh", "en"}:
        raise SystemExit("Brief language must be 'zh' or 'en'.")


def build_prompt(brief: dict[str, Any]) -> str:
    validate_brief(brief)
    templates = load_json(TEMPLATES_PATH)
    mode = brief["mode"]
    language = brief["language"]
    template = templates[mode][language]

    prompt = template.format(
        title=brief["title"],
        audience=brief["audience"],
        background=brief["background"],
        must_include=normalize_list(brief["must_include"]),
        style_constraints=normalize_list(brief["style_constraints"]),
        negative_constraints=normalize_list(brief["negative_constraints"]),
    )

    return (
        prompt
        + "\n\nCodex Desktop boundary: generate the image in the current Codex conversation. "
        + "Do not call a Python image provider, reverse proxy, or external image API for this default workflow."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an engineering figure prompt from a brief JSON file.")
    parser.add_argument("--brief", required=True, help="Path to a figure brief JSON file.")
    parser.add_argument("--out", required=True, help="Output Markdown prompt path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    brief_path = Path(args.brief)
    out_path = Path(args.out)
    brief = load_json(brief_path)
    if not isinstance(brief, dict):
        raise SystemExit("Brief JSON must be an object.")

    prompt = build_prompt(brief)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(prompt + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

