---
name: engineering-figure-codex
description: Use when the user needs engineering or research-paper figures in Codex Desktop, including system architecture diagrams, algorithm workflows, graphical abstracts, benchmark charts, ablation plots, heatmaps, scatter plots, exact publication-style plots from numeric data, or figure prompts for Codex image generation. This skill separates Codex Desktop conversational image generation from local deterministic plotting.
---

# Engineering Figure Codex

Use this skill for engineering figures, paper figures, architecture diagrams, algorithm workflows, graphical abstracts, and exact benchmark plots.

## Boundary

This is a Codex Desktop workflow skill, not an image provider. Codex Desktop image generation is a tool available to the current agent conversation. It is not a Python API, local HTTP endpoint, MCP server, or script provider.

Do not ask for OpenAI, Gemini, Banana, or relay API keys for the default workflow. Do not route image prompts through a third-party reverse proxy. Do not claim that local scripts can call Codex Desktop image generation directly.

If the current conversation has an image generation tool, use it for conceptual figures after building a precise prompt. If the current conversation has no image generation tool, produce a prompt-only handoff and say that image generation is unavailable in this conversation.

## Mode Selection

- `concept`: system architecture diagrams, algorithm workflows, hardware/software schematics, graphical abstracts, and paper-style conceptual panels. Build a final prompt, then call the current Codex conversation image tool when available.
- `plot`: exact numeric figures such as benchmark bars, ablation plots, trend curves, heatmaps, and scatter plots. Use local plotting scripts and real data only.
- `mixed`: combine local exact plots with conceptual panels. Render numeric panels locally first, then generate conceptual panels in the Codex conversation.

Never use image generation for exact values, axes, error bars, table geometry, benchmark rankings, or quantitative claims.

## Workflow

1. Decide whether the request is `concept`, `plot`, or `mixed`.
2. For concept work, create or infer a concise figure brief. Use `scripts/build_prompt.py` when the user provides a brief JSON or when a reusable prompt artifact is useful.
3. For plot work, require real numeric data. Use `scripts/render_plot.py` with a plot spec and save PNG/SVG/PDF outputs.
4. For mixed work, render numeric panels before generating conceptual panels.
5. Save stable local artifacts when producing files: brief JSON, prompt Markdown, plot spec, and exact plot files.
6. For conceptual images, call the current Codex conversation image generation tool when available. Otherwise provide the final prompt only.
7. Keep labels short, claims grounded, and visual hierarchy publication-oriented.

## References

Load only what is needed:

- `references/workflow.md`: mode details and artifact boundaries.
- `references/prompt-style.md`: publication prompt style and Chinese/English label rules.
- `references/plot-rules.md`: deterministic plotting rules and supported spec shape.

## Scripts

Build an image prompt from a brief:

```bash
python scripts/build_prompt.py --brief ../../../../examples/rag-architecture.brief.json --out output/rag-prompt.md
```

Render an exact plot:

```bash
python scripts/render_plot.py --spec ../../../../examples/benchmark.plot-spec.json --out-dir output/benchmark --formats png svg pdf
```

Run offline checks:

```bash
python scripts/check_skill.py
```

All scripts are offline by default. They do not read API keys and do not access network image providers.

## Output Rules

- Concept prompts should specify diagram purpose, panels, modules, arrows, labels, layout, style, and negative constraints.
- Use Chinese labels when the user asks in Chinese unless they request English.
- Preserve standard technical notation when it improves clarity.
- Use white or light neutral backgrounds for research figures unless the user requests another style.
- Keep dense but readable information hierarchy for paper and group-meeting figures.
- For local plots, include units, axis labels, legend, and deterministic output formats.

