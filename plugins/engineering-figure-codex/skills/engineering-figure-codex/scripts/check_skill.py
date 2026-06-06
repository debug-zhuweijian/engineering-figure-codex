#!/usr/bin/env python3
"""Offline validation for the Engineering Figure Codex skill."""

from __future__ import annotations

import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_ROOT.parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]


def require_file(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path}")


def load_json(path: Path) -> dict:
    with path.open("rb") as raw:
        prefix = raw.read(3)
        if prefix == b"\xef\xbb\xbf":
            raise SystemExit(f"JSON file must be UTF-8 without BOM: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return payload


def main() -> int:
    required = [
        REPO_ROOT / ".agents" / "plugins" / "marketplace.json",
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "assets" / "prompt_templates.json",
        SKILL_ROOT / "references" / "workflow.md",
        SKILL_ROOT / "references" / "prompt-style.md",
        SKILL_ROOT / "references" / "plot-rules.md",
        REPO_ROOT / "examples" / "rag-architecture.brief.json",
        REPO_ROOT / "examples" / "benchmark.plot-spec.json",
    ]
    for path in required:
        require_file(path)

    marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    if marketplace.get("name") != "engineering-figure-codex":
        raise SystemExit("Marketplace name must be engineering-figure-codex.")
    plugin_path = marketplace["plugins"][0]["source"]["path"]
    if plugin_path != "./plugins/engineering-figure-codex":
        raise SystemExit("Marketplace plugin path is incorrect.")

    plugin = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    forbidden = {"mcpServers", "apps", "hooks"}
    present_forbidden = sorted(forbidden & set(plugin))
    if present_forbidden:
        raise SystemExit(f"Plugin manifest must not declare: {', '.join(present_forbidden)}")
    if plugin.get("skills") != "./skills/":
        raise SystemExit("Plugin manifest must point skills to ./skills/.")

    templates = load_json(SKILL_ROOT / "assets" / "prompt_templates.json")
    for mode in ("concept", "mixed"):
        for language in ("zh", "en"):
            if not templates.get(mode, {}).get(language):
                raise SystemExit(f"Missing prompt template: {mode}/{language}")

    load_json(REPO_ROOT / "examples" / "rag-architecture.brief.json")
    load_json(REPO_ROOT / "examples" / "benchmark.plot-spec.json")
    print("Engineering Figure Codex offline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

