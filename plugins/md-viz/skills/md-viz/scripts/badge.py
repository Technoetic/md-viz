"""Draw a two-tone, 28-pixel README badge using only the Python standard library."""
import argparse
import math
from pathlib import Path
import re
import unicodedata
from xml.sax.saxutils import escape

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}")
DEFAULT_LABEL_BG = "#23273a"


def validate_text(value):
    if not isinstance(value, str):
        raise ValueError("Use a non-empty, printable label on a single line.")
    text = value.strip()
    if not text or not text.replace("\u200d", "").isprintable():
        raise ValueError("Use a non-empty, printable label on a single line.")
    return text


def validate_color(value):
    if not isinstance(value, str) or not HEX_COLOR_RE.fullmatch(value):
        raise ValueError("Use a six-digit hex color such as #32C7A2.")
    return value


def text_argument(value):
    try:
        return validate_text(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def color_argument(value):
    try:
        return validate_color(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def text_width(text):
    # East Asian wide glyphs need more room than the tracked Latin capitals.
    cells = sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
                for c in text if unicodedata.category(c) not in ("Mn", "Me", "Cf"))
    return max(8, math.ceil(7.5 * cells))


def ink_color(background):
    background = validate_color(background)
    channels = [int(background[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
              for c in channels]
    luminance = sum(k * c for k, c in zip((0.2126, 0.7152, 0.0722), linear))
    return "#ffffff" if 1.05 / (luminance + 0.05) >= (luminance + 0.05) / 0.05 else "#000000"


def badge_svg(label, value, color, label_bg=DEFAULT_LABEL_BG):
    label = validate_text(label)
    value = validate_text(value)
    color = validate_color(color)
    label_bg = validate_color(label_bg)
    label_width, value_width = text_width(label), text_width(value)
    split = label_width + 20
    width = split + value_width + 20
    label_ink = ink_color(label_bg)
    value_ink = ink_color(color)
    label_esc, value_esc = escape(label), escape(value)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" role="img" aria-labelledby="title">
  <title id="title">{label_esc} · {value_esc}</title>
  <rect width="{split}" height="28" fill="{label_bg}"/>
  <rect x="{split}" width="{width - split}" height="28" fill="{color}"/>
  <g font-family="Verdana, DejaVu Sans, Malgun Gothic, sans-serif" font-size="11" font-weight="700" text-anchor="middle" letter-spacing=".7">
    <text x="{split / 2:g}" y="18" fill="{label_ink}" textLength="{label_width}" lengthAdjust="spacingAndGlyphs">{label_esc}</text>
    <text x="{(split + width) / 2:g}" y="18" fill="{value_ink}" textLength="{value_width}" lengthAdjust="spacingAndGlyphs">{value_esc}</text>
  </g>
</svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("label", type=text_argument)
    parser.add_argument("value", type=text_argument)
    parser.add_argument("output", type=Path)
    parser.add_argument("--color", type=color_argument, default="#32c7a2")
    parser.add_argument("--label-bg", type=color_argument, default=DEFAULT_LABEL_BG)
    args = parser.parse_args()
    svg = badge_svg(args.label, args.value, args.color, label_bg=args.label_bg)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(svg.encode("utf-8"))


if __name__ == "__main__":
    main()
