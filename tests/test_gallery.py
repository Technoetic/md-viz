import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GalleryTests(unittest.TestCase):
    def test_all_25_gallery_pieces_have_images_and_descriptions(self):
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

    def test_bilingual_readmes_showcase_all_25_engines_and_live_boosters(self):
        expected_pngs = {
            p.relative_to(ROOT).as_posix()
            for section in ("structure", "data", "notation")
            for p in (ROOT / "docs/art" / section).glob("*.png")
        }
        self.assertEqual(len(expected_pngs), 25)
        for name in ("README.md", "README.ko.md"):
            with self.subTest(readme=name):
                text = (ROOT / name).read_text(encoding="utf8")
                pictures = re.findall(r"<picture>(.*?)</picture>", text, re.DOTALL)
                self.assertEqual(len(pictures), 2)
                for picture in pictures:
                    self.assertIn("prefers-reduced-motion: reduce", picture)
                    source, animation = re.findall(r'\bsrc(?:set)?="([^"]+)"', picture)
                    self.assertEqual(Path(source).suffix, ".png")
                    self.assertEqual(Path(animation).suffix, ".gif")
                    for asset in (source, animation):
                        self.assertTrue((ROOT / asset).is_file(), asset)
                embedded = set(re.findall(r"docs/art/(?:structure|data|notation)/[a-z0-9-]+\.png", text))
                self.assertEqual(embedded, expected_pngs)
                self.assertIn("```mermaid", text)
                self.assertIn("```geojson", text)
                self.assertIn("$$", text)
                self.assertIn("<kbd>", text)
                self.assertIn("<details open>", text)
