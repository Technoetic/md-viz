"""Read-only preflight check for all 25 md-viz visualization engines using only the Python stdlib."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ENGINES = [
    # Structure, Signals & Music (9)
    ("Mermaid", "structure", "cli_or_native", ("mmdc",), (), ("mermaid",), "GitHub/Obsidian native mermaid fence or mmdc CLI"),
    ("PlantUML", "structure", "cli", ("plantuml", "java"), (), (), "plantuml CLI or java -jar plantuml.jar"),
    ("Graphviz", "structure", "cli", ("dot",), (), (), "Graphviz dot -Tsvg / -Tpng"),
    ("D2", "structure", "cli", ("d2",), (), (), "Terrastruct d2 CLI"),
    ("Structurizr", "structure", "cli", ("structurizr-cli", "structurizr"), (), (), "Structurizr CLI export -format dot + Graphviz"),
    ("markmap", "structure", "node", ("markmap", "node"), (), ("markmap-lib", "markmap-cli"), "markmap-cli or markmap-lib + browser capture"),
    ("Excalidraw", "structure", "node", ("node",), (), ("@excalidraw/excalidraw",), "Excalidraw SVG/PNG export via Node/browser"),
    ("WaveDrom", "structure", "node", ("wavedrom-cli", "node"), (), ("wavedrom",), "wavedrom-cli or wavedrom JS renderer"),
    ("abcjs", "structure", "node", ("node",), (), ("abcjs",), "abcjs renderAbc() SVG/PNG capture"),
    # Data, Charts, Networks & Maps (12)
    ("Vega-Lite", "data", "py_or_node", ("vl2svg", "vl2png", "node"), ("vl_convert", "altair"), ("vega-lite",), "vl-convert-python, vl2svg, or Vega-Lite JS"),
    ("Matplotlib", "data", "python", (), ("matplotlib",), (), "python matplotlib static PNG/SVG"),
    ("seaborn", "data", "python", (), ("seaborn", "matplotlib"), (), "python seaborn statistical plots"),
    ("Altair", "data", "python", (), ("altair", "vl_convert"), (), "python altair + vl-convert-python"),
    ("ggplot2", "data", "r", ("Rscript",), (), (), "Rscript ggplot2 + svglite"),
    ("Chart.js", "data", "node", ("node",), (), ("chart.js",), "Chart.js canvas/browser capture"),
    ("Observable Plot", "data", "node", ("node",), (), ("@observablehq/plot",), "Observable Plot SVG/PNG capture"),
    ("Plotly", "data", "py_or_node", ("node",), ("plotly",), ("plotly.js-dist-min", "plotly.js"), "Plotly JS or python plotly/kaleido"),
    ("Apache ECharts", "data", "node", ("node",), (), ("echarts",), "Apache ECharts SVG/canvas capture"),
    ("D3", "data", "node", ("node",), (), ("d3",), "D3 custom SVG/PNG capture"),
    ("Cytoscape.js", "data", "node", ("node",), (), ("cytoscape",), "Cytoscape.js graph capture"),
    ("Leaflet", "data", "node", ("node",), (), ("leaflet",), "Leaflet coordinate map capture or GitHub GeoJSON"),
    # Code Highlighting & Math (4)
    ("Shiki", "notation", "node", ("node",), (), ("shiki",), "Shiki static HTML/SVG code highlighting"),
    ("highlight.js", "notation", "node", ("node",), (), ("highlight.js",), "highlight.js browser/Node highlighting"),
    ("MathJax", "notation", "node", ("node",), (), ("@mathjax/src", "mathjax"), "MathJax TeX-to-SVG/HTML rendering"),
    ("KaTeX", "notation", "node", ("katex", "node"), (), ("katex",), "KaTeX fast TeX-to-HTML/MathML rendering"),
]

RUNTIMES = ("python", "python3", "node", "npm", "npx", "Rscript", "dot", "d2", "plantuml", "mmdc", "aside", "chrome", "chromium", "msedge")


def has_python_module(name):
    return importlib.util.find_spec(name) is not None


def has_node_pkg(pkg, search_roots):
    parts = pkg.split("/")
    for root in search_roots:
        if (root / "node_modules").joinpath(*parts).exists():
            return True
    return False


def discover_node_roots(cwd):
    roots = [cwd]
    for sub in ("examples/data", "examples/notation", "examples/structure"):
        candidate = cwd / sub
        if candidate.is_dir():
            roots.append(candidate)
    return roots


def inspect_environment(cwd=None):
    base = Path(cwd).resolve() if cwd else Path.cwd().resolve()
    node_roots = discover_node_roots(base)
    runtimes = {cmd: shutil.which(cmd) is not None for cmd in RUNTIMES}
    runtimes["python_active"] = True
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    results = []
    ready_count = 0
    partial_count = 0
    for name, category, mode, clis, py_mods, npm_pkgs, note in ENGINES:
        found_clis = [c for c in clis if shutil.which(c) is not None]
        found_py = [m for m in py_mods if has_python_module(m)]
        found_npm = [p for p in npm_pkgs if has_node_pkg(p, node_roots)]

        if mode == "cli_or_native":
            status = "ready"
        elif mode == "cli":
            status = "ready" if found_clis else "missing"
        elif mode == "python":
            if py_mods and len(found_py) == len(py_mods):
                status = "ready"
            elif found_py:
                status = "partial"
            else:
                status = "missing"
        elif mode == "r":
            status = "partial" if found_clis else "missing"
        elif mode == "py_or_node":
            if found_py or found_npm or any(c != "node" for c in found_clis):
                status = "ready"
            elif "node" in found_clis:
                status = "partial"
            else:
                status = "missing"
        elif mode == "node":
            if found_npm or any(c != "node" for c in found_clis):
                status = "ready"
            elif "node" in found_clis:
                status = "partial"
            else:
                status = "missing"
        else:
            status = "missing"

        if status == "ready":
            ready_count += 1
        elif status == "partial":
            partial_count += 1

        results.append({
            "name": name,
            "category": category,
            "status": status,
            "found_clis": found_clis,
            "found_python": found_py,
            "found_npm": found_npm,
            "note": note,
        })

    return {
        "cwd": str(base),
        "python_version": python_version,
        "runtimes": runtimes,
        "summary": {
            "total": len(ENGINES),
            "ready": ready_count,
            "partial": partial_count,
            "missing": len(ENGINES) - ready_count - partial_count,
        },
        "engines": results,
    }


def render_markdown(report):
    s = report["summary"]
    lines = [
        f"## md-viz Local Renderer Preflight (`{s['ready']}` ready / `{s['partial']}` runtime-only / `{s['missing']}` missing of `{s['total']}`)",
        "",
        f"- **Python:** `{report['python_version']}`",
        "- **Runtimes on PATH:** " + ", ".join(
            f"`{k}`" for k, v in report["runtimes"].items() if v and k != "python_active"
        ),
        "",
        "| Status | Engine | Category | Detected | Notes |",
        "|---|---|---|---|---|",
    ]
    badge = {"ready": "✅ ready", "partial": "⚠️ runtime-only", "missing": "❌ missing"}
    for eng in report["engines"]:
        items = eng["found_clis"] + eng["found_python"] + eng["found_npm"]
        if not items and eng["status"] == "ready":
            items = ["GitHub/Obsidian native"]
        detected = ", ".join(items) or "—"
        lines.append(f"| {badge[eng['status']]} | **{eng['name']}** | `{eng['category']}` | `{detected}` | {eng['note']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=None, help="Directory to inspect for local node_modules")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output")
    args = parser.parse_args()
    report = inspect_environment(args.cwd)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")


if __name__ == "__main__":
    main()
