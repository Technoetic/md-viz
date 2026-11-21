"""Draw four NEON ENCORE charts into a temporary web preview directory."""
import json
import sys
from pathlib import Path

import altair as alt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import vl_convert as vl

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
DATA = json.loads((HERE / "show.json").read_text(encoding="utf-8"))
BG, FG, GRID = "#101425", "#E9EDFF", "#343B53"
CYAN, PINK, LIME = "#71E7E1", "#FE72B7", "#DAF777"
THEME = {
    "view": {"stroke": None}, "background": BG, "font": "Arial",
    "axis": {"labelColor": FG, "titleColor": FG, "gridColor": GRID, "domain": False,
             "labelFontSize": 16, "titleFontSize": 15, "tickColor": GRID, "titlePadding": 10},
    "legend": {"titleColor": FG, "labelColor": FG, "labelFontSize": 16},
}


def svg(name, spec):
    spec.update(width=720, height=202, config=THEME, background=BG)
    (OUT / (name + ".svg")).write_text(vl.vegalite_to_svg(spec), encoding="utf-8")


def admission_waves():
    series = DATA["admissions"]
    rows = [{"minute": minute, "gate": gate, "people": series[gate][i]}
            for i, minute in enumerate(series["minutes"]) for gate in ("North", "East", "West")]
    svg("vega-lite", {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"values": rows},
        "mark": {"type": "area", "opacity": 0.96, "line": {"color": BG, "strokeWidth": 1.5}},
        "encoding": {
            "x": {"field": "minute", "type": "quantitative", "axis": {"title": "Minutes after 18:00", "grid": False,
                  "values": [0, 10, 20, 30, 40, 50]}},
            "y": {"field": "people", "type": "quantitative", "stack": "zero", "title": "Admissions per 10 min"},
            "color": {"field": "gate", "type": "nominal", "legend": {"title": None, "orient": "top"},
                      "scale": {"domain": ["North", "East", "West"], "range": [CYAN, PINK, LIME]}},
            "order": {"field": "gate", "sort": "ascending"},
        },
    })


def spotlights():
    beams = DATA["beams"]
    with plt.rc_context({"font.size": 13, "text.color": FG, "axes.labelcolor": FG,
                         "xtick.color": FG, "ytick.color": FG}):
        fig = plt.figure(figsize=(8.8, 3.1), facecolor=BG)
        ax = fig.add_axes([0.05, 0.05, 0.68, 0.86], projection="polar", facecolor=BG)
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_thetamin(-85)
        ax.set_thetamax(85)
        ax.set_ylim(0, 100)
        ax.set_xticks(np.deg2rad([-75, -45, -15, 15, 45, 75]))
        ax.set_yticks([25, 50, 75, 100], labels=[])
        ax.spines["polar"].set_color(GRID)
        ax.grid(color=GRID)
        for key, color in [("Cyan", CYAN), ("Amber", LIME)]:
            theta = np.deg2rad(beams["degrees"])
            ax.fill(theta, beams[key], color=color, alpha=0.23)
            ax.plot(theta, beams[key], "o-", color=color, ms=3, lw=2.8)
        fig.text(.76, .68, "CYAN", color=CYAN, weight="bold")
        fig.text(.76, .57, "peak   −15°", fontsize=16)
        fig.text(.76, .40, "AMBER", color=LIME, weight="bold")
        fig.text(.76, .29, "peak   +30°", fontsize=16)
        fig.savefig(OUT / "matplotlib.png", dpi=135, facecolor=BG)
        plt.close(fig)


def audience_heat():
    a = DATA["audience"]
    fig, ax = plt.subplots(figsize=(8.8, 2.8), facecolor=BG)
    frame = pd.DataFrame(a["index"], index=a["tracks"], columns=a["zones"]).T
    sns.heatmap(frame, ax=ax, cmap=sns.blend_palette(["#172341", "#385779", "#B74C9C", "#FF8C9D"], as_cmap=True),
                vmin=0, vmax=100, annot=True, fmt="d", cbar=False, linewidths=2, linecolor=BG,
                annot_kws={"fontsize": 13, "weight": "bold", "color": "white"})
    ax.tick_params(colors=FG, labelsize=12, length=0, pad=7)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    fig.subplots_adjust(left=.15, right=.993, top=.985, bottom=.16)
    fig.savefig(OUT / "seaborn.png", dpi=140, facecolor=BG)
    plt.close(fig)


def check_time():
    parts = pd.DataFrame(DATA["soundcheck"])
    y = alt.Y("part:N", sort=parts.part.tolist(), title=None, axis=alt.Axis(labelPadding=10))
    points = parts.melt(id_vars="part", var_name="series", value_name="minutes")
    rules = alt.Chart(parts).mark_rule(color="#64738C", strokeWidth=5).encode(
        y=y, x=alt.X("plan:Q", title="Minutes", scale=alt.Scale(domain=[0,10])), x2="actual:Q")
    dots = alt.Chart(points).mark_point(filled=True, size=190, stroke=BG, strokeWidth=1.8).encode(
        y=y, x="minutes:Q", color=alt.Color("series:N", scale=alt.Scale(domain=["plan","actual"], range=[CYAN,PINK]),
                                          legend=alt.Legend(orient="top", title=None)),
        shape=alt.Shape("series:N", scale=alt.Scale(domain=["plan","actual"], range=["diamond","circle"]), legend=None))
    svg("altair", (rules + dots).to_dict())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    admission_waves()
    spotlights()
    audience_heat()
    check_time()
