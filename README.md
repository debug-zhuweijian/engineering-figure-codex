# Engineering Figure Codex

Engineering Figure Codex is a Codex Desktop plugin marketplace for engineering and research figures. It helps Codex prepare paper-style architecture diagrams, algorithm workflows, graphical abstracts, and exact local publication plots.

This plugin is built for Codex Desktop's plugin UI. The default workflow does not need image API keys, does not use image reverse proxies, and does not treat Codex Desktop image generation as a Python provider.

## Paper Figure for Codex, Antigravity, and Gemini

`paper-figure` is a standalone Agent Skill for scientific illustrations, paper overviews and editable method diagrams. It uses reference figures to plan the layout, then draws with the current app's built-in image tool or generates an editable vector. It requires no API key, relay, or extra service subscription. Image generation uses the host account's available features and quota.

[View SKILL.md](./plugins/engineering-figure-codex/skills/paper-figure/SKILL.md) · [Download SKILL.md](https://raw.githubusercontent.com/debug-zhuweijian/engineering-figure-codex/main/plugins/engineering-figure-codex/skills/paper-figure/SKILL.md)

| 平台 | 安装方式 | 如何调用 |
| --- | --- | --- |
| Codex | 从下面的 Marketplace 安装或更新插件。也可将下载的文件放到 `~/.agents/skills/paper-figure/SKILL.md` 作为全局 Skill。 | 选择或输入 `$paper-figure`。出位图时使用当前会话自带的图像工具。 |
| Antigravity | 将文件放到 `~/.gemini/config/skills/paper-figure/SKILL.md`。只在一个项目使用时，可放到项目的 `.agents/skills/paper-figure/SKILL.md`。 | 在 Antigravity App 输入 `/paper-figure`。在 IDE 的 Agent 面板可用自然语言点名 `paper-figure`。 |
| Gemini 网页 | 打开 Gemini 网页侧栏的 **Customize → Skills → Create → Upload**，上传 `SKILL.md` 并保存。 | 在对话输入 `/`（或新版的 `@`），选择 `paper-figure`。可在同一对话添加参考图并生成图像。 |

使用示例

- 使用 `paper-figure`，参考附件的布局，画一张 16:9 的英文方法概览图。请实际生成图片。
- 使用 `paper-figure`，按照我的方法描述输出可编辑 SVG，确保模块名称和箭头方向正确。

本 Skill 借鉴了 [Top-Conf Paper Figure Gallery / FigureForge](https://github.com/qwdwqfwq/topconf-paper-figure-gallery) 的参考图检索和版式分析流程。它通过宿主搜索访问公共图库，不打包论文图片。没有原生图像工具的会话可以绘制适合做成矢量图的内容，或为位图插画准备提示词。

官方说明 · [Codex Skills](https://learn.chatgpt.com/docs/build-skills) · [Codex Image Generation](https://learn.chatgpt.com/docs/image-generation) · [Antigravity Skills](https://antigravity.google/docs/skills) · [Gemini Apps Skills](https://support.google.com/gemini/answer/17094296)

## Install in Codex Desktop

1. Open Codex Desktop.
2. Go to Plugins.
3. Open the marketplace dropdown near the search box.
4. Click `+ 添加更多` / `+ Add more`.
5. Paste this repository URL:

```text
https://github.com/debug-zhuweijian/engineering-figure-codex
```

6. Confirm adding the marketplace.
7. Select `Engineering Figure Codex` from the marketplace dropdown.
8. Install or enable the `Engineering Figure Codex` plugin.
9. Start a new Codex thread before using it.

If the UI does not accept the full URL, try the repository shorthand:

```text
debug-zhuweijian/engineering-figure-codex
```

## What It Does

- `concept` mode: builds precise prompts for system architecture diagrams, algorithm workflows, graphical abstracts, and paper-style conceptual figures. Codex Desktop generates the image in the current conversation when image generation is available.
- `plot` mode: renders exact numeric figures locally from JSON plot specs.
- `mixed` mode: combines local exact plot panels with Codex-generated conceptual panels.

Codex Desktop image generation is a conversation tool. It is not a local Python API, HTTP provider, or MCP endpoint. The scripts in this plugin do not call image providers and do not read image API keys.

## Example Prompts

```text
使用 Engineering Figure Codex，画一个中文 RAG 系统架构图，包含 OCR、chunking、embedding、vector search、rerank、answer synthesis。
```

```text
Use Engineering Figure Codex to create an English paper-style method figure for my multimodal retrieval system.
```

```text
Use Engineering Figure Codex to render an exact benchmark plot from this data.
```

## Offline Scripts

Build a prompt from a brief:

```powershell
python .\plugins\engineering-figure-codex\skills\engineering-figure-codex\scripts\build_prompt.py `
  --brief .\examples\rag-architecture.brief.json `
  --out .\output\rag-prompt.md
```

Render an exact plot:

```powershell
python .\plugins\engineering-figure-codex\skills\engineering-figure-codex\scripts\render_plot.py `
  --spec .\examples\benchmark.plot-spec.json `
  --out-dir .\output\benchmark `
  --formats png svg pdf
```

Run offline checks:

```powershell
python .\plugins\engineering-figure-codex\skills\engineering-figure-codex\scripts\check_skill.py
```

## Related Project

Related project: [heyu-233/engineering-figure-agent](https://github.com/heyu-233/engineering-figure-agent).

Engineering Figure Codex is an independent Codex Desktop plugin marketplace. The related project is a useful reference for engineering figure workflows, but it is not this plugin's provider backend. If code or templates from that MIT-licensed project are copied in future versions, retain the required license and attribution.

## Optional CLI fallback

The Codex Desktop UI path above is the recommended installation route. Use CLI only for troubleshooting or automation when the UI path fails.

```powershell
codex plugin marketplace add https://github.com/debug-zhuweijian/engineering-figure-codex --ref main
codex plugin add engineering-figure-codex@engineering-figure-codex
```

To refresh a Git marketplace snapshot from CLI:

```powershell
codex plugin marketplace upgrade engineering-figure-codex
codex plugin add engineering-figure-codex@engineering-figure-codex
```

After installing or upgrading, start a new Codex thread so the skill is loaded.

## Failure Handling

- If the plugin marketplace does not appear after adding it, check that this repository contains `.agents/plugins/marketplace.json`.
- If the plugin appears but does not install, check `plugins/engineering-figure-codex/.codex-plugin/plugin.json`.
- If the skill does not trigger, start a new Codex thread and mention `Engineering Figure Codex` explicitly.
- If image generation is unavailable in the current conversation, the skill should produce prompt-only output and should not claim that an image was generated.

## License

MIT

