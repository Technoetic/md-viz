"""Zero-install pure-Python-stdlib animated GIF89a + identical-dimension reduced-motion PNG generator for GitHub README.md."""
import argparse
import html
import json
import os
from pathlib import Path
import re
import struct
import sys
import zlib

SLOT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

# Fixed 16-color NEON ENCORE palette (4-bit indexed color for compact GIF89a & PNG PLTE)
PALETTE_HEX = (
    "#0B0F1A",  # 0: obsidian background
    "#131621",  # 1: panel dark
    "#1E293B",  # 2: inactive cell
    "#27304A",  # 3: border / grid
    "#475569",  # 4: muted rail
    "#F8FAFC",  # 5: bright white playhead / highlight
    "#00F5D4",  # 6: electric cyan
    "#FF2E93",  # 7: hot magenta
    "#C8FF00",  # 8: acid lime
    "#FFBB54",  # 9: solar amber
    "#C084FC",  # 10: ultraviolet
    "#38BDF8",  # 11: sky neon
    "#FF3864",  # 12: crimson pulse
    "#0E4A4B",  # 13: dim cyan glow
    "#571238",  # 14: dim magenta glow
    "#3B4D07",  # 15: dim lime glow
)

COLOR_INDEX = {h.upper(): i for i, h in enumerate(PALETTE_HEX)}
ACCENT_INDICES = (6, 7, 8, 9, 10, 11, 12)
DIM_FOR_ACCENT = {6: 13, 7: 14, 8: 15, 9: 3, 10: 3, 11: 13, 12: 14}


def hex_to_rgb(h):
    return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))


PALETTE_RGB = tuple(hex_to_rgb(h) for h in PALETTE_HEX)


def nearest_palette_index(hex_color, fallback=6):
    if not hex_color:
        return fallback
    val = str(hex_color).upper()
    if not HEX_RE.fullmatch(val):
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    if val in COLOR_INDEX:
        return COLOR_INDEX[val]
    r, g, b = hex_to_rgb(val)
    best_i, best_d = fallback, 10**9
    for idx in ACCENT_INDICES:
        pr, pg, pb = PALETTE_RGB[idx]
        d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d < best_d:
            best_i, best_d = idx, d
    return best_i


def fill_rect(buf, width, height, x0, y0, x1, y1, color_idx):
    x0 = max(0, min(width, int(x0)))
    x1 = max(0, min(width, int(x1)))
    y0 = max(0, min(height, int(y0)))
    y1 = max(0, min(height, int(y1)))
    if x1 <= x0 or y1 <= y0:
        return
    span = bytes([color_idx]) * (x1 - x0)
    for y in range(y0, y1):
        row = y * width
        buf[row + x0 : row + x1] = span


def stroke_rect(buf, width, height, x0, y0, x1, y1, color_idx, thickness=2):
    fill_rect(buf, width, height, x0, y0, x1, y0 + thickness, color_idx)
    fill_rect(buf, width, height, x0, y1 - thickness, x1, y1, color_idx)
    fill_rect(buf, width, height, x0, y0, x0 + thickness, y1, color_idx)
    fill_rect(buf, width, height, x1 - thickness, y0, x1, y1, color_idx)


def lzw_encode_gif(pixels, min_code_size=4):
    """Spec-compliant GIF89a variable-width LSB-first LZW encoder (Python stdlib only)."""
    clear_code = 1 << min_code_size
    eoi_code = clear_code + 1
    next_code = eoi_code + 1
    code_size = min_code_size + 1
    max_code_for_size = 1 << code_size

    out = bytearray()
    bit_buf = 0
    bit_cnt = 0

    def emit(code):
        nonlocal bit_buf, bit_cnt
        bit_buf |= code << bit_cnt
        bit_cnt += code_size
        while bit_cnt >= 8:
            out.append(bit_buf & 0xFF)
            bit_buf >>= 8
            bit_cnt -= 8

    emit(clear_code)
    table = {}
    prefix = pixels[0]
    for k in pixels[1:]:
        key = (prefix << 8) | k
        found = table.get(key)
        if found is not None:
            prefix = found
        else:
            emit(prefix)
            if next_code < 4096:
                table[key] = next_code
                next_code += 1
                if next_code > max_code_for_size and code_size < 12:
                    code_size += 1
                    max_code_for_size = 1 << code_size
            else:
                emit(clear_code)
                table.clear()
                next_code = eoi_code + 1
                code_size = min_code_size + 1
                max_code_for_size = 1 << code_size
            prefix = k

    emit(prefix)
    emit(eoi_code)
    if bit_cnt > 0:
        out.append(bit_buf & 0xFF)
    return bytes(out)


def encode_gif89a(frames, width, height, delay_cs=26):
    """Encode indexed 16-color frames into a looping GIF89a byte stream."""
    out = bytearray()
    out.extend(b"GIF89a")
    # Logical Screen Descriptor: 16-color Global Color Table (GCT flag=1, res=7, size=3 -> 0xF3)
    out.extend(struct.pack("<HHBBB", width, height, 0xF3, 0, 0))
    for r, g, b in PALETTE_RGB:
        out.extend((r, g, b))
    # Netscape 2.0 infinite loop Application Extension
    out.extend(b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00")

    for pixels in frames:
        # Graphic Control Extension (disposal=1 keep, delay in centiseconds)
        out.extend(struct.pack("<BBBBHB", 0x21, 0xF9, 4, 0x04, delay_cs, 0))
        out.append(0x00)
        # Image Descriptor
        out.extend(struct.pack("<BHHHHB", 0x2C, 0, 0, width, height, 0))
        # LZW Minimum Code Size = 4
        out.append(4)
        compressed = lzw_encode_gif(pixels, min_code_size=4)
        for i in range(0, len(compressed), 255):
            chunk = compressed[i : i + 255]
            out.append(len(chunk))
            out.extend(chunk)
        out.append(0x00)  # block terminator
    out.append(0x3B)  # GIF trailer
    return bytes(out)


def _png_chunk(tag, payload):
    crc = zlib.crc32(tag + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)


def encode_indexed_png(pixels, width, height):
    """Encode an indexed 16-color frame as a standard 8-bit paletted PNG (stdlib zlib only)."""
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)
    plte = b"".join(struct.pack("BBB", *rgb) for rgb in PALETTE_RGB)
    raw_rows = bytearray()
    for y in range(height):
        raw_rows.append(0)  # filter type 0 (None)
        row = y * width
        raw_rows.extend(pixels[row : row + width])
    idat = zlib.compress(bytes(raw_rows), level=9)
    return b"".join((
        b"\x89PNG\r\n\x1a\n",
        _png_chunk(b"IHDR", ihdr),
        _png_chunk(b"PLTE", plte),
        _png_chunk(b"IDAT", idat),
        _png_chunk(b"IEND", b""),
    ))


def build_sequencer_frames(spec):
    width = int(spec.get("width", 760))
    height = int(spec.get("height", 196))
    steps = max(4, min(32, int(spec.get("steps", 16))))
    tracks = spec.get("tracks") or [
        {"label": "NATIVE", "color": "#00F5D4", "active": [0, 1, 2, 3, 8, 9, 10, 11]},
        {"label": "SVG", "color": "#FF2E93", "active": [2, 3, 4, 5, 6, 10, 11, 12, 13]},
        {"label": "GIF", "color": "#C8FF00", "active": [5, 6, 7, 12, 13, 14, 15]},
    ]
    if width < 240 or height < 96:
        raise ValueError("Minimum animation size is 240x96")

    pad_x = 24
    pad_top = 34
    pad_bot = 26
    gap_x = 6
    gap_y = 10
    n_tracks = len(tracks)
    cell_w = max(10, (width - pad_x * 2 - gap_x * (steps - 1)) // steps)
    row_h = max(18, (height - pad_top - pad_bot - gap_y * (n_tracks - 1)) // n_tracks)
    total_grid_w = steps * cell_w + (steps - 1) * gap_x
    start_x = (width - total_grid_w) // 2

    parsed_tracks = []
    for idx, tr in enumerate(tracks):
        c_idx = nearest_palette_index(tr.get("color"), ACCENT_INDICES[idx % len(ACCENT_INDICES)])
        parsed_tracks.append((c_idx, DIM_FOR_ACCENT.get(c_idx, 3), set(tr.get("active", []))))

    frames = []
    for head in range(steps):
        buf = bytearray(width * height)
        # Outer border + neon top bar + progress rail
        stroke_rect(buf, width, height, 0, 0, width, height, 3, thickness=2)
        fill_rect(buf, width, height, 2, 2, width - 2, 7, 6)
        # Step indicator dots along top bar
        for s in range(steps):
            cx0 = start_x + s * (cell_w + gap_x)
            dot_c = 5 if s == head else (6 if s < head else 3)
            fill_rect(buf, width, height, cx0, 16, cx0 + cell_w, 22, dot_c)

        # Sequencer cells
        for r_idx, (on_c, dim_c, active) in enumerate(parsed_tracks):
            y0 = pad_top + r_idx * (row_h + gap_y)
            y1 = y0 + row_h
            for s in range(steps):
                x0 = start_x + s * (cell_w + gap_x)
                x1 = x0 + cell_w
                is_on = s in active
                is_head = s == head
                if is_on and is_head:
                    fill_rect(buf, width, height, x0, y0, x1, y1, 5)
                    stroke_rect(buf, width, height, x0, y0, x1, y1, on_c, thickness=3)
                elif is_on:
                    fill_rect(buf, width, height, x0, y0, x1, y1, on_c)
                elif is_head:
                    fill_rect(buf, width, height, x0, y0, x1, y1, dim_c)
                    stroke_rect(buf, width, height, x0, y0, x1, y1, 5, thickness=2)
                else:
                    fill_rect(buf, width, height, x0, y0, x1, y1, 2)
                    stroke_rect(buf, width, height, x0, y0, x1, y1, 3, thickness=1)

        # Vertical playhead hairline at bottom rail
        hx = start_x + head * (cell_w + gap_x) + cell_w // 2
        fill_rect(buf, width, height, start_x, height - 14, start_x + total_grid_w, height - 10, 3)
        fill_rect(buf, width, height, start_x, height - 14, hx + 2, height - 10, 8)
        fill_rect(buf, width, height, hx - 2, height - 17, hx + 3, height - 7, 5)
        frames.append(bytes(buf))
    return frames, width, height


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


def generate_gif_pair(spec, out_gif):
    frames, width, height = build_sequencer_frames(spec)
    delay_ms = int(spec.get("duration_ms", 240))
    delay_cs = max(4, round(delay_ms / 10))
    gif_bytes = encode_gif89a(frames, width, height, delay_cs=delay_cs)
    png_bytes = encode_indexed_png(frames[0], width, height)

    gif_path = Path(out_gif)
    if gif_path.suffix.lower() != ".gif":
        raise ValueError("Output path must end with .gif")
    png_path = gif_path.with_suffix(".png")
    gif_path.parent.mkdir(parents=True, exist_ok=True)
    gif_path.write_bytes(gif_bytes)
    png_path.write_bytes(png_bytes)

    return {
        "gif_path": str(gif_path.resolve()),
        "png_path": str(png_path.resolve()),
        "width": width,
        "height": height,
        "frames": len(frames),
        "gif_bytes": len(gif_bytes),
        "png_bytes": len(png_bytes),
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True, help="JSON input file describing tracks & steps")
    parser.add_argument("--out", type=Path, required=True, help="Output .gif path (companion .png written alongside)")
    parser.add_argument("--readme", type=Path, default=None, help="Optional README.md to embed <picture> into")
    parser.add_argument("--slot", default=None, help="Slot id for <!-- md-viz:start:<slot> -->")
    parser.add_argument("--alt", default="", help="Accessible alt text")
    parser.add_argument("--no-append", action="store_true", help="Fail if slot is missing instead of appending")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    meta = generate_gif_pair(spec, args.out)
    base_dir = args.readme.resolve().parent if args.readme else Path.cwd().resolve()
    rel_gif = Path(os.path.relpath(Path(meta["gif_path"]), start=base_dir)).as_posix()
    rel_png = Path(os.path.relpath(Path(meta["png_path"]), start=base_dir)).as_posix()
    alt = str(args.alt or spec.get("title") or args.out.stem).replace("\n", " ").strip()
    snippet = (
        "<picture>\n"
        f'  <source media="(prefers-reduced-motion: reduce)" srcset="{rel_png}">\n'
        f'  <img src="{rel_gif}" width="{meta["width"]}" alt="{html.escape(alt, quote=True)}">\n'
        "</picture>"
    )
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
