import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


GENERATOR = Path(__file__).resolve().parents[1] / "plugins/md-viz/skills/md-viz/scripts/badge.py"


class BadgeGeneratorTests(unittest.TestCase):
    def test_cli_renders_user_text_and_selects_contrasting_ink(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "assets" / "badge.svg"
            for color, ink in (("#152038", "#ffffff"), ("#F7DC61", "#000000")):
                with self.subTest(color=color):
                    subprocess.run([sys.executable, str(GENERATOR), "도구 & 예제", "<25>",
                                    str(output), "--color", color], check=True)
                    svg = ET.parse(output).getroot()
                    self.assertEqual(svg.get("height"), "28")
                    self.assertEqual(svg.find("{*}title").text, "도구 & 예제 · <25>")
                    rectangles = svg.findall("{*}rect")
                    self.assertEqual(sum(int(r.get("width")) for r in rectangles), int(svg.get("width")))
                    self.assertEqual(rectangles[1].get("fill"), color)
                    labels = svg.findall(".//{*}text")
                    self.assertEqual([label.text for label in labels], ["도구 & 예제", "<25>"])
                    self.assertEqual(labels[1].get("fill"), ink)
