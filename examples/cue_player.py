"""Animate the same 32 beats as the D3 sequencer in the gallery."""
import json
from pathlib import Path
from PIL import Image, ImageDraw
from cover import ART, PAPER, font


cues = json.loads((Path(__file__).parent / "data" / "show.json").read_text(encoding="utf8"))["cues"]
tracks = [("Wash", "#cdff57"), ("Beam", "#66e6fe"), ("Flash", "#fa77cd")]
beats = len(cues["Wash"])
per_bar = cues["beatsPerBar"]
frames = []
for beat in range(beats):
    img = Image.new("RGB", (1080, 355), "#11131e")
    d = ImageDraw.Draw(img)
    d.text((32, 24), "LIGHT SCORE", font=font(56, "display"), fill=PAPER, anchor="lt")
    d.text((1046, 31), f"BAR  {beat // per_bar + 1:02} / 08", font=font(30, "mono"), fill=PAPER, anchor="rt")
    d.text((1046, 72), "120 BPM   |   4/4", font=font(19, "mono"), fill="#a9b2c5", anchor="rt")
    for n, (name, color) in enumerate(tracks):
        y = 129 + n*52
        d.text((34, y+4), name.upper(), font=font(23, "mono"), fill=color, anchor="lt")
        for step, val in enumerate(cues[name]):
            x = 145 + step*27 + (step // per_bar)*4
            d.rounded_rectangle((x, y, x+21, y+31), radius=3, fill=color if val else "#25293a")
    cursor = 145 + beat*27 + (beat // per_bar)*4
    d.polygon([(cursor, 110), (cursor+21, 110), (cursor+10, 120)], fill=PAPER)
    d.line((cursor+10, 271, cursor+10, 278), fill=PAPER, width=3)
    for b in range(beats//per_bar):
        d.text((145+b*(27*per_bar+4), 282), f"{b+1:02}", font=font(15, "mono"), fill="#b4bdd1", anchor="lt")
    d.text((33, 321), "NEON ENCORE   /   조명 큐", font=font(17, "korean"), fill="#c6ccdb", anchor="lt")
    d.text((1045, 322), f"{beat*60/cues['tempo']:04.1f} s   /   16.0 s", font=font(18, "mono"), fill=PAPER, anchor="rt")
    if beat == 0:
        img.save(ART / "cue-player.png", optimize=True)
    frames.append(img)
frames[0].save(ART / "cue-player.gif", save_all=True, append_images=frames[1:],
               duration=round(60000/cues["tempo"]), loop=0, disposal=1, optimize=True)
