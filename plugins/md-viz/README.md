# MD-Viz Plugin (`v0.4.0`, MIT)

**Zero-install GitHub `README.md` visual engine** for **Antigravity CLI (`agy`)**, **Claude Code**, and **Codex**.

Zero `npm install`, zero `pip install`, zero external binaries — every bundled generator runs strictly on the **Python 3 standard library** and pairs seamlessly with GitHub's native Markdown renderers (`Mermaid`, `MathJax`, `GeoJSON`, Alerts `5/5`).

## Install

- **Claude Code (in-session one-step, 2.1.275+):** `/plugin install md-viz --marketplace Technoetic/md-viz`
- **Claude Code CLI:** `claude plugin marketplace add Technoetic/md-viz && claude plugin install md-viz@technoetic-md-viz`
- **Antigravity CLI:** `agy plugin install https://github.com/Technoetic/md-viz/tree/main/plugins/md-viz`
- **Codex CLI:** `codex plugin marketplace add Technoetic/md-viz && codex plugin add md-viz@technoetic-md-viz`

## What Is Included (100% Python 3 Stdlib — 0 External Installs)

- `skills/md-viz/SKILL.md` — Dedicated zero-install GitHub `README.md` visualization workflow combining GitHub-native live syntax with the 4 bundled Python stdlib generators.
- `skills/md-viz/references/markdown-patterns.md` — Copy-ready templates for live Mermaid, MathJax, GeoJSON, 5/5 alerts, `<picture>` GIF/PNG, neon badge banners, pure SVG chart JSON specs, and aligned directory trees.
- `skills/md-viz/scripts/badge.py` — 28 px two-tone neon SVG badge generator (strict 6-digit hex, WCAG ink contrast, East-Asian width, XML escaping).
- `skills/md-viz/scripts/svg_chart.py` — **10 GitHub `<img>`-safe pure dark-neon SVG visual types** (`hero`, `kpi`, `bar`, `line`, `donut`, `heatmap`, `waterfall`, `radar`, `sankey`, `timeline`) with built-in `<script>`/`<foreignObject>` rejection and idempotent `--readme --slot` embedding.
- `skills/md-viz/scripts/gif_anim.py` — Pure-stdlib animated **GIF89a + identical-dimension reduced-motion PNG** generator emitting ready-to-paste `<picture>` HTML.
- `skills/md-viz/scripts/tree_gen.py` — Real-filesystem directory tree formatter with exact East-Asian single-column `← role` alignment.
- `skills/md-viz/scripts/check_env.py` — Read-only preflight verifying the zero-install stack and optional external renderers.

## Quick Commands (0 Dependencies)

```sh
# 1. Verify the zero-install GitHub README stack
python skills/md-viz/scripts/check_env.py

# 2. Generate a two-tone neon SVG badge
python skills/md-viz/scripts/badge.py ZERO-DEPS "PYTHON STDLIB" badge.svg --color "#00F5D4"

# 3. Generate a pure GitHub-safe dark-neon SVG chart & embed into README.md
python skills/md-viz/scripts/svg_chart.py --type kpi --spec kpi.json --out docs/art/kpi.svg --readme README.md --slot kpi

# 4. Generate a looping animated GIF89a + reduced-motion PNG <picture> pair
python skills/md-viz/scripts/gif_anim.py --spec loop.json --out docs/art/loop.gif --readme README.md --slot loop

# 5. Generate a real-repo column-aligned directory tree
python skills/md-viz/scripts/tree_gen.py --root . --max-depth 3
```

## Full Showcase & Documentation

- English Showcase: [Repository README](https://github.com/Technoetic/md-viz)
- Korean Showcase: [README.ko.md](https://github.com/Technoetic/md-viz/blob/main/README.ko.md)
- License: [MIT](LICENSE)
