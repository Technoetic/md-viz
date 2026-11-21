"""Check that all native plugin catalogs, licenses, icons, hygiene, and links stay valid."""
import json
from pathlib import Path
import re
import struct
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
INVISIBLE_CHARS = {
    "\ufeff", "\u200b", "\u200c", "\u200e", "\u200f", "\u00ad", "\u034f",
    "\u061c", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e", "\u2066",
    "\u2067", "\u2068", "\u2069", "\u3164", "\uffa0",
}
TEXT_EXTS = {".md", ".py", ".json", ".geojson", ".svg", ".yml", ".yaml", ".js", ".mjs", ".R", ".txt", ".html"}


def manifest(path):
    return json.loads(path.read_text(encoding="utf-8"))


class PluginPackagingTests(unittest.TestCase):
    def test_catalogs_reference_one_native_plugin_with_license_and_icon(self):
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
            self.assertEqual(host.get("license"), "MIT")

        root_license = ROOT / "LICENSE"
        plugin_license = package / "LICENSE"
        self.assertTrue(root_license.is_file())
        self.assertTrue(plugin_license.is_file())
        self.assertEqual(
            root_license.read_bytes().replace(b"\r\n", b"\n"),
            plugin_license.read_bytes().replace(b"\r\n", b"\n"),
        )
        self.assertTrue((package / "README.md").is_file())
        self.assertTrue((ROOT / "SECURITY.md").is_file())

        icon = package / ".claude-plugin/icon.png"
        self.assertTrue(icon.is_file())
        self.assertLess(icon.stat().st_size, 2 * 1024 * 1024)
        header = icon.read_bytes()[:24]
        self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", header[16:24])
        self.assertEqual(width, height)
        self.assertGreaterEqual(width, 512)
        self.assertLessEqual(width, 2048)

        standard = package / "skills"
        self.assertEqual((package / hosts[1]["skills"]).resolve(), standard)
        skill, = standard.glob("*/SKILL.md")
        header_lines = skill.read_text(encoding="utf-8").split("---", 2)[1].splitlines()
        self.assertEqual(skill.parent.name, "md-viz")
        self.assertIn("name: md-viz", header_lines)

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

    def test_readmes_local_links_exist(self):
        fence_re = re.compile(r"^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[ \t]*$", re.MULTILINE | re.DOTALL)
        for doc_name in ("README.md", "README.ko.md"):
            doc = ROOT / doc_name
            visible = fence_re.sub("", doc.read_text(encoding="utf-8"))
            refs = re.findall(r"\]\(([^)\s]+)\)", visible)
            refs.extend(re.findall(r'''\b(?:src|srcset|href)=["']([^"']+)["']''', visible))
            for ref in refs:
                url = urlsplit(ref)
                if url.scheme or url.netloc or not url.path:
                    continue
                with self.subTest(doc=doc_name, ref=ref):
                    self.assertTrue((ROOT / unquote(url.path)).exists(), ref)

    def test_repo_text_files_have_no_bom_or_invisible_unicode(self):
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if ".git" in path.parts or "node_modules" in path.parts or "dist" in path.parts:
                continue
            if path.suffix not in TEXT_EXTS and path.name != "LICENSE":
                continue
            raw = path.read_bytes()
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM detected")
                text = raw.decode("utf-8")
                bad = [hex(ord(c)) for c in text if c in INVISIBLE_CHARS]
                self.assertEqual(bad, [], f"Invisible chars in {path}: {bad}")


if __name__ == "__main__":
    unittest.main()
