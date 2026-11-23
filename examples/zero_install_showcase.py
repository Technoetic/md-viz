"""Regenerate every zero-install GitHub README SVG (10 types) and stdlib GIF89a+PNG pair from examples/data/show.json."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins/md-viz/skills/md-viz/scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import gif_anim  # noqa: E402
import svg_chart  # noqa: E402

SHOW = ROOT / "examples/data/show.json"
MANIFEST = ROOT / "plugins/md-viz/plugin.json"
OUT_DIR = ROOT / "docs/art/zero-install"


def active_indices(bits, limit=None):
    seq = bits[:limit] if limit is not None else bits
    return [idx for idx, flag in enumerate(seq) if flag]


def build_specs():
    data = json.loads(SHOW.read_text(encoding="utf-8"))
    version = json.loads(MANIFEST.read_text(encoding="utf-8"))["version"]
    adm = data["admissions"]
    power = data["power"]
    merch = data["merch"]
    tickets = data["tickets"]
    final_seats = tickets["start"] + tickets["released"] - tickets["sightline"] - tickets["reserved"]
    aud = data["audience"]
    beams = data["beams"]
    cues = data["cues"]
    walks = data["walks"]

    return {
        "hero": {
            "title": f"MD-VIZ v{version}",
            "kicker": "ZERO-INSTALL GITHUB README.MD VISUAL ENGINE",
            "tagline": "GitHub-native Mermaid, MathJax & GeoJSON + Python stdlib SVG, badges, GIF89a & trees.",
            "accent": "#00F5D4",
            "accent2": "#FF2E93",
            "accent3": "#C8FF00",
            "pills": ["0 EXTERNAL DEPS", "10 PURE-SVG CHARTS", "STDLIB GIF89A", "GITHUB NATIVE 6+4"],
        },
        "kpi": {
            "title": "Zero-Install README Engine Telemetry",
            "subtitle": "NEON ENCORE / STDLIB",
            "accent": "#00F5D4",
            "items": [
                {"label": "EXTERNAL INSTALLS", "value": "0", "delta": "STDLIB", "note": "No npm, pip, or browser"},
                {"label": "PURE-SVG TYPES", "value": "10", "delta": "IMG SAFE", "note": "Zero script / foreignObject"},
                {"label": "SHOW TEMPO", "value": f"{cues['tempo']}", "delta": "BPM", "note": "Illustrative show.json"},
                {"label": "NET SEATS SOLD", "value": f"{final_seats:,}", "delta": "-100", "note": f"From {tickets['start']:,} base seats"},
            ],
        },
        "bar": {
            "title": "Merchandise Ranking (Illustrative Example)",
            "subtitle": "BAR · ZERO-INSTALL SVG",
            "accent": "#C8FF00",
            "unit": " pcs",
            "items": [
                {"label": item, "value": sold}
                for item, sold in merch.items()
            ],
        },
        "line": {
            "title": "Gate Admissions per 10 min (Illustrative Example)",
            "subtitle": "AREA / LINE · STDLIB SVG",
            "accent": "#00F5D4",
            "area": True,
            "x": [f"18:{m:02d}" for m in adm["minutes"]],
            "series": [
                {"name": "North Gate", "values": adm["North"], "color": "#00F5D4"},
                {"name": "East Gate", "values": adm["East"], "color": "#FF2E93"},
                {"name": "West Gate", "values": adm["West"], "color": "#C8FF00"},
            ],
        },
        "donut": {
            "title": "Stage Power Share (Illustrative Example)",
            "subtitle": "DONUT · STDLIB SVG",
            "accent": "#FFBB54",
            "unit": " kWh",
            "center_label": "TOTAL LOAD",
            "items": [
                {"label": system, "value": kwh}
                for system, kwh in power.items()
            ],
        },
        "heatmap": {
            "title": "Crowd Energy by Track & Zone (Illustrative Example)",
            "subtitle": "HEATMAP · STDLIB SVG",
            "accent": "#FF2E93",
            "rows": aud["zones"],
            "columns": aud["tracks"],
            "vmin": 0,
            "vmax": 100,
            "matrix": [
                [aud["index"][t_idx][z_idx] for t_idx in range(len(aud["tracks"]))]
                for z_idx in range(len(aud["zones"]))
            ],
        },
        "waterfall": {
            "title": "Seat Inventory Waterfall (Illustrative Example)",
            "subtitle": "WATERFALL · STDLIB SVG",
            "accent": "#38BDF8",
            "items": [
                {"label": "Start", "value": tickets["start"], "type": "total"},
                {"label": "Released", "value": tickets["released"]},
                {"label": "Sightline", "value": -tickets["sightline"]},
                {"label": "Reserved", "value": -tickets["reserved"]},
                {"label": "Final", "value": final_seats, "type": "total"},
            ],
        },
        "radar": {
            "title": "Beam Intensity Profile by Angle (Illustrative Example)",
            "subtitle": "RADAR · STDLIB SVG",
            "accent": "#C084FC",
            "max": 100,
            "axes": [f"{deg:+d}°" for deg in beams["degrees"][::2]],
            "series": [
                {"name": "Cyan Fixture", "values": beams["Cyan"][::2], "color": "#00F5D4"},
                {"name": "Amber Fixture", "values": beams["Amber"][::2], "color": "#C8FF00"},
            ],
        },
        "sankey": {
            "title": "Entrance to Seating Flow (Illustrative Example)",
            "subtitle": "SANKEY · STDLIB SVG",
            "accent": "#FFBB54",
            "unit": "",
            "links": [
                {"source": src, "target": tgt, "value": people}
                for src, tgt, people in walks
            ],
        },
        "timeline": {
            "title": "32-Beat Lighting Cue Matrix (Illustrative Example)",
            "subtitle": "TIMELINE · STDLIB SVG",
            "accent": "#C8FF00",
            "steps": len(cues["Wash"]),
            "tracks": [
                {"label": "Wash", "color": "#00F5D4", "active": active_indices(cues["Wash"])},
                {"label": "Beam", "color": "#FF2E93", "active": active_indices(cues["Beam"])},
                {"label": "Flash", "color": "#C8FF00", "active": active_indices(cues["Flash"])},
            ],
        },
    }


def build_gif_spec():
    data = json.loads(SHOW.read_text(encoding="utf-8"))
    cues = data["cues"]
    return {
        "title": "ZERO-INSTALL STDLIB 16-BEAT CUE LOOP",
        "width": 760,
        "height": 196,
        "steps": 16,
        "duration_ms": 220,
        "tracks": [
            {"label": "Wash", "color": "#00F5D4", "active": active_indices(cues["Wash"], 16)},
            {"label": "Beam", "color": "#FF2E93", "active": active_indices(cues["Beam"], 16)},
            {"label": "Flash", "color": "#C8FF00", "active": active_indices(cues["Flash"], 16)},
        ],
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    specs = build_specs()
    results = []
    for chart_type, spec in specs.items():
        results.append(svg_chart.generate_chart(chart_type, spec, OUT_DIR / f"{chart_type}.svg"))
    gif_meta = gif_anim.generate_gif_pair(build_gif_spec(), OUT_DIR / "cue-loop.gif")
    print(json.dumps({"svg_count": len(results), "gif": gif_meta}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
