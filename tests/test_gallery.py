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

    def test_readme_bundles_both_motion_preferences(self):
        readme = (ROOT / "README.md").read_text(encoding="utf8")
        pictures = re.findall(r"<picture>(.*?)</picture>", readme, re.DOTALL)
        self.assertEqual(len(pictures), 2)
        for picture in pictures:
            self.assertIn("prefers-reduced-motion: reduce", picture)
            source, animation = re.findall(r'\bsrc(?:set)?="([^"]+)"', picture)
            self.assertEqual(Path(source).suffix, ".png")
            self.assertEqual(Path(animation).suffix, ".gif")
            for name in (source, animation):
                self.assertTrue((ROOT / name).is_file(), name)
