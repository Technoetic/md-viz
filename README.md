<div align="center">
  <strong>🌐 English</strong> · <a href="README.ko.md"><strong>🇰🇷 한국어 (Korean)</strong></a> · <a href="docs/github-elements.md"><strong>✨ GitHub Techniques (6+4)</strong></a> · <a href="plugins/md-viz/skills/md-viz/SKILL.md"><strong>📖 Skill Spec</strong></a>
</div>

<br>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/art/cover.png">
  <img src="docs/art/cover.gif" width="1280" alt="MD-VIZ NEON ENCORE poster. Vivid neon vinyl grooves pulse across a dark obsidian stage representing 25 visualization libraries and 6+4 GitHub Markdown visual techniques for Antigravity, Claude Code, and Codex.">
</picture>

<h1 align="center">⚡ md-viz · Full-Arsenal High-Impact Markdown Visualizer</h1>

<div align="center">
  <a href="plugins/md-viz/plugin.json"><img src="docs/art/elements/release.svg" alt="Release v0.3.0 · Open plugin manifest"></a>
  <a href="LICENSE"><img src="docs/art/elements/license.svg" alt="MIT License · Read license"></a>
  <a href=".github/workflows/ci.yml"><img src="docs/art/elements/ci.svg" alt="CI Ubuntu + Windows · View workflow"></a>
  <a href="#-full-25-engine-inline-visual-wall"><img src="docs/art/elements/renderers.svg" alt="Gallery 25 Tools · Jump to full wall"></a>
  <a href="docs/github-elements.md"><img src="docs/art/elements/markdown.svg" alt="GitHub Markdown 6+4 Live Techniques"></a>
  <a href="#-install-in-one-command"><img src="docs/art/elements/hosts.svg" alt="Install on 3 AI Agent Hosts"></a>
</div>
<div align="center">
  <a href="#antigravity-cli-agy"><img src="docs/art/elements/antigravity.svg" alt="Install for Antigravity CLI"></a>
  <a href="#claude-code"><img src="docs/art/elements/claude-code.svg" alt="Install for Claude Code"></a>
  <a href="#codex"><img src="docs/art/elements/codex.svg" alt="Install for Codex"></a>
  <a href="plugins/md-viz/skills/md-viz/scripts/check_env.py"><img src="docs/art/elements/check-env.svg" alt="Zero-dependency local renderer preflight check_env.py"></a>
</div>
<div align="center">
  <a href="docs/structure.md"><img src="docs/art/elements/structure.svg" alt="Structure, Signals & Sheet Music · 9 Tools"></a>
  <a href="docs/data.md"><img src="docs/art/elements/data.svg" alt="Data, Stats, Networks & Maps · 12 Tools"></a>
  <a href="docs/notation.md"><img src="docs/art/elements/notation.svg" alt="Code Syntax & Math Typography · 4 Tools"></a>
  <a href="docs/github-elements.md#알림-블록--공연-노트에서-무엇을-강조할까"><img src="docs/art/elements/alerts.svg" alt="All 5 GitHub Alert Types Live"></a>
</div>
<div align="center">
  <a href="#-live-visual-overdrive-pipeline"><img src="docs/art/elements/mermaid.svg" alt="Live Styled Mermaid Flow"></a>
  <a href="docs/structure.md#첫-멜로디--abcjs"><img src="docs/art/elements/abcjs.svg" alt="abcjs Sheet Music Score"></a>
  <a href="docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까"><img src="docs/art/elements/d3.svg" alt="D3 Radial Beat Sequencer"></a>
  <a href="#-live-interactive-geojson-map--github-techniques"><img src="docs/art/elements/geojson.svg" alt="Live Interactive GeoJSON Map"></a>
  <a href="docs/notation.md#다음-큐까지-몇-초를-셀까--katex"><img src="docs/art/elements/katex.svg" alt="KaTeX + Live GitHub LaTeX Math"></a>
</div>

<p align="center">
  <kbd>/md-viz</kbd> + <kbd>25 Rendering Libraries</kbd> + <kbd>6 Core GitHub Techniques</kbd> + <kbd>4 Native Boosters</kbd> → <strong>Maximum Visual Impact Without Inventing a Single Fact</strong>
</p>

**Turn plain Markdown into an electrifying, multi-lens visual showcase.** Give `md-viz` a rehearsal note — *"120 BPM, 4/4 time, first bar C–D–E–G"* — and it fires every fitting renderer in parallel: sheet music for the band (**abcjs**), beat-accurate timing switches for lighting (**WaveDrom**), radial cue wheels (**D3**), Sankey crowd flow (**ECharts**), interactive maps (**GeoJSON** + **Leaflet**), syntax-lit code (**Shiki** + **highlight.js**), crisp equations (**KaTeX** + **MathJax** + native `$$...$$`), animated beat-sync GIFs, neon SVG badge walls, aligned directory trees, and all 5 GitHub alerts — **all directly inside your document**.

---

## ⚡ Live Visual Overdrive Pipeline

Here is how `md-viz` inspects your machine with `scripts/check_env.py` and fans out a single Markdown draft across **25 visualization libraries** and **6+4 GitHub-native techniques** (rendered live by GitHub's native Mermaid engine with high-contrast neon `classDef` styling):

```mermaid
flowchart TB
    DOC["📄 Source Markdown · README · Specs"]:::src --> SCAN["🔍 check_env.py · Local 25-Engine Preflight"]:::env
    SCAN --> W1["🎭 Structure & Signals · 9\nMermaid · PlantUML · Graphviz · D2 · Structurizr · markmap · Excalidraw · WaveDrom · abcjs"]:::cyan
    SCAN --> W2["📊 Data · Graphs · Maps · 12\nVega-Lite · ggplot2 · ECharts · Leaflet · Altair · Matplotlib · D3 · Cytoscape · seaborn · Chart.js · Plot · Plotly"]:::amber
    SCAN --> W3["🧮 Code & Math · 4\nShiki · highlight.js · MathJax · KaTeX"]:::violet
    SCAN --> W4["✨ GitHub Native · 6+4\nGeoJSON · Neon SVG Badges · Emojis · Picture GIF · Tree · 5/5 Alerts · Live Mermaid & LaTeX"]:::magenta
    W1 & W2 & W3 & W4 --> FINAL["🚀 Full-Arsenal Visual Showcase · 100% Factual Fidelity · Maximum Contrast"]:::lime

    classDef src fill:#131621,stroke:#94a3b8,color:#f8fafc,stroke-width:2px
    classDef env fill:#0f172a,stroke:#38bdf8,color:#e0f2fe,stroke-width:2px
    classDef cyan fill:#083344,stroke:#00f5d4,color:#ccfbf1,stroke-width:2px
    classDef amber fill:#451a03,stroke:#ffbb54,color:#fef3c7,stroke-width:2px
    classDef violet fill:#2e1065,stroke:#c084fc,color:#f3e8ff,stroke-width:2px
    classDef magenta fill:#500724,stroke:#ff2e93,color:#fce7f3,stroke-width:2px
    classDef lime fill:#1a2e05,stroke:#c8ff00,color:#ecfccb,stroke-width:3px
```

---

## 🎵 Eight Notes → Multi-Engine Impact

> [!NOTE]
> **NEON ENCORE** is a fictional concert crafted specifically to stress-test all **25 rendering libraries** and **6+4 GitHub Markdown techniques** against one shared dataset ([`examples/data/show.json`](examples/data/show.json)). Every chart, map, score, waveform, and formula below is generated from real code in [`examples/`](examples).

[![Show Tempo 120 BPM · Open source dataset](docs/art/elements/tempo.svg)](examples/data/show.json)

Drop eight quarter notes (`C D E G | G E D C |]`) into ABC notation and pair the live GitHub LaTeX equation with four simultaneous visual lenses (**abcjs**, **WaveDrom**, **KaTeX**, and **D3**):

$$\Delta t_{\text{beat}} = \frac{60}{120\text{ BPM}} = 0.5\text{ s}, \qquad T_{8\text{ bars}} = 8 \times 4 \times 0.5\text{ s} = 16\text{ s}$$

| 🎼 Sheet Music (`abcjs`) | ⚡ Beat Switch Timing (`WaveDrom`) |
|:---:|:---:|
| [![abcjs sheet music rendering C-D-E-G then G-E-D-C at 120 BPM](docs/art/structure/encore.png)](docs/structure.md#첫-멜로디--abcjs) | [![WaveDrom 8-beat signal timing for click, track, and lights](docs/art/structure/count-in.png)](docs/structure.md#박자에-맞춘-스위치--wavedrom) |
| 🧮 **Queue Duration Formula (`KaTeX`)** | 🎡 **32-Beat Radial Sequencer (`D3`)** |
| [![KaTeX equation card: 8 bars x 4 beats x 0.5 s = 16 s](docs/art/notation/katex.png)](docs/notation.md#다음-큐까지-몇-초를-셀까--katex) | [![D3 circular 32-beat lighting sequencer for Wash, Beam, and Flash](docs/art/data/d3.png)](docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까) |

### 🎬 Beat-Synced Animated Cue Player (`<picture>` Motion-Safe Loop)

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/art/cue-player.png">
  <img src="docs/art/cue-player.gif" width="1080" alt="Three colored rows show Wash, Beam, and Flash lighting cues across 32 beats. The playhead advances every 0.5 seconds for a 16-second loop.">
</picture>

Bright cells fire on the active beat. Read vertically to see simultaneous fixtures; readers with `prefers-reduced-motion: reduce` automatically receive the crisp still frame [`cue-player.png`](docs/art/cue-player.png).

---

## 🔥 Full 25-Engine Inline Visual Wall

![25-engine master contact sheet displaying all structure, data, code, and math renderers in five vivid rows](docs/art/contact-sheet.png)

Every single one of the **25 libraries** is rendered live right below — click any card to inspect its full walkthrough and raw source code.

<details open>
<summary><strong>🎭 Wing 1 · Structure, Architecture, Signals & Sheet Music — All 9/9 Libraries</strong></summary>

| 🔀 Mermaid · Flow Gate | 💬 PlantUML · Sequence | 🕸️ Graphviz · Signal DAG |
|:---:|:---:|:---:|
| [![Mermaid flow gate diagram](docs/art/structure/cue-gate.png)](docs/structure.md#시작-판단--mermaid)<br>[Walkthrough](docs/structure.md#시작-판단--mermaid) · [`.mmd`](examples/structure/cue-gate.mmd) | [![PlantUML standby call-and-response sequence](docs/art/structure/standby.png)](docs/structure.md#호출과-응답--plantuml)<br>[Walkthrough](docs/structure.md#호출과-응답--plantuml) · [`.puml`](examples/structure/standby.puml) | [![Graphviz audio signal routing graph](docs/art/structure/signal-path.png)](docs/structure.md#소리의-갈림길--graphviz)<br>[Walkthrough](docs/structure.md#소리의-갈림길--graphviz) · [`.dot`](examples/structure/signal-path.dot) |
| 🧩 **D2 · Rack Topology** | 🏛️ **Structurizr · C4 Context** | 🌿 **markmap · Mind Map** |
| [![D2 stage rack and FOH console topology](docs/art/structure/patch-bays.png)](docs/structure.md#장비의-위치--d2)<br>[Walkthrough](docs/structure.md#장비의-위치--d2) · [`.d2`](examples/structure/patch-bays.d2) | [![Structurizr C4 system context view](docs/art/structure/cue-desk.png)](docs/structure.md#시스템의-경계--structurizr)<br>[Walkthrough](docs/structure.md#시스템의-경계--structurizr) · [`.dsl`](examples/structure/cue-desk.dsl) | [![markmap rehearsal notes mind map](docs/art/structure/set-notes.png)](docs/structure.md#노트의-가지--markmap)<br>[Walkthrough](docs/structure.md#노트의-가지--markmap) · [`.md`](examples/structure/set-notes.md) |
| ✏️ **Excalidraw · Stage Plot** | 📡 **WaveDrom · Timing** | 🎼 **abcjs · Sheet Music** |
| [![Excalidraw spatial stage plot](docs/art/structure/stage-plot.png)](docs/structure.md#관객이-보는-무대--excalidraw)<br>[Walkthrough](docs/structure.md#관객이-보는-무대--excalidraw) · [`.js`](examples/structure/stage-plot.js) | [![WaveDrom count-in signal waveform](docs/art/structure/count-in.png)](docs/structure.md#박자에-맞춘-스위치--wavedrom)<br>[Walkthrough](docs/structure.md#박자에-맞춘-스위치--wavedrom) · [`.json`](examples/structure/count-in.json) | [![abcjs encore motif music notation](docs/art/structure/encore.png)](docs/structure.md#첫-멜로디--abcjs)<br>[Walkthrough](docs/structure.md#첫-멜로디--abcjs) · [`.abc`](examples/structure/encore.abc) |

</details>

<details open>
<summary><strong>📊 Wing 2 · Data, Statistics, Networks & Geospatial Maps — All 12/12 Libraries</strong></summary>

| 📈 Vega-Lite · Stacked Area | 📦 ggplot2 · Wait Boxplot | 🌊 Apache ECharts · Sankey |
|:---:|:---:|:---:|
| [![Vega-Lite stacked gate arrivals chart](docs/art/data/vega-lite.png)](docs/data.md#vega-lite--언제-입장객이-몰렸을까)<br>[Walkthrough](docs/data.md#vega-lite--언제-입장객이-몰렸을까) | [![ggplot2 horizontal wait-time boxplot with samples](docs/art/data/ggplot2.png)](docs/data.md#ggplot2--입구별로-관객은-얼마나-기다렸을까)<br>[Walkthrough](docs/data.md#ggplot2--입구별로-관객은-얼마나-기다렸을까) | [![Apache ECharts audience flow Sankey diagram](docs/art/data/echarts.png)](docs/data.md#apache-echarts--세-입구를-통과한-사람들은-어디로-갔을까)<br>[Walkthrough](docs/data.md#apache-echarts--세-입구를-통과한-사람들은-어디로-갔을까) |
| 🧭 **Leaflet · Route Map** | 🏋️ **Altair · Dumbbell Delta** | 🎯 **Matplotlib · Polar Beam** |
| [![Leaflet shuttle coordinate route map](docs/art/data/leaflet.png)](docs/data.md#leaflet--집결점에서-무대까지-어느-방향으로-움직일까)<br>[Walkthrough](docs/data.md#leaflet--집결점에서-무대까지-어느-방향으로-움직일까) | [![Altair planned vs actual soundcheck dumbbell chart](docs/art/data/altair.png)](docs/data.md#altair--사운드체크-계획은-어디서-어긋났을까)<br>[Walkthrough](docs/data.md#altair--사운드체크-계획은-어디서-어긋났을까) | [![Matplotlib polar lighting intensity pattern](docs/art/data/matplotlib.png)](docs/data.md#matplotlib--두-조명의-밝은-방향은-어디일까)<br>[Walkthrough](docs/data.md#matplotlib--두-조명의-밝은-방향은-어디일까) |
| 🎡 **D3 · Radial Sequencer** | 🧬 **Cytoscape.js · Audio Mesh** | 🔥 **seaborn · Crowd Heatmap** |
| [![D3 circular 32-beat lighting cue sequencer](docs/art/data/d3.png)](docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까)<br>[Walkthrough](docs/data.md#d3--한-박씩-돌려-보면-어떤-조명이-켜질까) | [![Cytoscape.js vocal audio splitter network](docs/art/data/cytoscape.png)](docs/data.md#cytoscapejs--보컬-소리가-녹음기까지-가는-길은)<br>[Walkthrough](docs/data.md#cytoscapejs--보컬-소리가-녹음기까지-가는-길은) | [![seaborn song-by-zone crowd energy heatmap](docs/art/data/seaborn.png)](docs/data.md#seaborn--어느-곡에서-객석-전체가-함께-반응했을까)<br>[Walkthrough](docs/data.md#seaborn--어느-곡에서-객석-전체가-함께-반응했을까) |
| 🍩 **Chart.js · Power Donut** | 🏆 **Observable Plot · Merch Rank** | 💧 **Plotly · Seat Waterfall** |
| [![Chart.js 100 kWh power share donut chart](docs/art/data/chartjs.png)](docs/data.md#chartjs--무엇이-전기를-가장-많이-썼을까)<br>[Walkthrough](docs/data.md#chartjs--무엇이-전기를-가장-많이-썼을까) | [![Observable Plot merchandise ranking chart](docs/art/data/observable.png)](docs/data.md#observable-plot--가장-잘-팔린-기념품은)<br>[Walkthrough](docs/data.md#observable-plot--가장-잘-팔린-기념품은) | [![Plotly seat inventory waterfall chart](docs/art/data/plotly.png)](docs/data.md#plotly--좌석-증감이-최종-판매-수를-어떻게-바꿨을까)<br>[Walkthrough](docs/data.md#plotly--좌석-증감이-최종-판매-수를-어떻게-바꿨을까) |

</details>

<details open>
<summary><strong>🧮 Wing 3 · Code Syntax Highlighting & Mathematical Typography — All 4/4 Libraries</strong></summary>

| 💎 Shiki · Static Highlight | 🔦 highlight.js · Dynamic Highlight |
|:---:|:---:|
| [![Shiki syntax-highlighted JS cue object](docs/art/notation/shiki.png)](docs/notation.md#첫-조명은-무슨-색일까--shiki)<br>[Walkthrough](docs/notation.md#첫-조명은-무슨-색일까--shiki) | [![highlight.js syntax-highlighted Python downbeat check](docs/art/notation/highlight.png)](docs/notation.md#어느-박에서-조명을-바꿀까--highlightjs)<br>[Walkthrough](docs/notation.md#어느-박에서-조명을-바꿀까--highlightjs) |
| 📐 **MathJax · TeX SVG Equation** | ⚡ **KaTeX · Fast HTML/MathML** |
| [![MathJax beat duration equation 60 / 120 = 0.5 s](docs/art/notation/mathjax.png)](docs/notation.md#한-박의-길이는--mathjax)<br>[Walkthrough](docs/notation.md#한-박의-길이는--mathjax) | [![KaTeX 8-bar cue duration formula = 16 s](docs/art/notation/katex.png)](docs/notation.md#다음-큐까지-몇-초를-셀까--katex)<br>[Walkthrough](docs/notation.md#다음-큐까지-몇-초를-셀까--katex) |

</details>

> [!CAUTION]
> Re-rendering the data gallery overwrites existing PNG files under `docs/art/data/` by default. To preview regenerated charts safely without clobbering tracked assets, pass an alternate output directory: `python render.py --output preview` inside [`examples/data/`](examples/data/README.md#출력).

---

## 🌍 Live Interactive GeoJSON Map & GitHub Techniques

GitHub renders the `geojson` block below as a **live, zoomable, clickable vector map** directly inside this README — synchronized with [`docs/art/elements/shuttle.geojson`](docs/art/elements/shuttle.geojson) and [`examples/data/show.json`](examples/data/show.json):

```geojson
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {"title": "A · 집결", "marker-color": "#27aaa6"},
      "geometry": {"type": "Point", "coordinates": [126.9754, 37.5741]}
    },
    {
      "type": "Feature",
      "properties": {"title": "B · 환승", "marker-color": "#d33b90"},
      "geometry": {"type": "Point", "coordinates": [126.9836, 37.5708]}
    },
    {
      "type": "Feature",
      "properties": {"title": "C · 무대", "marker-color": "#799326"},
      "geometry": {"type": "Point", "coordinates": [126.9774, 37.5662]}
    },
    {
      "type": "Feature",
      "properties": {"title": "방문 순서 A → B → C", "stroke": "#228582"},
      "geometry": {
        "type": "LineString",
        "coordinates": [[126.9754, 37.5741], [126.9836, 37.5708], [126.9774, 37.5662]]
      }
    }
  ]
}
```

> [!WARNING]
> GeoJSON coordinates strictly follow **`[longitude, latitude]`** order. Swapping Seoul's longitude (`126.9754`) into the latitude slot produces an invalid out-of-range coordinate (`|lat| > 90`). Inspect the validated coordinates in [`docs/art/elements/shuttle.geojson`](docs/art/elements/shuttle.geojson).

Explore all 6 core GitHub Markdown patterns + copyable templates in the full field guide: [**✨ GitHub Markdown Field Guide**](docs/github-elements.md) and [**📐 Copy-Paste Pattern Reference**](plugins/md-viz/skills/md-viz/references/markdown-patterns.md).

---

## 🔌 Install in One Command

All three AI coding agents install the **exact same single-source plugin** (`plugins/md-viz/`, MIT licensed) bundling `SKILL.md`, `markdown-patterns.md`, `scripts/badge.py`, and `scripts/check_env.py`.

### Antigravity CLI (`agy`)

```sh
agy plugin install https://github.com/Technoetic/md-viz/tree/main/plugins/md-viz
```

> <kbd>/md-viz</kbd> `Turn README.md into a maximum-impact visual showcase using every applicable library and GitHub technique.`

### Claude Code

```sh
claude plugin marketplace add Technoetic/md-viz
claude plugin install md-viz@technoetic-md-viz
```

> <kbd>/md-viz:md-viz</kbd> `Visualize the architecture, metrics, and timing flow in this spec with maximum visual contrast.`

### Codex

```sh
codex plugin marketplace add Technoetic/md-viz
codex plugin add md-viz@technoetic-md-viz
```

> <kbd>$md-viz:md-viz</kbd> `Convert every table, workflow, and formula in README.md into vivid visuals and report exact tool coverage.`

### 🔍 Local Renderer Preflight (Zero Dependencies)

Run the bundled preflight script anytime to see which of the 25 engines are ready on your machine:

```sh
python plugins/md-viz/skills/md-viz/scripts/check_env.py
```

> [!IMPORTANT]
> The plugin installs orchestration rules plus two zero-dependency Python stdlib scripts (`badge.py` and `check_env.py`). External diagram, chart, and math engines must be available locally when generating new images; all pre-rendered gallery assets in this repo work immediately on GitHub and offline. See [`examples/data/README.md`](examples/data/README.md#준비).

> [!TIP]
> Default invocation goes **full-throttle** across all 25 engines and 6+4 GitHub patterns — or narrow it anytime with a single phrase like *"Mermaid flowchart only"* or *"generate one neon SVG badge with `badge.py`"*.

---

## 📁 Repository Architecture

```text
md-viz/                         ← Repository root (MIT)
├── LICENSE                     ← MIT open-source license
├── SECURITY.md                 ← Security policy & boundaries
├── README.ko.md                ← Full Korean showcase parity
├── .github/                    ← Automation workflows
│   └── workflows/              ← GitHub Actions definitions
│       └── ci.yml              ← Ubuntu + Windows CI & ZIP check
├── plugins/md-viz/             ← Slim installable 3-host plugin
│   ├── plugin.json             ← Antigravity manifest (v0.3.0)
│   ├── LICENSE                 ← Bundled MIT license
│   ├── README.md               ← Plugin-local quick-start
│   └── skills/md-viz/          ← Shared skill, patterns & tools
│       ├── SKILL.md            ← Full-arsenal overdrive spec
│       └── scripts/            ← Zero-dependency stdlib scripts
│           ├── badge.py        ← 28px two-tone neon SVG badges
│           └── check_env.py    ← 25-engine local preflight
├── docs/                       ← 25-tool galleries & live art
│   ├── github-elements.md      ← Live 6-pattern field guide
│   └── art/                    ← Rendered PNG, GIF, SVG & GeoJSON
├── examples/                   ← Reproducible inputs & renderers
│   ├── badges.py               ← Regenerate all 20 SVG badges
│   └── data/                   ← Show JSON & 12-chart pipeline
├── tools/                      ← Release engineering helpers
│   └── build_release_zip.py    ← Deterministic UTC slim ZIP
└── tests/                      ← Gallery, badge & plugin tests
```

Regenerate all 20 SVG badges byte-identically from the repo root with `python examples/badges.py`, or build a deterministic slim plugin ZIP with `python tools/build_release_zip.py --version v0.3.0 --out dist`.
