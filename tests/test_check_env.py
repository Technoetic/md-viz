import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECK_ENV = ROOT / "plugins/md-viz/skills/md-viz/scripts/check_env.py"


class CheckEnvTests(unittest.TestCase):
    def test_json_output_reports_all_25_engines_without_side_effects(self):
        with tempfile.TemporaryDirectory() as td:
            proc = subprocess.run(
                [sys.executable, str(CHECK_ENV), "--cwd", td, "--json"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            data = json.loads(proc.stdout)
            self.assertEqual(data["summary"]["total"], 25)
            self.assertEqual(len(data["engines"]), 25)
            self.assertEqual(
                data["summary"]["ready"] + data["summary"]["partial"] + data["summary"]["missing"],
                25,
            )
            categories = {e["category"] for e in data["engines"]}
            self.assertEqual(categories, {"structure", "data", "notation"})
            # Strictly read-only: temp directory remains empty.
            self.assertEqual(list(Path(td).iterdir()), [])

    def test_markdown_output_contains_table_and_mermaid_ready(self):
        proc = subprocess.run(
            [sys.executable, str(CHECK_ENV), "--cwd", str(ROOT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        self.assertIn("| Status | Engine | Category | Detected | Notes |", proc.stdout)
        self.assertIn("**Mermaid**", proc.stdout)
        self.assertIn("**KaTeX**", proc.stdout)
