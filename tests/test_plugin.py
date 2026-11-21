"""Check that all native plugin catalogs resolve the same packaged skill."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def manifest(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PluginPackagingTests(unittest.TestCase):
    def test_catalogs_reference_one_native_plugin(self):
        claude = manifest(ROOT / ".claude-plugin/marketplace.json")
        codex = manifest(ROOT / ".agents/plugins/marketplace.json")
        self.assertEqual(claude["name"], codex["name"])
        claude_entry, = claude["plugins"]
        codex_entry, = codex["plugins"]
        self.assertEqual(codex_entry["source"]["source"], "local")
        package = (ROOT / claude_entry["source"]).resolve()
        self.assertEqual(package, (ROOT / codex_entry["source"]["path"]).resolve())
        self.assertIn(ROOT, package.parents)
        hosts = [
            manifest(package / ".claude-plugin/plugin.json"),
            manifest(package / ".codex-plugin/plugin.json"),
            manifest(package / "plugin.json"),
        ]
        for host in hosts:
            self.assertEqual(host["name"], "md-viz")
            self.assertEqual(host["name"], claude_entry["name"])
            self.assertEqual(host["name"], codex_entry["name"])
            self.assertEqual(host["version"], claude_entry["version"])

        standard = package / "skills"
        self.assertEqual((package / hosts[1]["skills"]).resolve(), standard)
        skill, = standard.glob("*/SKILL.md")
        header = skill.read_text(encoding="utf-8").split("---", 2)[1].splitlines()
        self.assertEqual(skill.parent.name, "md-viz")
        self.assertIn("name: md-viz", header)

    def test_skill_references_are_available_after_plugin_installation(self):
        package = ROOT / "plugins/md-viz"
        skill = package / "skills/md-viz/SKILL.md"
        links = re.findall(r"\]\(([^)\s]+)\)", skill.read_text(encoding="utf-8"))
        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            with self.subTest(link=link):
                reference = (skill.parent / unquote(url.path)).resolve()
                self.assertIn(package, reference.parents)
                self.assertTrue(reference.is_file(), reference)


if __name__ == "__main__":
    unittest.main()
