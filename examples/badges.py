"""Regenerate every two-tone SVG badge in docs/art/elements/ with the packaged stdlib badge tool."""
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/md-viz"
RENDERER = PLUGIN / "skills/md-viz/scripts/badge.py"
ART = ROOT / "docs/art/elements"
SHOW = ROOT / "examples/data/show.json"


def badge_specs():
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    license_id = manifest["license"]
    tempo = json.loads(SHOW.read_text(encoding="utf-8"))["cues"]["tempo"]
    return [
        # Row 1: Release, License, CI, Full Arsenal
        ("release", "RELEASE", f"V{version}", "#2864BA"),
        ("license", "LICENSE", license_id, "#00D68F"),
        ("ci", "CI", "UBUNTU + WIN", "#0EA5E9"),
        ("renderers", "GALLERY", "25 TOOLS", "#C8EF51"),
        ("markdown", "MARKDOWN", "6+4 LIVE", "#FF2E93"),
        ("hosts", "INSTALL", "3 HOSTS", "#00F5D4"),
        # Row 2: Host CLIs + Preflight
        ("antigravity", "CLI", "ANTIGRAVITY", "#7B61FF"),
        ("claude-code", "CLI", "CLAUDE CODE", "#FF7849"),
        ("codex", "CLI", "CODEX", "#14B8A6"),
        ("check-env", "PREFLIGHT", "CHECK_ENV.PY", "#F59E0B"),
        # Row 3: 3 Visual Wings + Alerts
        ("structure", "STRUCTURE", "9 TOOLS", "#38BDF8"),
        ("data", "DATA", "12 TOOLS", "#FFBB54"),
        ("notation", "CODE + MATH", "4 TOOLS", "#C084FC"),
        ("alerts", "ALERTS", "5 / 5 TYPES", "#FF3864"),
        # Row 4: Featured Live Showcase Jumps + Tempo
        ("mermaid", "FLOW", "MERMAID LIVE", "#00E5A0"),
        ("abcjs", "MUSIC", "ABCJS", "#EC4899"),
        ("d3", "LIGHT CUES", "D3 RADIAL", "#FF7043"),
        ("geojson", "MAP", "GEOJSON LIVE", "#A3E635"),
        ("katex", "MATH", "KATEX + LATEX", "#60A5FA"),
        ("tempo", "TEMPO", f"{tempo} BPM", "#C8FF00"),
    ]


def main():
    ART.mkdir(parents=True, exist_ok=True)
    for name, label, value, color in badge_specs():
        subprocess.run(
            [sys.executable, str(RENDERER), label, value, str(ART / f"{name}.svg"), "--color", color],
            check=True,
        )


if __name__ == "__main__":
    main()
