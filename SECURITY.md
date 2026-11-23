# Security Policy

## Scope

`md-viz` distributes zero-install GitHub `README.md` visualization instructions and five Python 3 standard-library scripts under `plugins/md-viz/skills/md-viz/scripts/`:

- `badge.py` — 28 px two-tone neon SVG badge generator
- `svg_chart.py` — 10 GitHub `<img>`-safe pure-SVG chart and banner generators (`hero`, `kpi`, `bar`, `line`, `donut`, `heatmap`, `waterfall`, `radar`, `sankey`, `timeline`)
- `gif_anim.py` — Pure-stdlib animated GIF89a + identical-dimension reduced-motion PNG generator
- `tree_gen.py` — Real-repository column-aligned annotated directory tree formatter
- `check_env.py` — Read-only preflight inspection script

### Security Boundaries

- **Pure GitHub-safe SVG generation (`badge.py`, `svg_chart.py`):** Validates strict 6-digit hex color values (`#RRGGBB`), XML-escapes all user text, validates slot identifiers (`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`), rejects unsafe link schemes (`javascript:`, `data:`, `vbscript:`), and parses every emitted SVG to block `<script>`, `<foreignObject>`, `<iframe>`, `<embed>`, `<object>`, `javascript:`, and `on*=` event attributes.
- **Pure-stdlib binary encoding (`gif_anim.py`):** Encodes indexed GIF89a and PNG files strictly with Python stdlib `struct` and `zlib` (no third-party image decoders or shell commands), validates hex colors and slot names, and HTML-escapes `<picture>` attributes.
- **Filesystem tree & preflight (`tree_gen.py`, `check_env.py`):** Read-only inspection (except optional explicit `--readme --slot` replacement in `tree_gen.py`), excluding `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, and `dist`. Never installs packages and never makes network requests.
- **Optional external renderers:** Third-party tools listed in the optional 25-engine reference archive run only if installed and explicitly invoked by the user in their own environment.

## Supported Versions

Only the latest published minor/patch release (currently `0.4.x`) receives security fixes.

## Reporting a Vulnerability

Please report security issues privately via GitHub Security Advisories on [`Technoetic/md-viz`](https://github.com/Technoetic/md-viz/security/advisories/new) instead of opening a public issue. Include:

1. Affected version or commit SHA
2. Minimal reproduction steps or input
3. Expected vs. actual behavior and impact

Reports are acknowledged as quickly as possible and fixed via pull request with regression tests.
