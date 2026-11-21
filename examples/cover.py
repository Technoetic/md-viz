"""Render the README cover. Requires Pillow, NumPy and system fonts."""
from functools import lru_cache
from pathlib import Path
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ART = Path(__file__).resolve().parents[1] / "docs" / "art"
W, H = 1280, 576
INK = "#101118"
PAPER = "#f7f6ec"
LIME = "#d2ff4c"
PINK = "#f85dce"
FONT_DIR = Path(os.environ.get("WINDIR", "/usr/share")) / "Fonts"


@lru_cache(maxsize=None)
def font(size, family):
    names = {
        "display": ["impact.ttf", "DejaVuSansCondensed-Bold.ttf"],
        "mono": ["consolab.ttf", "DejaVuSansMono-Bold.ttf"],
        "korean": ["malgunbd.ttf", "NotoSansCJK-Bold.ttc"],
    }
    for name in names[family]:
        for target in (FONT_DIR / name, name):
            try:
                return ImageFont.truetype(str(target), size)
            except OSError:
                continue
    raise RuntimeError(f"Install one of the fonts for {family}: {names[family]}")


def base():
    y, x = np.ogrid[:H, :W]
    bloom = np.exp(-((x - 937) / 260) ** 2 - ((y - 270) / 210) ** 2)
    grain = np.random.default_rng(25).normal(0, 1.35, (H, W))
    rgb = np.stack([v + c * bloom + grain for v, c in [(15, 23), (16, 10), (24, 51)]], axis=-1)
    out = Image.fromarray(rgb.clip(0, 255).astype("uint8"))
    draw = ImageDraw.Draw(out)
    for x0 in range(732, 1250, 32):
        for y0 in range(74, 492, 32):
            draw.point((x0, y0), fill="#514464")
    draw.line((46, 59, 1234, 59), fill="#4f5059")
    draw.line((46, 493, 1234, 493), fill="#4f5059")
    draw.polygon([(48, 23), (68, 23), (62, 36), (42, 36)], fill=LIME)
    draw.text((79, 19), "TECHNOETIC   /   MD-VIZ", font=font(20, "mono"), fill=PAPER)
    draw.text((1233, 20), "FIELD RECORDINGS     VOL. 01", font=font(18, "mono"), fill="#d3cfe2", anchor="rt")
    # Two offset inks reference the cyan/magenta registration on concert posters.
    title = font(180, "display")
    for dx, dy, color in [(4, 4, "#ef52bf"), (-3, -2, "#73e6f6"), (0, 0, PAPER)]:
        draw.text((43 + dx, 78 + dy), "MD-VIZ", font=title, fill=color, anchor="lt")
    draw.text((50, 294), "텍스트가 무대에 오르는 순간", font=font(37, "korean"), fill=PAPER)
    draw.text((52, 372), "01—21", font=font(24, "mono"), fill=LIME)
    draw.text((161, 370), "도식 · 차트 · 악보", font=font(22, "korean"), fill=PAPER)
    draw.text((52, 411), "22—25", font=font(24, "mono"), fill=PINK)
    draw.text((161, 409), "코드 · 수식", font=font(22, "korean"), fill=PAPER)
    draw.text((48, 524), "NEON ENCORE", font=font(22, "mono"), fill=LIME, anchor="lt")
    draw.text((245, 525), "가상 공연 기술 노트", font=font(19, "korean"), fill="#c7c5d4", anchor="lt")
    draw.text((1234, 525), "AGY    /    CLAUDE CODE    /    CODEX", font=font(20, "mono"), fill=PAPER, anchor="rt")
    return out


def record(draw, phase):
    major, minor = 136, 30
    u, v = np.meshgrid(np.arange(major + 1) * 2 * np.pi / major,
                       np.arange(minor + 1) * 2 * np.pi / minor, indexing="ij")
    pulse = 1 + .20 * np.sin(5*u + phase) + .09 * np.cos(11*u - phase)
    radius = 143 + 9*np.cos(3*u - phase) + 62*np.cos(v)*pulse
    x, y, z = radius*np.cos(u), radius*np.sin(u), 62*np.sin(v)*pulse + 18*np.sin(3*u + phase)
    a = .98
    y, z = y*np.cos(a) - z*np.sin(a), y*np.sin(a) + z*np.cos(a)
    b = -.55
    x, y = x*np.cos(b) - y*np.sin(b), x*np.sin(b) + y*np.cos(b)
    s = 1.22 + .00063*z
    points = np.stack((956 + s*x, 279 + s*y), axis=-1).round().astype(int).tolist()
    depth = (z[:-1,:-1]+z[1:,:-1]+z[1:,1:]+z[:-1,1:])/4
    # Paint back to front so the central hole and front-facing grooves read at phone size.
    for tile in np.argsort(depth.ravel()):
        i, j = divmod(int(tile), minor)
        pts = [tuple(points[i][j]), tuple(points[i+1][j]),
               tuple(points[i+1][j+1]), tuple(points[i][j+1])]
        angle = 2*math.pi*i/major
        mix = (math.cos(angle-.8)+1)/2
        rgb = np.array([112 + 135*mix, 80 + 167*(1-mix)**1.5, 241 - 150*(1-mix)**2])
        if math.sin(angle + .7) < -.2:
            rgb = np.array([155, 233, 247])*.65 + rgb*.35
        light = .38 + .48*(math.cos(2*math.pi*j/minor - 1.8)+1)/2 + .13*depth[i,j]/200
        color = tuple((rgb*light).clip(0,255).astype(int))
        face = tuple((rgb*(.18 + .22*light)).astype(int))
        draw.polygon(pts, fill=face)
        draw.line((pts[0],pts[3]), fill=color, width=2)
        if j % 3 == 0:
            draw.line((pts[0],pts[1]), fill=tuple((rgb*(light*.77)).astype(int)))
    draw.text((1209, 450), "FIG. A   /   GROOVE", font=font(15, "mono"), fill="#c4bfcd", anchor="rt")


if __name__ == "__main__":
    ART.mkdir(parents=True, exist_ok=True)
    template = base()
    frames = []
    for frame in range(36):
        image = template.copy()
        record(ImageDraw.Draw(image), 2*math.pi*frame/36)
        if frame == 0:
            image.save(ART / "cover.png", optimize=True)
        frames.append(image.resize((960, 432), Image.Resampling.LANCZOS))
    palette = frames[0].quantize(colors=192)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(ART / "cover.gif", save_all=True, append_images=indexed[1:],
                    duration=125, loop=0, optimize=True, disposal=1)
