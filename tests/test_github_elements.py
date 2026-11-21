"""Check the files and rendered examples in the GitHub Markdown chapter and bilingual READMEs."""
import json
import re
import struct
import unicodedata
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "docs/github-elements.md"
SHOW = ROOT / "examples/data/show.json"
# Match the whole outer fence so a copyable example inside it stays inert.
FENCE = re.compile(
    r"^ {0,3}(?P<marker>`{3,}|~{3,})[ \t]*(?P<info>[^\n]*)\n"
    r"(?P<body>.*?)^ {0,3}(?P=marker)[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


class GitHubElementsTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHAPTER.is_file(), "The GitHub elements chapter is missing")
        self.document = CHAPTER.read_text(encoding="utf-8")
        self.visible = FENCE.sub("", self.document)
        self.fences = list(FENCE.finditer(self.document))

    def test_readme_and_visible_examples_link_to_existing_files(self):
        for readme_name in ("README.md", "README.ko.md"):
            readme = (ROOT / readme_name).read_text(encoding="utf-8")
            self.assertRegex(FENCE.sub("", readme), r"docs/github-elements\.md")
        references = re.findall(r"\]\(([^)\s]+)\)", self.visible)
        references.extend(re.findall(r'''\b(?:src|srcset|href)=["']([^"']+)["']''', self.visible))
        for reference in references:
            with self.subTest(reference=reference):
                url = urlsplit(reference)
                if url.scheme or url.netloc or not url.path:
                    continue
                self.assertTrue((CHAPTER.parent / unquote(url.path)).exists(), reference)

    def test_rendered_geojson_and_download_follow_the_shuttle_stops(self):
        stops = json.loads(SHOW.read_text(encoding="utf-8"))["shuttle"]
        coordinates = [[stop["lon"], stop["lat"]] for stop in stops]
        canonical = json.loads((ROOT / "docs/art/elements/shuttle.geojson").read_text(encoding="utf-8"))
        for doc_path in (CHAPTER, ROOT / "README.md", ROOT / "README.ko.md"):
            with self.subTest(document=doc_path.name):
                fences = list(FENCE.finditer(doc_path.read_text(encoding="utf-8")))
                embeds = [m["body"] for m in fences if m["info"].strip() == "geojson"]
                self.assertEqual(len(embeds), 1, f"Expected one live geojson fence in {doc_path.name}")
                route = json.loads(embeds[0])
                self.assertEqual(route, canonical)
                self.assertEqual(route["type"], "FeatureCollection")
                geometries = [feature["geometry"] for feature in route["features"]]
                self.assertTrue(all(feature["type"] == "Feature" for feature in route["features"]))
                self.assertCountEqual([g["coordinates"] for g in geometries if g["type"] == "Point"], coordinates)
                self.assertEqual([g["coordinates"] for g in geometries if g["type"] == "LineString"], [coordinates])

    def test_each_github_alert_has_visible_quoted_content(self):
        for path in (CHAPTER, ROOT / "README.md", ROOT / "README.ko.md"):
            with self.subTest(document=path.name):
                visible = FENCE.sub("", path.read_text(encoding="utf-8"))
                alerts = re.findall(r"(?:\A|\n[ \t]*\n)> \[!(\w+)\][ \t]*\n>[ \t]+\S", visible)
                self.assertEqual(set(alerts), {"NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"})

    def test_tempo_badge_uses_the_show_tempo(self):
        badges = re.findall(r"\[!\[([^\]]+)\]\(([^)\s]+\.svg)\)\]\(([^)\s]+)\)", self.visible)
        badges = [(alt, path) for alt, path, source in badges if (CHAPTER.parent / source).resolve() == SHOW]
        self.assertTrue(badges, "Expected an SVG badge with alt text linked to the show data")
        tempo = json.loads(SHOW.read_text(encoding="utf-8"))["cues"]["tempo"]
        alt, link = badges[0]
        badge = ET.parse(CHAPTER.parent / link).getroot()
        self.assertEqual(badge.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertRegex(alt, rf"\b{tempo}\b")
        caption = " ".join("".join(node.itertext()) for node in badge.findall(".//{*}text"))
        self.assertRegex(caption, rf"\b{tempo}\b")

    def test_emoji_instructions_pair_icons_with_readable_labels(self):
        emoji = r"(?:[\U0001F300-\U0001FAFF\u2600-\u27BF]\ufe0f?|:[a-z][a-z0-9_+-]+:)"
        symbols = set(re.findall(emoji, self.visible))
        self.assertTrue(symbols, "Expected a live emoji example")
        for symbol in symbols:
            with self.subTest(symbol=symbol):
                self.assertRegex(self.visible, re.escape(symbol) + r"\s+[*_]*\w")

    def test_directory_trees_show_paths_and_aligned_roles(self):
        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_ko = (ROOT / "README.ko.md").read_text(encoding="utf-8")
        copy_examples = "\n".join(m["body"] for m in self.fences if m["info"].strip() == "markdown")
        for example, source, directory, root_label, role_pattern in (
            ("README.md", readme_en, ROOT, "md-viz/", r"[A-Za-z]{3,}"),
            ("README.ko.md", readme_ko, ROOT, "md-viz/", r"[가-힣]"),
            ("chapter", self.document, CHAPTER.parent, "docs/", r"[가-힣]"),
            ("copy example", copy_examples, CHAPTER.parent, "docs/", r"[가-힣]"),
        ):
            with self.subTest(example=example):
                trees = [
                    m["body"] for m in FENCE.finditer(source)
                    if m["info"].strip() == "text" and "└── " in m["body"]
                ]
                self.assertTrue(trees, "Expected a fenced text tree")
                for tree in trees:
                    self.assert_annotated_tree(tree, directory, root_label, role_pattern)

    def assert_annotated_tree(self, tree, directory, root_label, role_pattern):
        for guide in ("├── ", "│   ", "└── "):
            self.assertIn(guide, tree)
        self.assertNotIn("\t", tree)
        arrow_columns = set()
        names = []
        for row in tree.splitlines():
            left, arrow, role = row.partition("← ")
            self.assertTrue(arrow and left.endswith("  "), row)
            self.assertRegex(role, role_pattern, row)
            arrow_columns.add(sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in left))
            names.append(left.rstrip())
        self.assertEqual(len(arrow_columns), 1, f"Align the role arrows in one display column: {arrow_columns}")
        root, *entries = names
        self.assertEqual(root, root_label)
        parents = [directory]
        for entry in entries:
            branch = re.fullmatch(r"((?:│   |    )*)[├└]── (.+)", entry)
            self.assertIsNotNone(branch, entry)
            depth = len(branch[1]) // 4
            self.assertLess(depth, len(parents), entry)
            path = parents[depth] / branch[2]
            self.assertTrue(path.is_dir() if branch[2].endswith("/") else path.is_file(), path)
            parents[depth + 1:] = [path]

    def test_cue_animation_and_reduced_motion_still_have_the_same_dimensions(self):
        picture = re.search(r"<picture\b[^>]*>(.*?)</picture>", self.visible, re.DOTALL)
        self.assertIsNotNone(picture, "Expected the live animation and its reduced-motion alternative")
        source = re.search(r"<source\b[^>]*>", picture[1])[0]
        self.assertIn("prefers-reduced-motion: reduce", source)
        still = re.search(r'''\bsrcset=["']([^"']+)["']''', source)[1]
        animation = re.search(r'''<img\b[^>]*?\bsrc=["']([^"']+)["']''', picture[1])[1]
        with (CHAPTER.parent / still).open("rb") as stream:
            header = stream.read(24)
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
            png_size = struct.unpack(">II", header[16:24])
        with (CHAPTER.parent / animation).open("rb") as stream:
            header = stream.read(10)
            self.assertIn(header[:6], (b"GIF87a", b"GIF89a"))
            gif_size = struct.unpack("<HH", header[6:10])
        self.assertEqual(png_size, gif_size)
        self.assertTrue(all(gif_size))
