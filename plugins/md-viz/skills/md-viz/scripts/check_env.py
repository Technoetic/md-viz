"""Read-only preflight for the zero-install GitHub README.md visual stack plus optional external renderers."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

SCRIPT_DIR = Path(__file__).resolve().parent

GITHUB_NATIVE_CAPABILITIES = (
    ("Mermaid", "native-fence", "Live styled flowcharts, sequence, state, Gantt, mindmap, quadrant & XY diagrams"),
    ("MathJax", "native-math", "Live inline $...$, display $$...$$, and ```math``` LaTeX equations"),
    ("GeoJSON / TopoJSON", "native-map", "Live zoomable, clickable geographic vector maps (```geojson``` / ```topojson```)"),
    ("GitHub Alerts 5/5", "native-callout", "NOTE, TIP, IMPORTANT, WARNING, and CAUTION callout blocks"),
    ("Syntax Highlighting", "native-code", "GitHub Linguist fenced code blocks with language identifiers"),
    ("Layout & UX Primitives", "native-layout", "<picture> reduced-motion/theme switching, <details>, <kbd>, tables & semantic emoji"),
)

ZERO_INSTALL_GENERATORS = (
    ("badge.py", "svg-badge", "28px two-tone neon SVG badges (WCAG ink contrast, East-Asian width, strict hex)"),
    ("svg_chart.py", "svg-suite-10", "10 GitHub <img>-safe pure-SVG visuals (hero, kpi, bar, line, donut, heatmap, waterfall, radar, sankey, timeline)"),
    ("gif_anim.py", "gif-png-pair", "Pure-stdlib animated GIF89a + identical-dimension reduced-motion PNG (<picture>)"),
    ("tree_gen.py", "aligned-tree", "Real-repo column-aligned annotated directory tree (East-Asian width exact)"),
)

ENGINES = [
    # Structure, Signals & Music (9)
    ("Mermaid", "structure", "cli_or_native", ("mmdc",), (), ("mermaid",), True, "GitHub native mermaid fence or mmdc CLI"),
    ("PlantUML", "structure", "cli", ("plantuml", "java"), (), (), False, "Optional external pre-render: plantuml CLI"),
    ("Graphviz", "structure", "cli", ("dot",), (), (), False, "Optional external pre-render: Graphviz dot"),
    ("D2", "structure", "cli", ("d2",), (), (), False, "Optional external pre-render: Terrastruct d2"),
    ("Structurizr", "structure", "cli", ("structurizr-cli", "structurizr"), (), (), False, "Optional external pre-render: Structurizr CLI"),
    ("markmap", "structure", "node", ("markmap", "node"), (), ("markmap-lib", "markmap-cli"), False, "Optional external pre-render (or native Mermaid mindmap)"),
    ("Excalidraw", "structure", "node", ("node",), (), ("@excalidraw/excalidraw",), False, "Optional external pre-render: Excalidraw"),
    ("WaveDrom", "structure", "node", ("wavedrom-cli", "node"), (), ("wavedrom",), False, "Optional external pre-render (or zero-install svg_chart.py timeline)"),
    ("abcjs", "structure", "node", ("node",), (), ("abcjs",), False, "Optional external pre-render: abcjs sheet music"),
    # Data, Charts, Networks & Maps (12)
    ("Vega-Lite", "data", "py_or_node", ("vl2svg", "vl2png", "node"), ("vl_convert", "altair"), ("vega-lite",), False, "Optional external pre-render (or zero-install svg_chart.py line/bar)"),
    ("Matplotlib", "data", "python", (), ("matplotlib",), (), False, "Optional external pre-render (or zero-install svg_chart.py radar/bar)"),
    ("seaborn", "data", "python", (), ("seaborn", "matplotlib"), (), False, "Optional external pre-render (or zero-install svg_chart.py heatmap)"),
    ("Altair", "data", "python", (), ("altair", "vl_convert"), (), False, "Optional external pre-render (or zero-install svg_chart.py bar/line)"),
    ("ggplot2", "data", "r", ("Rscript",), (), (), False, "Optional external pre-render: Rscript ggplot2"),
    ("Chart.js", "data", "node", ("node",), (), ("chart.js",), False, "Optional external pre-render (or zero-install svg_chart.py donut/bar)"),
    ("Observable Plot", "data", "node", ("node",), (), ("@observablehq/plot",), False, "Optional external pre-render (or zero-install svg_chart.py bar)"),
    ("Plotly", "data", "py_or_node", ("node",), ("plotly",), ("plotly.js-dist-min", "plotly.js"), False, "Optional external pre-render (or zero-install svg_chart.py waterfall)"),
    ("Apache ECharts", "data", "node", ("node",), (), ("echarts",), False, "Optional external pre-render (or zero-install svg_chart.py sankey)"),
    ("D3", "data", "node", ("node",), (), ("d3",), False, "Optional external pre-render (or zero-install svg_chart.py donut/timeline)"),
    ("Cytoscape.js", "data", "node", ("node",), (), ("cytoscape",), False, "Optional external pre-render (or native Mermaid flowchart)"),
    ("Leaflet", "data", "node", ("node",), (), ("leaflet",), False, "Optional external pre-render (or GitHub native GeoJSON map)"),
    # Code Highlighting & Math (4)
    ("Shiki", "notation", "node", ("node",), (), ("shiki",), False, "Optional external pre-render (or GitHub native syntax highlighting)"),
    ("highlight.js", "notation", "node", ("node",), (), ("highlight.js",), False, "Optional external pre-render (or GitHub native syntax highlighting)"),
    ("MathJax", "notation", "cli_or_native", ("node",), (), ("@mathjax/src", "mathjax"), True, "GitHub native $$...$$ / ```math``` renderer"),
    ("KaTeX", "notation", "node", ("katex", "node"), (), ("katex",), False, "Optional external pre-render (GitHub README uses native MathJax)"),
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

    bundled_scripts = [
        {
            "script": name,
            "kind": kind,
            "status": "ready" if (SCRIPT_DIR / name).is_file() else "missing",
            "dependencies": "Python 3 stdlib only (zero install)",
            "description": desc,
        }
        for name, kind, desc in ZERO_INSTALL_GENERATORS
    ]
    github_native = [
        {"name": name, "kind": kind, "status": "ready", "description": desc}
        for name, kind, desc in GITHUB_NATIVE_CAPABILITIES
    ]

    results = []
    ready_count = 0
    partial_count = 0
    github_native_libs = 0
    for name, category, mode, clis, py_mods, npm_pkgs, gh_native, note in ENGINES:
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
        if gh_native:
            github_native_libs += 1

        results.append({
            "name": name,
            "category": category,
            "status": status,
            "github_native": gh_native,
            "found_clis": found_clis,
            "found_python": found_py,
            "found_npm": found_npm,
            "note": note,
        })

    zero_install_ready = all(s["status"] == "ready" for s in bundled_scripts)
    return {
        "cwd": str(base),
        "python_version": python_version,
        "zero_install_ready": zero_install_ready,
        "github_native_capabilities": github_native,
        "bundled_generators": bundled_scripts,
        "runtimes": runtimes,
        "summary": {
            "zero_install_generators_ready": sum(1 for s in bundled_scripts if s["status"] == "ready"),
            "zero_install_generators_total": len(bundled_scripts),
            "github_native_capabilities": len(github_native),
            "github_native_libraries": github_native_libs,
            "github_prerender_libraries": len(ENGINES) - github_native_libs,
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
        f"## md-viz Zero-Install GitHub README Preflight (`{s['zero_install_generators_ready']}/{s['zero_install_generators_total']}` stdlib generators ready · `{s['github_native_capabilities']}` GitHub-native layers)",
        "",
        f"- **Zero-Install Mode:** `{'✅ READY (0 external installs needed)' if report['zero_install_ready'] else '⚠️ incomplete'}`",
        f"- **Python:** `{report['python_version']}` (stdlib only)",
        f"- **GitHub README Native Libraries:** `{s['github_native_libraries']}/25` (`Mermaid`, `MathJax`) + `GeoJSON` maps + Alerts 5/5 + Syntax Highlighting",
        "",
        "### Bundled Zero-Install Generators (100% Python Stdlib)",
        "",
        "| Status | Script | Output | Description |",
        "|---|---|---|---|",
    ]
    for gen in report["bundled_generators"]:
        st = "✅ ready" if gen["status"] == "ready" else "❌ missing"
        lines.append(f"| {st} | `{gen['script']}` | `{gen['kind']}` | {gen['description']} |")

    lines.extend([
        "",
        f"### Optional External 25-Engine Reference Catalog (`{s['ready']}` ready / `{s['partial']}` runtime-only / `{s['missing']}` missing of `{s['total']}`)",
        "",
        "| Status | Engine | Category | Detected | Notes |",
        "|---|---|---|---|---|",
    ])
    badge = {"ready": "✅ ready", "partial": "⚠️ runtime-only", "missing": "❌ missing"}
    for eng in report["engines"]:
        items = list(eng["found_clis"]) + list(eng["found_python"]) + list(eng["found_npm"])
        if eng["github_native"] and not any(x != "node" for x in items):
            items = ["GitHub native"]
        detected = ", ".join(items) or "—"
        lines.append(f"| {badge[eng['status']]} | **{eng['name']}** | `{eng['category']}` | `{detected}` | {eng['note']} |")
    return "\n".join(lines) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=None, help="Directory to inspect for optional local node_modules")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output")
    args = parser.parse_args()
    report = inspect_environment(args.cwd)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")


if __name__ == "__main__":
    main()
