---
name: paper-image
description: Design and generate scientific paper figures, graphical abstracts, method overviews, framework diagrams, architecture diagrams, pipelines and figure revisions. Use when asked to 画科研图、论文主图、课题框架图、模型架构图、方法流程图 or to turn a scientific method and optional references into a new figure using the current app's image tool or editable vector output.
---

# Paper Image

Create the requested figure using the current host's signed-in capabilities. The skill requires no service credentials, API clients, relays, or paid API setup. Use the steps below in the same turn when possible.

## 1. Establish the scientific content

- Read the supplied method, visual references, and constraints. Extract the figure's purpose, main takeaway, panel roles, exact labels, and directed relationships. Use only confirmed claims and values. Use only supplied measurements and performance annotations. Avoid inventing intermediate scientific stages.
- For a revision, inspect or attach the existing figure and preserve unrelated content and layout. Apply only the requested changes.
- Choose a visual form that serves the task. A conceptual illustration or graphical abstract communicates the main idea. A pipeline follows the data flow. A framework exposes interactions and feedback. An architecture diagram shows internal modules and connections.
- Use the requested language and aspect ratio. For an unspecified paper overview, start with a compact landscape composition and short labels. Ask a focused question only when missing information would change scientific meaning or make the requested figure infeasible.

## 2. Learn from references

- Prioritize images the user supplies. For a new visual overview without adequate references, use the host's available search or browsing to find two to four relevant figures in the [Top-Conf Paper Figure Gallery](https://qwdwqfwq.github.io/topconf-paper-figure-gallery/) or the source papers. Search by topic and visual form. Use generic public search terms for unpublished work.
- Inspect any available reference images for reading order, panel placement, grouping, line styles, visual density and typography. Reuse these principles in an original arrangement. Keep reference text, scientific content, and distinctive artwork out of the new figure. Include links for references actually used. If images cannot be inspected, use the supplied material and describe any public links as uninspected.
- Use the host's normal file or attachment tools where supported. If reference retrieval is unavailable, continue from the user brief and any attachments. Attach reference images to the native generator only when supported and useful.

## 3. Build a figure brief and render it

Write a short internal brief with the canvas, panel placement, exact labels, arrow endpoints and direction, palette, and output format. Include a clear cue for distinct roles such as data, process, state, and feedback. For image generation only, turn the brief into a concise visual prompt. Keep short in-image labels in quotation marks and specify where they appear. If the user asks only for a brief or prompt, deliver that and stop here.

- **Illustrative image or requested bitmap.** Invoke the current host's built-in image-generation or image-editing capability. In Codex, use the built-in image tool or `$imagegen` if available. In Antigravity, use its native image tool. In Gemini Apps, generate inside the current conversation with the built-in image feature. Provide the source image for an edit if the host supports it. Deliver the generated image where the host returns it.
- **Exact scientific diagram or editable figure.** Produce a vector figure with editable text and shapes, preferably SVG or the requested editable format. Use vector or plotting tools for exact labels, connections, quantitative plots, and publication layouts that require reproducible geometry. For a mixed figure, render result panels from their data and compose them with the conceptual panels. Return the actual file when the host supports files. If it only supports text, provide the complete vector source and say which format it represents.
- **Native image tool unavailable.** For a schematic that can be drawn accurately, deliver an editable SVG where feasible. If raster illustration is essential, give a ready-to-run prompt for the user's signed-in image app and say that this session could not generate the bitmap. Keep all requests within the native session or local drawing tools. Never ask for credentials or automate another consumer app from this skill.

## 4. Check and deliver

- Inspect the returned image or render the vector when the host can. Compare labels, arrows and any numerical values against the brief. Check legibility, clipping, spacing and overlaps. Fix any material defect before handing off if the available tools allow. When a bitmap repeatedly misrenders critical text or links, use an editable vector for the affected schematic.
- Provide the actual artifact and format, used reference links, and any material accuracy checks still open. Report generation or validation as complete only when performed.
