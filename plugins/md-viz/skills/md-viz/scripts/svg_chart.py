"""Zero-install GitHub README.md pure-SVG visual generator (Python 3 stdlib only, 10 dark-neon visual types)."""
import argparse
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

BG = "#0B0F1A"
PANEL = "#131621"
BORDER = "#27304A"
GRID = "#1E293B"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
NEON = ("#00F5D4", "#FF2E93", "#C8FF00", "#FFBB54", "#C084FC", "#38BDF8")

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
SLOT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FORBIDDEN_SVG_TAGS = {"script", "foreignobject", "iframe", "embed", "object"}
CHART_TYPES = ("hero", "kpi", "bar", "line", "donut", "heatmap", "waterfall", "radar", "sankey", "timeline")


def validate_hex(color, default="#00F5D4"):
    val = default if color is None else str(color)
    if not HEX_RE.fullmatch(val):
        raise ValueError(f"Expected 6-digit hex color like #00F5D4, got {val!r}")
    return val


def esc(value):
    return html.escape(str(value), quote=True)


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(ch) in ("F", "W") else 1 for ch in str(text))


def pick_ink(hex_color):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return "#0B0F1A" if luminance > 0.58 else "#F8FAFC"


def lerp_hex(c1, c2, t):
    t = max(0.0, min(1.0, float(t)))
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def heat_color(t):
    stops = ("#141D38", "#1E4B6E", "#8A3AB9", "#FF2E93", "#FFBB54")
    t = max(0.0, min(1.0, float(t)))
    scaled = t * (len(stops) - 1)
    idx = min(len(stops) - 2, int(scaled))
    return lerp_hex(stops[idx], stops[idx + 1], scaled - idx)


def card_shell(width, height, title, subtitle, accent, body_parts, defs=""):
    accent = validate_hex(accent)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f'  <title>{esc(title)}</title>',
    ]
    if defs:
        parts.append(f"  <defs>{defs}</defs>")
    parts.extend([
        f'  <rect width="{width}" height="{height}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'  <rect x="0" y="0" width="{width}" height="5" rx="2" fill="{accent}"/>',
        f'  <text x="26" y="38" fill="{TEXT}" font-family="ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif" font-size="19" font-weight="700">{esc(title)}</text>',
        f'  <text x="{width - 26}" y="38" text-anchor="end" fill="{accent}" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="12" font-weight="700">{esc(subtitle)}</text>',
    ])
    parts.extend("  " + p for p in body_parts)
    parts.append("</svg>\n")
    return "\n".join(parts), width, height


def render_hero(spec):
    width = int(spec.get("width", 1040))
    height = int(spec.get("height", 260))
    title = str(spec.get("title", "PROJECT SHOWCASE"))
    tagline = str(spec.get("tagline", "Zero-install GitHub README visual banner"))
    kicker = str(spec.get("kicker", "ZERO-INSTALL GITHUB README"))
    accent = validate_hex(spec.get("accent", "#00F5D4"))
    accent2 = validate_hex(spec.get("accent2", "#FF2E93"))
    accent3 = validate_hex(spec.get("accent3", "#C8FF00"))
    pills = spec.get("pills") or ["ZERO DEPS", "PURE SVG", "GITHUB NATIVE"]

    defs = (
        f'<linearGradient id="heroBar" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'<stop offset="0%" stop-color="{accent}"/>'
        f'<stop offset="50%" stop-color="{accent2}"/>'
        f'<stop offset="100%" stop-color="{accent3}"/>'
        f"</linearGradient>"
        f'<linearGradient id="heroGlow" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{accent}" stop-opacity="0.14"/>'
        f'<stop offset="55%" stop-color="{accent2}" stop-opacity="0.10"/>'
        f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/>'
        f"</linearGradient>"
    )
    grid = []
    for gx in range(40, width, 48):
        grid.append(f'<line x1="{gx}" y1="6" x2="{gx}" y2="{height - 6}" stroke="#172038" stroke-width="1"/>')
    for gy in range(40, height, 48):
        grid.append(f'<line x1="6" y1="{gy}" x2="{width - 6}" y2="{gy}" stroke="#172038" stroke-width="1"/>')

    # Decorative neon arcs on the right side
    cx, cy = width - 106, height // 2 + 4
    rings = [
        f'<circle cx="{cx}" cy="{cy}" r="76" fill="none" stroke="{accent}" stroke-width="2" stroke-opacity="0.35" stroke-dasharray="16 8"/>',
        f'<circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{accent2}" stroke-width="3" stroke-opacity="0.6" stroke-dasharray="24 8"/>',
        f'<circle cx="{cx}" cy="{cy}" r="28" fill="none" stroke="{accent3}" stroke-width="3" stroke-opacity="0.85"/>',
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="{accent}"/>',
    ]

    pill_svg = []
    px = 42
    py = height - 62
    for i, pill in enumerate(pills[:6]):
        pcol = NEON[i % len(NEON)]
        pw = max(84, display_width(pill) * 9 + 26)
        ink = pick_ink(pcol)
        pill_svg.append(
            f'<rect x="{px}" y="{py}" width="{pw}" height="30" rx="6" fill="{pcol}"/>'
            f'<text x="{px + pw / 2:.1f}" y="{py + 20}" text-anchor="middle" fill="{ink}" font-family="ui-monospace, Consolas, monospace" font-size="12" font-weight="700">{esc(pill)}</text>'
        )
        px += pw + 12

    svg = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f'  <title>{esc(title)} — {esc(tagline)}</title>',
        f'  <defs>{defs}</defs>',
        f'  <rect width="{width}" height="{height}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'  <rect width="{width}" height="{height}" rx="14" fill="url(#heroGlow)"/>',
        *("  " + g for g in grid),
        f'  <rect x="0" y="0" width="{width}" height="6" rx="3" fill="url(#heroBar)"/>',
        *("  " + r for r in rings),
        f'  <text x="42" y="54" fill="{accent}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="700" letter-spacing="1.5">{esc(kicker)}</text>',
        f'  <text x="42" y="114" fill="{TEXT}" font-family="ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif" font-size="40" font-weight="800">{esc(title)}</text>',
        f'  <text x="42" y="154" fill="#CBD5E1" font-family="ui-sans-serif, system-ui, Segoe UI, Arial, sans-serif" font-size="17">{esc(tagline)}</text>',
        *("  " + p for p in pill_svg),
        "</svg>\n",
    ])
    return svg, width, height


def render_kpi(spec):
    items = spec.get("items") or []
    if not items:
        raise ValueError("kpi spec requires a non-empty 'items' list")
    title = spec.get("title", "Key Metrics")
    subtitle = spec.get("subtitle", "KPI STRIP")
    accent = validate_hex(spec.get("accent", "#00F5D4"))
    cols = max(1, min(len(items), int(spec.get("columns", 4))))
    rows = math.ceil(len(items) / cols)
    card_w = int(spec.get("card_width", 228))
    card_h = 104
    gap = 16
    pad = 26
    width = max(560, pad * 2 + cols * card_w + (cols - 1) * gap)
    height = 70 + rows * card_h + (rows - 1) * gap + 24

    parts = []
    for i, item in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (card_w + gap)
        y = 62 + r * (card_h + gap)
        col = validate_hex(item.get("color"), NEON[i % len(NEON)])
        delta = item.get("delta")
        parts.append(
            f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="9" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>'
            f'<rect x="{x}" y="{y}" width="{card_w}" height="4" rx="2" fill="{col}"/>'
            f'<text x="{x + 14}" y="{y + 28}" fill="{MUTED}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="600">{esc(item.get("label", ""))}</text>'
            f'<text x="{x + 14}" y="{y + 68}" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="28" font-weight="800">{esc(item.get("value", ""))}</text>'
            f'<text x="{x + 14}" y="{y + 90}" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="11">{esc(item.get("note", ""))}</text>'
        )
        if delta:
            dw = max(46, display_width(delta) * 8 + 14)
            dx = x + card_w - dw - 10
            parts.append(
                f'<rect x="{dx}" y="{y + 14}" width="{dw}" height="20" rx="4" fill="#1E293B" stroke="{col}" stroke-width="1"/>'
                f'<text x="{dx + dw / 2:.1f}" y="{y + 28}" text-anchor="middle" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="11" font-weight="700">{esc(delta)}</text>'
            )
    return card_shell(width, height, title, subtitle, accent, parts)


def render_bar(spec):
    items = spec.get("items") or []
    if not items:
        raise ValueError("bar spec requires a non-empty 'items' list")
    title = spec.get("title", "Comparison")
    subtitle = spec.get("subtitle", "BAR CHART")
    accent = validate_hex(spec.get("accent", "#00F5D4"))
    unit = str(spec.get("unit", ""))
    orientation = spec.get("orientation", "horizontal")

    if orientation == "vertical":
        width = int(spec.get("width", max(640, 120 + len(items) * 96)))
        height = int(spec.get("height", 360))
        left, right, top, bottom = 68, 32, 74, 58
        plot_w = width - left - right
        plot_h = height - top - bottom
        max_v = max(1e-9, *(float(it["value"]) for it in items))
        parts = []
        for g in range(5):
            gy = top + plot_h - (plot_h * g / 4)
            gv = max_v * g / 4
            parts.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{width - right}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>')
            parts.append(f'<text x="{left - 10}" y="{gy + 4:.1f}" text-anchor="end" fill="{MUTED}" font-family="ui-monospace, Consolas, monospace" font-size="11">{gv:g}</text>')
        step = plot_w / len(items)
        bar_w = min(62, step * 0.58)
        for i, it in enumerate(items):
            val = float(it["value"])
            col = validate_hex(it.get("color"), NEON[i % len(NEON)])
            bh = max(4.0, (val / max_v) * plot_h)
            bx = left + i * step + (step - bar_w) / 2
            by = top + plot_h - bh
            parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="5" fill="{col}"/>')
            parts.append(f'<text x="{bx + bar_w / 2:.1f}" y="{by - 8:.1f}" text-anchor="middle" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="700">{esc(it["value"])}{esc(unit)}</text>')
            parts.append(f'<text x="{bx + bar_w / 2:.1f}" y="{height - 24}" text-anchor="middle" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="600">{esc(it["label"])}</text>')
        return card_shell(width, height, title, subtitle, accent, parts)

    width = int(spec.get("width", 800))
    row_h = 42
    pad = 26
    label_w = max(130, min(250, max(display_width(it["label"]) for it in items) * 9 + 20))
    val_w = 104
    bar_max = max(180, width - pad * 2 - label_w - val_w)
    height = max(180, 84 + len(items) * row_h)
    max_v = max(1e-9, *(float(it["value"]) for it in items))
    parts = []
    for i, it in enumerate(items):
        y = 70 + i * row_h
        val = float(it["value"])
        col = validate_hex(it.get("color"), NEON[i % len(NEON)])
        bw = max(6, round((val / max_v) * bar_max))
        parts.append(f'<text x="{pad + label_w - 12}" y="{y + 18}" text-anchor="end" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="600">{esc(it["label"])}</text>')
        parts.append(f'<rect x="{pad + label_w}" y="{y}" width="{bar_max}" height="26" rx="6" fill="{PANEL}"/>')
        parts.append(f'<rect x="{pad + label_w}" y="{y}" width="{bw}" height="26" rx="6" fill="{col}"/>')
        parts.append(f'<text x="{pad + label_w + bar_max + 12}" y="{y + 18}" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="14" font-weight="700">{esc(it["value"])}{esc(unit)}</text>')
    return card_shell(width, height, title, subtitle, accent, parts)


def render_line(spec):
    x_labels = spec.get("x") or []
    series_list = spec.get("series") or []
    if len(x_labels) < 2 or not series_list:
        raise ValueError("line spec requires 'x' (>=2 points) and non-empty 'series'")
    title = spec.get("title", "Trend")
    subtitle = spec.get("subtitle", "LINE / AREA")
    accent = validate_hex(spec.get("accent", "#00F5D4"))
    fill_area = bool(spec.get("area", True))
    width = int(spec.get("width", 840))
    height = int(spec.get("height", 370))
    left, right, top, bottom = 68, 34, 88, 54
    plot_w = width - left - right
    plot_h = height - top - bottom

    all_vals = [float(v) for s in series_list for v in s.get("values", ())]
    if not all_vals or any(len(s.get("values", ())) != len(x_labels) for s in series_list):
        raise ValueError("Each line series must have a 'values' list matching len(x)")
    min_v = min(0.0, min(all_vals))
    max_v = max(all_vals)
    if math.isclose(min_v, max_v):
        max_v = min_v + 1.0

    parts = []
    defs = []
    for g in range(5):
        gy = top + plot_h - (plot_h * g / 4)
        gv = min_v + (max_v - min_v) * g / 4
        parts.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{width - right}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 10}" y="{gy + 4:.1f}" text-anchor="end" fill="{MUTED}" font-family="ui-monospace, Consolas, monospace" font-size="11">{gv:g}</text>')

    for idx, label in enumerate(x_labels):
        px = left + (plot_w * idx / (len(x_labels) - 1))
        parts.append(f'<text x="{px:.1f}" y="{height - 20}" text-anchor="middle" fill="{MUTED}" font-family="ui-monospace, Consolas, monospace" font-size="12">{esc(label)}</text>')

    lx = left
    for s_idx, s in enumerate(series_list):
        col = validate_hex(s.get("color"), NEON[s_idx % len(NEON)])
        vals = [float(v) for v in s["values"]]
        pts = [
            (left + (plot_w * i / (len(x_labels) - 1)), top + plot_h - ((v - min_v) / (max_v - min_v)) * plot_h)
            for i, v in enumerate(vals)
        ]
        if fill_area:
            gid = f"areaGrad{s_idx}"
            defs.append(
                f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0%" stop-color="{col}" stop-opacity="0.28"/>'
                f'<stop offset="100%" stop-color="{col}" stop-opacity="0.02"/>'
                f"</linearGradient>"
            )
            poly_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" {pts[-1][0]:.1f},{top + plot_h:.1f} {pts[0][0]:.1f},{top + plot_h:.1f}"
            parts.append(f'<polygon points="{poly_pts}" fill="url(#{gid})"/>')
        line_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polyline fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="{line_pts}"/>')
        for x, y in pts:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{col}" stroke="{BG}" stroke-width="1.8"/>')
        name = str(s.get("name", f"Series {s_idx + 1}"))
        parts.append(f'<rect x="{lx}" y="58" width="12" height="12" rx="3" fill="{col}"/>')
        parts.append(f'<text x="{lx + 18}" y="69" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="600">{esc(name)}</text>')
        lx += display_width(name) * 9 + 40

    return card_shell(width, height, title, subtitle, accent, parts, defs="".join(defs))


def render_donut(spec):
    items = spec.get("items") or []
    if not items:
        raise ValueError("donut spec requires a non-empty 'items' list")
    title = spec.get("title", "Distribution")
    subtitle = spec.get("subtitle", "DONUT RING")
    accent = validate_hex(spec.get("accent", "#00F5D4"))
    unit = str(spec.get("unit", ""))
    center_label = str(spec.get("center_label", "TOTAL"))
    width = int(spec.get("width", 760))
    height = int(spec.get("height", max(320, 120 + len(items) * 38)))
    cx, cy = 195, height // 2 + 16
    r_out = min(122, height // 2 - 48)
    r_in = r_out * 0.58
    total = sum(float(it["value"]) for it in items)
    if total <= 0:
        raise ValueError("donut values must sum to > 0")

    parts = []
    angle = -math.pi / 2
    for i, it in enumerate(items):
        val = float(it["value"])
        frac = val / total
        sweep = max(0.01, frac * 2 * math.pi - 0.025)
        a0 = angle
        a1 = angle + sweep
        angle += frac * 2 * math.pi
        col = validate_hex(it.get("color"), NEON[i % len(NEON)])
        large = 1 if sweep > math.pi else 0
        x0_o, y0_o = cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)
        x1_o, y1_o = cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)
        x1_i, y1_i = cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)
        x0_i, y0_i = cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)
        d = (
            f"M {x0_o:.2f} {y0_o:.2f} A {r_out:.2f} {r_out:.2f} 0 {large} 1 {x1_o:.2f} {y1_o:.2f} "
            f"L {x1_i:.2f} {y1_i:.2f} A {r_in:.2f} {r_in:.2f} 0 {large} 0 {x0_i:.2f} {y0_i:.2f} Z"
        )
        parts.append(f'<path d="{d}" fill="{col}"/>')

        ly = 94 + i * 38
        pct = frac * 100
        parts.append(f'<rect x="380" y="{ly - 12}" width="14" height="14" rx="3" fill="{col}"/>')
        parts.append(f'<text x="404" y="{ly}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="600">{esc(it["label"])}</text>')
        parts.append(f'<text x="{width - 28}" y="{ly}" text-anchor="end" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="14" font-weight="700">{esc(it["value"])}{esc(unit)} ({pct:.1f}%)</text>')

    total_str = f"{total:g}{unit}"
    parts.append(f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" fill="{TEXT}" font-family="ui-monospace, Consolas, monospace" font-size="25" font-weight="800">{esc(total_str)}</text>')
    parts.append(f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" fill="{MUTED}" font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="700">{esc(center_label)}</text>')
    return card_shell(width, height, title, subtitle, accent, parts)


def render_heatmap(spec):
    rows = spec.get("rows") or []
    cols = spec.get("columns") or []
    matrix = spec.get("matrix") or []
    if not rows or not cols or len(matrix) != len(rows):
        raise ValueError("heatmap spec requires 'rows', 'columns', and matching 'matrix'")
    title = spec.get("title", "Matrix Heatmap")
    subtitle = spec.get("subtitle", "HEATMAP")
    accent = validate_hex(spec.get("accent", "#FF2E93"))

    flat = [float(v) for row in matrix for v in row]
    lo = float(spec.get("vmin", min(flat)))
    hi = float(spec.get("vmax", max(flat)))
    span = max(1e-9, hi - lo)

    label_w = max(100, max(display_width(r) for r in rows) * 9 + 24)
    cell_w = max(72, min(116, int(spec.get("cell_width", 96))))
    cell_h = 44
    gap = 6
    pad = 26
    width = pad * 2 + label_w + len(cols) * cell_w + (len(cols) - 1) * gap
    height = 96 + len(rows) * cell_h + (len(rows) - 1) * gap + 24

    parts = []
    for c_idx, cname in enumerate(cols):
        cx = pad + label_w + c_idx * (cell_w + gap) + cell_w / 2
        parts.append(f'<text x="{cx:.1f}" y="76" text-anchor="middle" fill="{MUTED}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="700">{esc(cname)}</text>')

    for r_idx, rname in enumerate(rows):
        y = 88 + r_idx * (cell_h + gap)
        parts.append(f'<text x="{pad + label_w - 12}" y="{y + 27}" text-anchor="end" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="600">{esc(rname)}</text>')
        for c_idx, val in enumerate(matrix[r_idx]):
            x = pad + label_w + c_idx * (cell_w + gap)
            t = (float(val) - lo) / span
            fill = heat_color(t)
            ink = pick_ink(fill)
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="6" fill="{fill}"/>')
            parts.append(f'<text x="{x + cell_w / 2:.1f}" y="{y + 27}" text-anchor="middle" fill="{ink}" font-family="ui-monospace, Consolas, monospace" font-size="14" font-weight="700">{esc(val)}</text>')
    return card_shell(width, height, title, subtitle, accent, parts)


def render_waterfall(spec):
    items = spec.get("items") or []
    if len(items) < 2:
        raise ValueError("waterfall spec requires at least 2 items")
    title = spec.get("title", "Delta Breakdown")
    subtitle = spec.get("subtitle", "WATERFALL")
    accent = validate_hex(spec.get("accent", "#38BDF8"))
    unit = str(spec.get("unit", ""))

    bars = []
    running = 0.0
    for idx, it in enumerate(items):
        kind = it.get("type")
        val = float(it["value"])
        if kind == "total" or (kind is None and (idx == 0 or idx == len(items) - 1)):
            low, high = min(0.0, val), max(0.0, val)
            running = val
            col = validate_hex(it.get("color"), "#38BDF8")
            label_val = f"{val:g}{unit}"
        else:
            start = running
            end = running + val
            low, high = min(start, end), max(start, end)
            running = end
            col = validate_hex(it.get("color"), "#C8FF00" if val >= 0 else "#FF2E93")
            label_val = f"{val:+g}{unit}"
        bars.append({"label": it["label"], "low": low, "high": high, "end": running, "color": col, "text": label_val})

    width = int(spec.get("width", max(700, 120 + len(bars) * 118)))
    height = int(spec.get("height", 360))
    left, right, top, bottom = 68, 32, 74, 58
    plot_w, plot_h = width - left - right, height - top - bottom
    min_y = min(0.0, *(b["low"] for b in bars))
    max_y = max(1e-9, *(b["high"] for b in bars)) * 1.12
    span = max(1e-9, max_y - min_y)

    def y_pos(v):
        return top + plot_h - ((v - min_y) / span) * plot_h

    parts = []
    for g in range(5):
        gv = min_y + span * g / 4
        gy = y_pos(gv)
        parts.append(f'<line x1="{left}" y1="{gy:.1f}" x2="{width - right}" y2="{gy:.1f}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(f'<text x="{left - 10}" y="{gy + 4:.1f}" text-anchor="end" fill="{MUTED}" font-family="ui-monospace, Consolas, monospace" font-size="11">{gv:g}</text>')

    step = plot_w / len(bars)
    bw = min(68, step * 0.56)
    prev_end_x = None
    prev_end_y = None
    for i, b in enumerate(bars):
        bx = left + i * step + (step - bw) / 2
        y_top = y_pos(b["high"])
        y_bot = y_pos(b["low"])
        bh = max(4.0, y_bot - y_top)
        if prev_end_x is not None:
            parts.append(f'<line x1="{prev_end_x:.1f}" y1="{prev_end_y:.1f}" x2="{bx:.1f}" y2="{prev_end_y:.1f}" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 4"/>')
        parts.append(f'<rect x="{bx:.1f}" y="{y_top:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="5" fill="{b["color"]}"/>')
        parts.append(f'<text x="{bx + bw / 2:.1f}" y="{y_top - 8:.1f}" text-anchor="middle" fill="{b["color"]}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="700">{esc(b["text"])}</text>')
        parts.append(f'<text x="{bx + bw / 2:.1f}" y="{height - 24}" text-anchor="middle" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="600">{esc(b["label"])}</text>')
        prev_end_x = bx + bw
        prev_end_y = y_pos(b["end"])
    return card_shell(width, height, title, subtitle, accent, parts)


def render_radar(spec):
    axes = spec.get("axes") or []
    series_list = spec.get("series") or []
    if len(axes) < 3 or not series_list:
        raise ValueError("radar spec requires >=3 'axes' and non-empty 'series'")
    title = spec.get("title", "Capability Radar")
    subtitle = spec.get("subtitle", "RADAR PROFILE")
    accent = validate_hex(spec.get("accent", "#C084FC"))
    max_v = float(spec.get("max", max(float(v) for s in series_list for v in s["values"]) or 100))
    width = int(spec.get("width", 760))
    height = int(spec.get("height", 420))
    cx, cy = 248, height // 2 + 18
    radius = min(138, height // 2 - 64)
    n = len(axes)

    parts = []
    for ring in (0.25, 0.5, 0.75, 1.0):
        pts = []
        for i in range(n):
            ang = -math.pi / 2 + (2 * math.pi * i / n)
            pts.append(f"{cx + radius * ring * math.cos(ang):.1f},{cy + radius * ring * math.sin(ang):.1f}")
        parts.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{GRID}" stroke-width="1.2"/>')

    for i, axis_name in enumerate(axes):
        ang = -math.pi / 2 + (2 * math.pi * i / n)
        x2, y2 = cx + radius * math.cos(ang), cy + radius * math.sin(ang)
        lx, ly = cx + (radius + 24) * math.cos(ang), cy + (radius + 24) * math.sin(ang)
        anchor = "middle" if abs(math.cos(ang)) < 0.25 else ("start" if math.cos(ang) > 0 else "end")
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="{anchor}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="12" font-weight="600">{esc(axis_name)}</text>')

    for s_idx, s in enumerate(series_list):
        col = validate_hex(s.get("color"), NEON[s_idx % len(NEON)])
        vals = [float(v) for v in s["values"]]
        pts = []
        for i, v in enumerate(vals):
            ang = -math.pi / 2 + (2 * math.pi * i / n)
            r = radius * max(0.0, min(1.0, v / max_v))
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        parts.append(f'<polygon points="{poly}" fill="{col}" fill-opacity="0.22" stroke="{col}" stroke-width="2.6"/>')
        for x, y in pts:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" stroke="{BG}" stroke-width="1.5"/>')
        ly = 110 + s_idx * 34
        parts.append(f'<rect x="490" y="{ly - 11}" width="14" height="14" rx="3" fill="{col}"/>')
        parts.append(f'<text x="514" y="{ly}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="600">{esc(s.get("name", f"Series {s_idx + 1}"))}</text>')
    return card_shell(width, height, title, subtitle, accent, parts)


def render_sankey(spec):
    links = spec.get("links") or []
    if not links:
        raise ValueError("sankey spec requires non-empty 'links'")
    title = spec.get("title", "Flow Breakdown")
    subtitle = spec.get("subtitle", "SANKEY FLOW")
    accent = validate_hex(spec.get("accent", "#FFBB54"))
    unit = str(spec.get("unit", ""))

    sources = {}
    targets = {}
    for lk in links:
        v = float(lk["value"])
        sources[lk["source"]] = sources.get(lk["source"], 0.0) + v
        targets[lk["target"]] = targets.get(lk["target"], 0.0) + v

    width = int(spec.get("width", 820))
    height = int(spec.get("height", 360))
    top, bottom = 78, 30
    avail_h = height - top - bottom
    gap = 18

    def layout_column(totals):
        keys = list(totals.keys())
        total_v = sum(totals.values())
        if total_v <= 0:
            raise ValueError("sankey link values must sum to > 0")
        usable = avail_h - gap * max(0, len(keys) - 1)
        y = float(top)
        boxes = {}
        for i, k in enumerate(keys):
            h = max(14.0, (totals[k] / total_v) * usable)
            boxes[k] = {"y": y, "h": h, "val": totals[k], "cursor": y, "color": NEON[i % len(NEON)]}
            y += h + gap
        return boxes

    src_boxes = layout_column(sources)
    tgt_boxes = layout_column(targets)
    x_left, x_right = 178, width - 196
    node_w = 18

    parts = []
    for lk in links:
        sb = src_boxes[lk["source"]]
        tb = tgt_boxes[lk["target"]]
        v = float(lk["value"])
        sh = sb["h"] * (v / sb["val"])
        th = tb["h"] * (v / tb["val"])
        y0_top, y0_bot = sb["cursor"], sb["cursor"] + sh
        y1_top, y1_bot = tb["cursor"], tb["cursor"] + th
        sb["cursor"] += sh
        tb["cursor"] += th
        mx = (x_left + node_w + x_right) / 2
        d = (
            f"M {x_left + node_w} {y0_top:.1f} C {mx:.1f} {y0_top:.1f}, {mx:.1f} {y1_top:.1f}, {x_right} {y1_top:.1f} "
            f"L {x_right} {y1_bot:.1f} C {mx:.1f} {y1_bot:.1f}, {mx:.1f} {y0_bot:.1f}, {x_left + node_w} {y0_bot:.1f} Z"
        )
        col = validate_hex(lk.get("color"), sb["color"])
        parts.append(f'<path d="{d}" fill="{col}" fill-opacity="0.38"/>')

    for name, b in src_boxes.items():
        parts.append(f'<rect x="{x_left}" y="{b["y"]:.1f}" width="{node_w}" height="{b["h"]:.1f}" rx="4" fill="{b["color"]}"/>')
        parts.append(f'<text x="{x_left - 10}" y="{b["y"] + b["h"] / 2 + 5:.1f}" text-anchor="end" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="600">{esc(name)} ({b["val"]:g}{esc(unit)})</text>')
    for i, (name, b) in enumerate(tgt_boxes.items()):
        tcol = NEON[(i + 3) % len(NEON)]
        parts.append(f'<rect x="{x_right}" y="{b["y"]:.1f}" width="{node_w}" height="{b["h"]:.1f}" rx="4" fill="{tcol}"/>')
        parts.append(f'<text x="{x_right + node_w + 10}" y="{b["y"] + b["h"] / 2 + 5:.1f}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="600">{esc(name)} ({b["val"]:g}{esc(unit)})</text>')
    return card_shell(width, height, title, subtitle, accent, parts)


def render_timeline(spec):
    tracks = spec.get("tracks") or []
    if not tracks:
        raise ValueError("timeline spec requires non-empty 'tracks'")
    steps = max(4, min(32, int(spec.get("steps", 16))))
    title = spec.get("title", "Execution Timeline")
    subtitle = spec.get("subtitle", f"{steps}-STEP MATRIX")
    accent = validate_hex(spec.get("accent", "#C8FF00"))
    width = int(spec.get("width", 840))
    row_h = 46
    pad = 26
    label_w = max(110, max(display_width(t["label"]) for t in tracks) * 9 + 18)
    gap = 5
    cell_w = max(14.0, (width - pad * 2 - label_w - gap * (steps - 1)) / steps)
    height = 90 + len(tracks) * row_h + 18

    parts = []
    for s in range(steps):
        if s % 4 == 0 or s == steps - 1:
            sx = pad + label_w + s * (cell_w + gap) + cell_w / 2
            parts.append(f'<text x="{sx:.1f}" y="70" text-anchor="middle" fill="{MUTED}" font-family="ui-monospace, Consolas, monospace" font-size="11">{s + 1}</text>')
    for r, track in enumerate(tracks):
        y = 82 + r * row_h
        col = validate_hex(track.get("color"), NEON[r % len(NEON)])
        active = set(track.get("active", []))
        parts.append(f'<text x="{pad + label_w - 12}" y="{y + 21}" text-anchor="end" fill="{col}" font-family="ui-monospace, Consolas, monospace" font-size="13" font-weight="700">{esc(track["label"])}</text>')
        for s in range(steps):
            x = pad + label_w + s * (cell_w + gap)
            on = s in active
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{cell_w:.1f}" height="30" rx="5" fill="{col if on else PANEL}" stroke="{col if on else BORDER}" stroke-width="1"/>')
    return card_shell(width, height, title, subtitle, accent, parts)


RENDERERS = {
    "hero": render_hero,
    "kpi": render_kpi,
    "bar": render_bar,
    "line": render_line,
    "donut": render_donut,
    "heatmap": render_heatmap,
    "waterfall": render_waterfall,
    "radar": render_radar,
    "sankey": render_sankey,
    "timeline": render_timeline,
}


def verify_github_safe_svg(svg_text):
    root = ET.fromstring(svg_text)
    if not root.tag.endswith("svg"):
        raise ValueError(f"Expected <svg> root, got {root.tag}")
    for elem in root.iter():
        local = elem.tag.rsplit("}", 1)[-1].lower()
        if local in FORBIDDEN_SVG_TAGS:
            raise ValueError(f"Forbidden GitHub SVG element: <{local}>")
        for attr, val in elem.attrib.items():
            alow = attr.rsplit("}", 1)[-1].lower()
            if alow.startswith("on") or "javascript:" in val.lower():
                raise ValueError(f"Forbidden SVG attribute: {attr}")
    return True


def update_readme_slot(readme_path, slot, snippet, append_if_missing=True):
    if not SLOT_RE.fullmatch(slot):
        raise ValueError(f"Invalid slot name {slot!r}")
    path = Path(readme_path)
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    start = f"<!-- md-viz:start:{slot} -->"
    end = f"<!-- md-viz:end:{slot} -->"
    block = f"{start}\n{snippet}\n{end}"
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pat.search(text):
        path.write_text(pat.sub(lambda _: block, text, count=1), encoding="utf-8")
        return "replaced"
    if not append_if_missing:
        raise ValueError(f"Slot {slot!r} not found in {path}")
    sep = "" if not text else ("\n\n" if not text.endswith("\n") else ("\n" if not text.endswith("\n\n") else ""))
    path.write_text(f"{text}{sep}{block}\n", encoding="utf-8")
    return "appended"


def generate_chart(chart_type, spec, out_path):
    if chart_type not in RENDERERS:
        raise ValueError(f"Unsupported chart type {chart_type!r}; choose from {CHART_TYPES}")
    svg_text, width, height = RENDERERS[chart_type](spec)
    verify_github_safe_svg(svg_text)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg_text, encoding="utf-8")
    return {
        "type": chart_type,
        "out": str(out.resolve()),
        "width": width,
        "height": height,
        "bytes": out.stat().st_size,
        "github_img_safe": True,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", required=True, choices=CHART_TYPES, help="Zero-install SVG visual type")
    parser.add_argument("--spec", type=Path, required=True, help="JSON input file describing the visual")
    parser.add_argument("--out", type=Path, required=True, help="Output .svg path")
    parser.add_argument("--readme", type=Path, default=None, help="Optional README.md to embed the SVG into")
    parser.add_argument("--slot", default=None, help="Slot id for <!-- md-viz:start:<slot> -->")
    parser.add_argument("--alt", default="", help="Alt text for Markdown image")
    parser.add_argument("--link", default=None, help="Optional hyperlink wrapping the SVG")
    parser.add_argument("--no-append", action="store_true", help="Fail if slot is missing instead of appending")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    meta = generate_chart(args.type, spec, args.out)
    base_dir = args.readme.resolve().parent if args.readme else Path.cwd().resolve()
    rel = Path(os.path.relpath(args.out.resolve(), start=base_dir)).as_posix()
    alt = str(args.alt or spec.get("title") or args.out.stem).replace("\n", " ").replace("]", "\\]").strip()
    snippet = f"![{alt}]({rel})"
    if args.link:
        if args.link.strip().lower().startswith(("javascript:", "data:", "vbscript:")):
            raise ValueError(f"Unsafe link scheme: {args.link!r}")
        snippet = f"[{snippet}]({args.link})"
    meta["markdown"] = snippet
    if args.readme:
        if not args.slot:
            parser.error("--slot is required when --readme is set")
        meta["readme_action"] = update_readme_slot(args.readme.resolve(), args.slot, snippet, append_if_missing=not args.no_append)
        meta["readme"] = str(args.readme.resolve())

    if args.json:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print(snippet)


if __name__ == "__main__":
    main()
