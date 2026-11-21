"""Build the visual index from the actual gallery outputs."""
from PIL import Image, ImageDraw, ImageOps
from cover import ART, LIME, PINK, PAPER, font


groups = [
    ("structure", LIME, [
        ("cue-gate", "Mermaid"), ("standby", "PlantUML"), ("signal-path", "Graphviz"),
        ("patch-bays", "D2"), ("cue-desk", "Structurizr"), ("set-notes", "markmap"),
        ("stage-plot", "Excalidraw"), ("count-in", "WaveDrom"), ("encore", "abcjs"),
    ]),
    ("data", "#77eafc", [
        ("vega-lite", "Vega-Lite"), ("matplotlib", "Matplotlib"), ("seaborn", "seaborn"),
        ("altair", "Altair"), ("ggplot2", "ggplot2"), ("chartjs", "Chart.js"),
        ("observable", "Observable Plot"), ("plotly", "Plotly"), ("echarts", "Apache ECharts"),
        ("d3", "D3"), ("cytoscape", "Cytoscape.js"), ("leaflet", "Leaflet"),
    ]),
    ("notation", PINK, [
        ("shiki", "Shiki"), ("highlight", "highlight.js"), ("mathjax", "MathJax"), ("katex", "KaTeX"),
    ]),
]
poster = Image.new("RGB", (1576, 1256), "#101118")
draw = ImageDraw.Draw(poster)
draw.text((34, 32), "THE VISUAL SETLIST", font=font(59, "display"), fill=PAPER, anchor="lt")
draw.text((1542, 49), "NEON ENCORE   /   25 CUTS", font=font(25, "mono"), fill=LIME, anchor="rt")
count = 0
for series, accent, engines in groups:
    for key, engine in engines:
        x = 34 + (count % 5)*304
        y = 139 + (count // 5)*220
        image = Image.open(ART / series / (key + ".png")).convert("RGB")
        w, h = image.size
        # All source cards have a title and caption. Index only the illustration.
        if series == "structure":
            image = image.crop((int(.03*w), 143, int(.97*w), h - 85))
        elif series == "data":
            image = image.crop((int(.03*w), int(.25*h), int(.97*w), int(.865*h)))
        else:
            image = image.crop((40, 133, w - 40, h - 42))
        draw.rectangle((x, y, x+289, y+191), fill="#1a1c29", outline="#44445a")
        thumb = ImageOps.pad(image, (286, 142), method=Image.Resampling.LANCZOS, color="#151927")
        poster.paste(thumb, (x+2, y+2))
        draw.line((x+2, y+145, x+287, y+145), fill=accent, width=2)
        draw.text((x+9, y+159), f"{count+1:02}", font=font(18, "mono"), fill=accent, anchor="lt")
        draw.text((x+52, y+157), engine, font=font(23, "mono"), fill=PAPER, anchor="lt")
        count += 1
assert count == 25
poster.save(ART / "contact-sheet.png", optimize=True)
