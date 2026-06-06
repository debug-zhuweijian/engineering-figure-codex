#!/usr/bin/env python3
"""Render exact publication-style plots from a compact JSON spec."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {"chart_type", "title", "data", "x", "y", "units", "formats"}


def load_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    if not isinstance(spec, dict):
        raise SystemExit("Plot spec must be a JSON object.")
    missing = sorted(REQUIRED_FIELDS - set(spec))
    if missing:
        raise SystemExit(f"Plot spec is missing required fields: {', '.join(missing)}")
    if not isinstance(spec["data"], list) or not spec["data"]:
        raise SystemExit("Plot spec data must be a non-empty list.")
    return spec


def unique_in_order(values: list[Any]) -> list[Any]:
    seen = set()
    result = []
    for value in values:
        key = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def axis_label(field: str, units: dict[str, str]) -> str:
    unit = units.get(field)
    return f"{field} ({unit})" if unit else field


def render_bar(ax: Any, spec: dict[str, Any]) -> None:
    data = spec["data"]
    x_field = spec["x"]
    y_field = spec["y"]
    series_field = spec.get("series")
    categories = unique_in_order([row[x_field] for row in data])

    if series_field:
        series_values = unique_in_order([row[series_field] for row in data])
        grouped: dict[Any, dict[Any, float]] = defaultdict(dict)
        for row in data:
            grouped[row[series_field]][row[x_field]] = float(row[y_field])
        width = 0.8 / max(len(series_values), 1)
        positions = list(range(len(categories)))
        for index, series in enumerate(series_values):
            offset = (index - (len(series_values) - 1) / 2) * width
            heights = [grouped[series].get(category, 0.0) for category in categories]
            ax.bar([pos + offset for pos in positions], heights, width=width, label=str(series))
        ax.set_xticks(positions)
        ax.set_xticklabels([str(category) for category in categories])
        ax.legend(frameon=False)
    else:
        heights = [float(row[y_field]) for row in data]
        ax.bar([str(category) for category in categories], heights, width=0.72)


def render_line_or_scatter(ax: Any, spec: dict[str, Any], *, scatter: bool) -> None:
    data = spec["data"]
    x_field = spec["x"]
    y_field = spec["y"]
    series_field = spec.get("series")

    if series_field:
        grouped: dict[Any, list[dict[str, Any]]] = defaultdict(list)
        for row in data:
            grouped[row[series_field]].append(row)
        for series, rows in grouped.items():
            x_values = [row[x_field] for row in rows]
            y_values = [float(row[y_field]) for row in rows]
            if scatter:
                ax.scatter(x_values, y_values, label=str(series), s=42)
            else:
                ax.plot(x_values, y_values, marker="o", label=str(series), linewidth=2)
        ax.legend(frameon=False)
    else:
        x_values = [row[x_field] for row in data]
        y_values = [float(row[y_field]) for row in data]
        if scatter:
            ax.scatter(x_values, y_values, s=42)
        else:
            ax.plot(x_values, y_values, marker="o", linewidth=2)


def render_heatmap(ax: Any, spec: dict[str, Any]) -> None:
    data = spec["data"]
    x_field = spec["x"]
    y_field = spec["y"]
    value_field = spec.get("value") or spec.get("z")
    if not value_field:
        raise SystemExit("Heatmap specs require a 'value' or 'z' field.")

    x_values = unique_in_order([row[x_field] for row in data])
    y_values = unique_in_order([row[y_field] for row in data])
    matrix = [[0.0 for _ in x_values] for _ in y_values]
    x_index = {value: index for index, value in enumerate(x_values)}
    y_index = {value: index for index, value in enumerate(y_values)}
    for row in data:
        matrix[y_index[row[y_field]]][x_index[row[x_field]]] = float(row[value_field])

    image = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(x_values)))
    ax.set_xticklabels([str(value) for value in x_values])
    ax.set_yticks(range(len(y_values)))
    ax.set_yticklabels([str(value) for value in y_values])
    ax.figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)


def render(spec: dict[str, Any], out_dir: Path, formats: list[str]) -> list[Path]:
    import matplotlib.pyplot as plt

    chart_type = spec["chart_type"]
    if chart_type not in {"bar", "line", "scatter", "heatmap"}:
        raise SystemExit("chart_type must be one of: bar, line, scatter, heatmap.")

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 10,
        }
    )

    fig, ax = plt.subplots(figsize=tuple(spec.get("figsize", [7.2, 4.6])))
    if chart_type == "bar":
        render_bar(ax, spec)
    elif chart_type == "line":
        render_line_or_scatter(ax, spec, scatter=False)
    elif chart_type == "scatter":
        render_line_or_scatter(ax, spec, scatter=True)
    else:
        render_heatmap(ax, spec)

    units = spec.get("units") or {}
    ax.set_title(spec["title"], pad=12)
    ax.set_xlabel(axis_label(spec["x"], units))
    ax.set_ylabel(axis_label(spec["y"], units))
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()

    out_dir.mkdir(parents=True, exist_ok=True)
    slug = spec.get("slug", "figure")
    outputs = []
    for fmt in formats:
        path = out_dir / f"{slug}.{fmt}"
        fig.savefig(path, dpi=spec.get("dpi", 220), bbox_inches="tight")
        outputs.append(path)
    plt.close(fig)
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an exact plot from JSON.")
    parser.add_argument("--spec", required=True, help="Path to a plot spec JSON file.")
    parser.add_argument("--out-dir", required=True, help="Output directory.")
    parser.add_argument("--formats", nargs="+", default=None, help="Output formats, e.g. png svg pdf.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    spec = load_spec(Path(args.spec))
    formats = args.formats or spec.get("formats") or ["png", "svg", "pdf"]
    outputs = render(spec, Path(args.out_dir), formats)
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

