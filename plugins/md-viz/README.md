# MD-Viz Plugin (`v0.3.0`, MIT)

High-impact, full-arsenal Markdown visualization skill for **Antigravity CLI (`agy`)**, **Claude Code**, and **Codex**.

## Install

- **Claude Code (in-session one-step, 2.1.275+):** `/plugin install md-viz --marketplace Technoetic/md-viz`
- **Claude Code CLI:** `claude plugin marketplace add Technoetic/md-viz && claude plugin install md-viz@technoetic-md-viz`
- **Antigravity CLI:** `agy plugin install https://github.com/Technoetic/md-viz/tree/main/plugins/md-viz`
- **Codex CLI:** `codex plugin marketplace add Technoetic/md-viz && codex plugin add md-viz@technoetic-md-viz`

## What Is Included

- `skills/md-viz/SKILL.md` — Maximalist visual-overdrive orchestration rules covering **25 visualization libraries** (9 structure/signal/music + 12 data/chart/network/map + 4 code/math) and **6 core GitHub Markdown techniques + 4 native layout boosters** (styled live Mermaid, live LaTeX math, multi-column `<details>` gallery walls, `<kbd>` pills).
- `skills/md-viz/references/markdown-patterns.md` — Copy-ready templates for neon badge banners, live GeoJSON maps, styled Mermaid pipelines, native LaTeX equations, `<picture>` reduced-motion GIFs, column-aligned annotated directory trees, and all 5 GitHub alerts.
- `skills/md-viz/scripts/badge.py` — Zero-dependency Python stdlib two-tone 28 px SVG badge generator with strict hex validation, WCAG contrast ink selection, East-Asian width calculation, and XML escaping.
- `skills/md-viz/scripts/check_env.py` — Zero-dependency read-only preflight script that detects which of the 25 visualization engines are locally available.

## Quick Commands

```sh
# 1. Inspect locally available renderers (0 dependencies)
python skills/md-viz/scripts/check_env.py

# 2. Generate a vivid two-tone neon SVG badge
python skills/md-viz/scripts/badge.py GALLERY "25 TOOLS" badge.svg --color "#C8EF51"
```

## Full Showcase & Documentation

- English Showcase & Live 25-Tool Gallery: [Repository README](https://github.com/Technoetic/md-viz)
- Korean Showcase: [README.ko.md](https://github.com/Technoetic/md-viz/blob/main/README.ko.md)
- License: [MIT](LICENSE)
