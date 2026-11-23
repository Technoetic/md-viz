import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECK_ENV = ROOT / "plugins/md-viz/skills/md-viz/scripts/check_env.py"


class CheckEnvTests(unittest.TestCase):
    def test_json_output_reports_zero_install_stack_and_25_engines_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(CHECK_ENV), "--cwd", td, "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertTrue(data["zero_install_ready"])
            self.assertEqual(data["summary"]["zero_install_generators_ready"], 4)
            self.assertEqual(data["summary"]["zero_install_generators_total"], 4)
            self.assertEqual(data["summary"]["github_native_libraries"], 2)
            self.assertEqual(data["summary"]["github_prerender_libraries"], 23)
            self.assertEqual(data["summary"]["total"], 25)
            self.assertEqual(len(data["engines"]), 25)
            self.assertEqual(
                data["summary"]["ready"] + data["summary"]["partial"] + data["summary"]["missing"],
                25,
            )
            native_names = {e["name"] for e in data["engines"] if e["github_native"]}
            self.assertEqual(native_names, {"Mermaid", "MathJax"})
            categories = {e["category"] for e in data["engines"]}
            self.assertEqual(categories, {"structure", "data", "notation"})
            # Strictly read-only: temp directory remains empty.
            self.assertEqual(list(Path(td).iterdir()), [])

    def test_markdown_output_handles_cp1252_and_lists_bundled_generators(self):
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "cp1252"
        proc = subprocess.run(
            [sys.executable, str(CHECK_ENV), "--cwd", str(ROOT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=True,
        )
        self.assertIn("`svg_chart.py`", proc.stdout)
        self.assertIn("`gif_anim.py`", proc.stdout)
        self.assertIn("`tree_gen.py`", proc.stdout)
        self.assertIn("| Status | Engine | Category | Detected | Notes |", proc.stdout)
        self.assertIn("**Mermaid**", proc.stdout)
        self.assertIn("**MathJax**", proc.stdout)
        self.assertIn("**KaTeX**", proc.stdout)
