import re
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ZERO_INSTALL_TYPES = ("hero", "kpi", "bar", "line", "donut", "heatmap", "waterfall", "radar", "sankey", "timeline")


class GalleryTests(unittest.TestCase):
    def test_all_25_archive_gallery_pieces_have_images_and_descriptions(self):
        for section, expected in (("structure", 9), ("data", 12), ("notation", 4)):
            with self.subTest(section=section):
                chapter = ROOT / "docs" / f"{section}.md"
                images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", chapter.read_text(encoding="utf8"))
                files = {chapter.parent / src for _, src in images}
                self.assertTrue(all(alt.strip() for alt, _ in images))
                self.assertEqual(len(images), expected)
                self.assertEqual(len(files), expected)
                self.assertEqual(files, set((ROOT / "docs/art" / section).glob("*.png")))
                for file in files:
                    with file.open("rb") as stream:
                        self.assertEqual(stream.read(8), b"\x89PNG\r\n\x1a\n")

    def test_bilingual_readmes_showcase_zero_install_suite_and_github_native_layer(self):
        expected_svgs = {f"docs/art/zero-install/{t}.svg" for t in ZERO_INSTALL_TYPES}
        for rel in expected_svgs:
            p = ROOT / rel
            self.assertTrue(p.is_file(), rel)
            root = ET.fromstring(p.read_text(encoding="utf-8"))
            self.assertTrue(root.tag.endswith("svg"))
            for elem in root.iter():
                local = elem.tag.rsplit("}", 1)[-1].lower()
                self.assertNotIn(local, {"script", "foreignobject", "iframe", "embed", "object"})

        for name in ("README.md", "README.ko.md"):
            with self.subTest(readme=name):
                text = (ROOT / name).read_text(encoding="utf8")
                pictures = re.findall(r"<picture>(.*?)</picture>", text, re.DOTALL)
                self.assertGreaterEqual(len(pictures), 2)
                for picture in pictures:
                    self.assertIn("prefers-reduced-motion: reduce", picture)
                    source, animation = re.findall(r'\bsrc(?:set)?="([^"]+)"', picture)
                    self.assertEqual(Path(source).suffix, ".png")
                    self.assertEqual(Path(animation).suffix, ".gif")
                    for asset in (source, animation):
                        self.assertTrue((ROOT / asset).is_file(), asset)
                embedded_svgs = set(re.findall(r"docs/art/zero-install/[a-z0-9-]+\.svg", text))
                self.assertEqual(embedded_svgs, expected_svgs)
                self.assertIn("docs/art/zero-install/cue-loop.gif", text)
                self.assertIn("docs/art/zero-install/cue-loop.png", text)
                self.assertIn("```mermaid", text)
                self.assertIn("```geojson", text)
                self.assertIn("$$", text)
                self.assertIn("<kbd>", text)
                self.assertIn("<details open>", text)
