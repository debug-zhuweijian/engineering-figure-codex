# Plot Rules

Use local plotting for exact values.

Supported chart types:

- `bar`
- `line`
- `scatter`
- `heatmap`

Minimum plot spec fields:

- `chart_type`
- `title`
- `data`
- `x`
- `y`
- `series`
- `units`
- `formats`

Rules:

- Preserve exact numeric values.
- Use deterministic ordering from the input data unless the spec gives another order.
- Include units in axis labels when available.
- Include a legend when `series` is present and non-empty.
- Save every requested format.
- Do not smooth, normalize, or aggregate unless explicitly requested in the spec.

