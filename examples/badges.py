"""Regenerate the four README badge rows with the packaged SVG tool."""
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/md-viz"
RENDERER = PLUGIN / "skills/md-viz/scripts/badge.py"
ART = ROOT / "docs/art/elements"


def main():
    version = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))["version"]
    badges = [
        ("release", "RELEASE", f"V{version}", "#2864BA"),
        ("renderers", "GALLERY", "25 TOOLS", "#C8EF51"),
        ("markdown", "MARKDOWN", "6 PATTERNS", "#D24CA4"),
        ("hosts", "INSTALL", "3 HOSTS", "#4BBDCA"),
        ("antigravity", "CLI", "ANTIGRAVITY", "#7953CA"),
        ("claude-code", "CLI", "CLAUDE CODE", "#E79066"),
        ("codex", "CLI", "CODEX", "#158172"),
        ("structure", "STRUCTURE", "9 TOOLS", "#71CAEA"),
        ("data", "DATA", "12 TOOLS", "#FFBB54"),
        ("notation", "CODE + MATH", "4 TOOLS", "#AE88ED"),
        ("abcjs", "MUSIC", "ABCJS", "#DA6DA8"),
        ("d3", "LIGHT CUES", "D3", "#FF965E"),
        ("geojson", "MAP", "GEOJSON", "#B3E071"),
        ("katex", "MATH", "KATEX", "#6F9FEB"),
    ]
    for name, label, value, color in badges:
        subprocess.run(
            [sys.executable, str(RENDERER), label, value, str(ART / f"{name}.svg"), "--color", color],
            check=True,
        )


if __name__ == "__main__":
    main()
