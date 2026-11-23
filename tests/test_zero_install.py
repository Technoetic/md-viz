"""Tests for zero-install Python stdlib generators: svg_chart.py, gif_anim.py, tree_gen.py, and showcase determinism."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unicodedata
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins/md-viz/skills/md-viz/scripts"
SVG_CHART = SCRIPTS / "svg_chart.py"
GIF_ANIM = SCRIPTS / "gif_anim.py"
TREE_GEN = SCRIPTS / "tree_gen.py"
SHOWCASE = ROOT / "examples/zero_install_showcase.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ZeroInstallGeneratorTests(unittest.TestCase):
    def test_all_10_svg_chart_types_render_github_safe_svg_and_escape_xml(self):
        showcase = load_module("zero_install_showcase", SHOWCASE)
        specs = showcase.build_specs()
        self.assertEqual(set(specs.keys()), {
            "hero", "kpi", "bar", "line", "donut", "heatmap", "waterfall", "radar", "sankey", "timeline",
        })
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            readme = td_path / "README.md"
            readme.write_text("# Demo\n", encoding="utf-8")

            for chart_type, spec in specs.items():
                spec_copy = json.loads(json.dumps(spec))
                spec_copy["title"] = f"{chart_type} <A & B>"
                spec_file = td_path / f"{chart_type}.json"
                out_file = td_path / "art" / f"{chart_type}.svg"
                spec_file.write_text(json.dumps(spec_copy, ensure_ascii=False), encoding="utf-8")
                proc = subprocess.run(
                    [
                        sys.executable, str(SVG_CHART),
                        "--type", chart_type,
                        "--spec", str(spec_file),
                        "--out", str(out_file),
                        "--readme", str(readme),
                        "--slot", f"slot-{chart_type}",
                        "--json",
                    ],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=True,
                )
                meta = json.loads(proc.stdout)
                self.assertTrue(meta["github_img_safe"])
                self.assertEqual(meta["readme_action"], "appended")
                svg_text = out_file.read_text(encoding="utf-8")
                root = ET.fromstring(svg_text)
                self.assertTrue(root.tag.endswith("svg"))
                self.assertIn("<A & B>", root.find("{*}title").text)
                for elem in root.iter():
                    local = elem.tag.rsplit("}", 1)[-1].lower()
                    self.assertNotIn(local, {"script", "foreignobject", "iframe", "embed", "object"})

            # Re-running the same slot must replace idempotently rather than duplicate.
            proc2 = subprocess.run(
                [
                    sys.executable, str(SVG_CHART),
                    "--type", "kpi",
                    "--spec", str(td_path / "kpi.json"),
                    "--out", str(td_path / "art/kpi.svg"),
                    "--readme", str(readme),
                    "--slot", "slot-kpi",
                    "--json",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            self.assertEqual(json.loads(proc2.stdout)["readme_action"], "replaced")
            readme_text = readme.read_text(encoding="utf-8")
            self.assertEqual(readme_text.count("<!-- md-viz:start:slot-kpi -->"), 1)
            self.assertIn("](art/kpi.svg)", readme_text)

    def test_svg_chart_rejects_invalid_hex_and_bad_slot(self):
        svg_mod = load_module("svg_chart_mod", SVG_CHART)
        with self.assertRaises(ValueError):
            svg_mod.validate_hex('#00ff00" onload="alert(1)')
        with self.assertRaises(ValueError):
            svg_mod.update_readme_slot(Path("README.md"), "../escape", "![x](y.svg)")
        with self.assertRaises(ValueError):
            svg_mod.verify_github_safe_svg('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
        with self.assertRaises(ValueError):
            svg_mod.verify_github_safe_svg('<svg xmlns="http://www.w3.org/2000/svg"><foreignObject/></svg>')

    def test_gif_anim_pure_stdlib_generates_valid_gif89a_and_matching_png_picture(self):
        showcase = load_module("zero_install_showcase_gif", SHOWCASE)
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            spec_file = td_path / "loop.json"
            spec_file.write_text(json.dumps(showcase.build_gif_spec()), encoding="utf-8")
            out_gif = td_path / "docs/art/loop.gif"
            readme = td_path / "README.md"
            readme.write_text("# Demo\n", encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable, str(GIF_ANIM),
                    "--spec", str(spec_file),
                    "--out", str(out_gif),
                    "--readme", str(readme),
                    "--slot", "loop",
                    "--alt", "Stdlib cue loop",
                    "--json",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            meta = json.loads(proc.stdout)
            gif_bytes = out_gif.read_bytes()
            png_bytes = out_gif.with_suffix(".png").read_bytes()
            self.assertEqual(gif_bytes[:6], b"GIF89a")
            self.assertIn(b"NETSCAPE2.0", gif_bytes[:128])
            self.assertEqual(gif_bytes[-1:], b"\x3b")
            self.assertEqual(png_bytes[:8], b"\x89PNG\r\n\x1a\n")
            gw, gh = struct.unpack("<HH", gif_bytes[6:10])
            pw, ph = struct.unpack(">II", png_bytes[16:24])
            self.assertEqual((gw, gh), (pw, ph))
            self.assertEqual((gw, gh), (meta["width"], meta["height"]))
            self.assertEqual(meta["frames"], 16)
            self.assertIn("prefers-reduced-motion: reduce", meta["markdown"])
            self.assertIn('srcset="docs/art/loop.png"', meta["markdown"])
            self.assertIn('src="docs/art/loop.gif"', meta["markdown"])

    def test_tree_gen_scans_real_filesystem_and_aligns_east_asian_arrows(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "demo-repo"
            (root / "src").mkdir(parents=True)
            (root / "docs").mkdir()
            (root / "node_modules/ignored").mkdir(parents=True)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "src/app.py").write_text("print(1)\n", encoding="utf-8")
            (root / "docs/안내.md").write_text("# 안내\n", encoding="utf-8")
            roles_file = Path(td) / "roles.json"
            roles_file.write_text(json.dumps({
                ".": "저장소 루트",
                "docs/안내.md": "한국어 가이드",
            }, ensure_ascii=False), encoding="utf-8")

            proc = subprocess.run(
                [sys.executable, str(TREE_GEN), "--root", str(root), "--max-depth", "3", "--roles", str(roles_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            body = proc.stdout.strip().removeprefix("```text\n").removesuffix("\n```")
            self.assertNotIn("node_modules", body)
            self.assertIn("안내.md", body)
            arrow_cols = set()
            for row in body.splitlines():
                left, arrow, role = row.partition("← ")
                self.assertTrue(arrow and left.endswith("  "), row)
                self.assertTrue(role.strip(), row)
                arrow_cols.add(sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in left))
            self.assertEqual(len(arrow_cols), 1, arrow_cols)

    def test_committed_zero_install_showcase_matches_generator_output(self):
        showcase = load_module("zero_install_showcase_det", SHOWCASE)
        svg_mod = load_module("svg_chart_det", SVG_CHART)
        gif_mod = load_module("gif_anim_det", GIF_ANIM)
        committed_dir = ROOT / "docs/art/zero-install"
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            for chart_type, spec in showcase.build_specs().items():
                out = td_path / f"{chart_type}.svg"
                svg_mod.generate_chart(chart_type, spec, out)
                self.assertEqual(
                    out.read_bytes().replace(b"\r\n", b"\n"),
                    (committed_dir / f"{chart_type}.svg").read_bytes().replace(b"\r\n", b"\n"),
                    f"Committed {chart_type}.svg is out of sync with examples/zero_install_showcase.py",
                )
            gif_out = td_path / "cue-loop.gif"
            gif_mod.generate_gif_pair(showcase.build_gif_spec(), gif_out)
            self.assertEqual(gif_out.read_bytes(), (committed_dir / "cue-loop.gif").read_bytes())
            self.assertEqual(
                gif_out.with_suffix(".png").read_bytes(),
                (committed_dir / "cue-loop.png").read_bytes(),
            )
