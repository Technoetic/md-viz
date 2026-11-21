import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "plugins/md-viz/skills/md-viz/scripts/badge.py"
EXAMPLES_BADGES = ROOT / "examples/badges.py"


def load_badge_module():
    spec = importlib.util.spec_from_file_location("md_viz_badge", GENERATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class BadgeGeneratorTests(unittest.TestCase):
    def test_cli_renders_user_text_and_selects_contrasting_ink(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "assets" / "badge.svg"
            for color, ink in (("#152038", "#ffffff"), ("#F7DC61", "#000000")):
                with self.subTest(color=color):
                    subprocess.run(
                        [sys.executable, str(GENERATOR), "도구 & 예제", "<25>", str(output), "--color", color],
                        check=True,
                    )
                    svg = ET.parse(output).getroot()
                    self.assertEqual(svg.get("height"), "28")
                    self.assertEqual(svg.find("{*}title").text, "도구 & 예제 · <25>")
                    rectangles = svg.findall("{*}rect")
                    self.assertEqual(sum(int(r.get("width")) for r in rectangles), int(svg.get("width")))
                    self.assertEqual(rectangles[1].get("fill"), color)
                    labels = svg.findall(".//{*}text")
                    self.assertEqual([label.text for label in labels], ["도구 & 예제", "<25>"])
                    self.assertEqual(labels[1].get("fill"), ink)

    def test_cli_rejects_injection_invalid_colors_and_bad_text(self):
        bad_cases = [
            ("color_injection", ["label", "val", "--color", '#ff0000" onload="alert(1)']),
            ("short_hex", ["label", "val", "--color", "#f0a"]),
            ("word_color", ["label", "val", "--color", "red"]),
            ("empty_label", ["", "val", "--color", "#32C7A2"]),
            ("empty_value", ["label", "", "--color", "#32C7A2"]),
            ("whitespace_label", ["   ", "val", "--color", "#32C7A2"]),
            ("multiline_label", ["a\nb", "val", "--color", "#32C7A2"]),
            ("bad_label_bg", ["label", "val", "--color", "#32C7A2", "--label-bg", "bad"]),
        ]
        with tempfile.TemporaryDirectory() as directory:
            for name, args in bad_cases:
                with self.subTest(case=name):
                    out = Path(directory) / f"{name}.svg"
                    proc = subprocess.run(
                        [sys.executable, str(GENERATOR), args[0], args[1], str(out), *args[2:]],
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(proc.returncode, 0)
                    self.assertFalse(out.exists())

    def test_python_api_validates_inputs_directly(self):
        badge = load_badge_module()
        with self.assertRaises(ValueError):
            badge.badge_svg("ok", "val", '#ff0000" onload="alert(1)')
        with self.assertRaises(ValueError):
            badge.badge_svg("ok", "val", "#32C7A2", label_bg="not-hex")
        with self.assertRaises(ValueError):
            badge.badge_svg("line1\nline2", "val", "#32C7A2")
        svg = badge.badge_svg("👨‍👩‍👧 가족", "<script>alert(1)</script>", "#00F5D4")
        self.assertNotIn("<script>", svg)
        ET.fromstring(svg)

    def test_examples_badges_script_matches_committed_svgs(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            shutil.copytree(ROOT / "plugins/md-viz", work / "plugins/md-viz")
            (work / "examples/data").mkdir(parents=True)
            shutil.copy2(EXAMPLES_BADGES, work / "examples/badges.py")
            shutil.copy2(ROOT / "examples/data/show.json", work / "examples/data/show.json")
            (work / "docs/art/elements").mkdir(parents=True)
            subprocess.run([sys.executable, str(work / "examples/badges.py")], cwd=work, check=True)
            generated = sorted(p.name for p in (work / "docs/art/elements").glob("*.svg"))
            committed = sorted(p.name for p in (ROOT / "docs/art/elements").glob("*.svg"))
            self.assertEqual(generated, committed)
            for name in committed:
                with self.subTest(svg=name):
                    gen_bytes = (work / "docs/art/elements" / name).read_bytes()
                    orig_bytes = (ROOT / "docs/art/elements" / name).read_bytes().replace(b"\r\n", b"\n")
                    self.assertEqual(gen_bytes, orig_bytes)
