# Security Policy

## Scope

`md-viz` distributes Markdown visualization instructions, a zero-dependency Python standard-library SVG badge generator (`plugins/md-viz/skills/md-viz/scripts/badge.py`), and a read-only local renderer preflight script (`plugins/md-viz/skills/md-viz/scripts/check_env.py`).

### Security Boundaries

- **SVG generation (`badge.py`):** Validates single-line printable labels/values and strict 6-digit hex color values (`#RRGGBB`) in both CLI arguments and the Python `badge_svg()` API, and XML-escapes all user text. Never writes outside the caller-specified output path.
- **Environment check (`check_env.py`):** Strictly read-only inspection (`PATH` lookup, Python import availability, optional `node_modules` inspection). Never installs packages, never modifies files, and never makes network requests.
- **External renderers:** Diagram, chart, code, and math libraries listed in `SKILL.md` are third-party tools installed and executed in the user's own environment. Render untrusted Markdown inputs locally and review generated assets before publishing.

## Supported Versions

Only the latest published minor/patch release (currently `0.3.x`) receives security fixes.

## Reporting a Vulnerability

Please report security issues privately via GitHub Security Advisories on [`Technoetic/md-viz`](https://github.com/Technoetic/md-viz/security/advisories/new) instead of opening a public issue. Include:

1. Affected version or commit SHA
2. Minimal reproduction steps or input
3. Expected vs. actual behavior and impact

Reports are acknowledged as quickly as possible and fixed via pull request with regression tests.
