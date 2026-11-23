import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_release_zip.py"
VERSION = json.loads((ROOT / "plugins/md-viz/plugin.json").read_text(encoding="utf-8"))["version"]


class ReleaseZipTests(unittest.TestCase):
    def test_deterministic_slim_plugin_zip_across_timezones(self):
        hashes = {}
        with tempfile.TemporaryDirectory() as td:
            for tz in ("UTC0", "KST-9", "EST5"):
                out_dir = Path(td) / tz
                env = os.environ.copy()
                env["TZ"] = tz
                env["SOURCE_DATE_EPOCH"] = "1795305600"
                proc = subprocess.run(
                    [sys.executable, str(BUILDER), "--version", f"v{VERSION}", "--out", str(out_dir)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    env=env,
                    check=True,
                )
                meta = json.loads(proc.stdout)
                zip_path = Path(meta["zip_path"])
                sums_path = Path(meta["sums_path"])
                self.assertTrue(zip_path.is_file())
                self.assertTrue(sums_path.is_file())
                digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
                self.assertEqual(digest, meta["sha256"])
                self.assertEqual(sums_path.read_text(encoding="utf-8"), f"{digest}  {zip_path.name}\n")
                self.assertLess(zip_path.stat().st_size, 512 * 1024)
                hashes[tz] = digest

                with zipfile.ZipFile(zip_path) as zf:
                    names = set(zf.namelist())
                    for required in (
                        "md-viz/LICENSE",
                        "md-viz/README.md",
                        "md-viz/plugin.json",
                        "md-viz/.claude-plugin/plugin.json",
                        "md-viz/.claude-plugin/icon.png",
                        "md-viz/.codex-plugin/plugin.json",
                        "md-viz/skills/md-viz/SKILL.md",
                        "md-viz/skills/md-viz/agents/openai.yaml",
                        "md-viz/skills/md-viz/references/markdown-patterns.md",
                        "md-viz/skills/md-viz/scripts/badge.py",
                        "md-viz/skills/md-viz/scripts/svg_chart.py",
                        "md-viz/skills/md-viz/scripts/gif_anim.py",
                        "md-viz/skills/md-viz/scripts/tree_gen.py",
                        "md-viz/skills/md-viz/scripts/check_env.py",
                    ):
                        self.assertIn(required, names)

        self.assertEqual(len(set(hashes.values())), 1, hashes)
