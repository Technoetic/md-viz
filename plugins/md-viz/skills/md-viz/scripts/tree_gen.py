"""Zero-install real-repository column-aligned annotated directory tree generator for GitHub README.md."""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

DEFAULT_EXCLUDES = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", ".pytest_cache", ".mypy_cache"}
SLOT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def display_width(text):
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in text)


def default_role(path, is_dir):
    name = path.name.lower()
    if is_dir:
        known_dirs = {
            ".github": "GitHub automation & workflows",
            "workflows": "GitHub Actions CI definitions",
            "docs": "Documentation & visual assets",
            "src": "Core application source",
            "tests": "Automated test suite",
            "scripts": "Utility & build scripts",
            "plugins": "Installable plugin packages",
            "skills": "Reusable agent skills",
            "examples": "Reproducible usage examples",
            "tools": "Release & maintenance tools",
            "assets": "Static images & visual assets",
        }
        return known_dirs.get(name, f"{path.name} directory")
    known_files = {
        "readme.md": "Primary repository guide",
        "readme.ko.md": "Korean documentation parity",
        "license": "Open-source license",
        "security.md": "Security policy & boundaries",
        "skill.md": "Agent skill instructions",
        "plugin.json": "Plugin manifest",
        "package.json": "Node package manifest",
        "pyproject.toml": "Python project configuration",
    }
    return known_files.get(name, f"{path.suffix.lstrip('.').upper() or 'Project'} file")


def build_tree_rows(root, max_depth=3, roles=None, excludes=None):
    root = Path(root).resolve()
    role_map = roles or {}
    skip = set(DEFAULT_EXCLUDES) | set(excludes or ())

    rows = [(f"{root.name}/", role_map.get(".", role_map.get(f"{root.name}/", "Repository root")))]

    def walk(directory, prefix, depth):
        if depth > max_depth:
            return
        entries = [
            p for p in directory.iterdir()
            if p.name not in skip and not p.name.endswith(".pyc")
        ]
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
        for idx, entry in enumerate(entries):
            is_last = idx == len(entries) - 1
            branch = "└── " if is_last else "├── "
            is_dir = entry.is_dir()
            rel = entry.relative_to(root).as_posix() + ("/" if is_dir else "")
            label = f"{prefix}{branch}{entry.name}{'/' if is_dir else ''}"
            role = role_map.get(rel) or role_map.get(rel.rstrip("/")) or default_role(entry, is_dir)
            rows.append((label, role))
            if is_dir and depth < max_depth:
                walk(entry, prefix + ("    " if is_last else "│   "), depth + 1)

    walk(root, "", 1)
    return rows


def format_annotated_tree(rows):
    max_w = max(display_width(left) for left, _ in rows)
    col = max_w + 2
    lines = []
    for left, role in rows:
        pad = " " * (col - display_width(left))
        lines.append(f"{left}{pad}← {role}")
    return "\n".join(lines)


def render_tree_fence(root, max_depth=3, roles=None, excludes=None):
    rows = build_tree_rows(root, max_depth=max_depth, roles=roles, excludes=excludes)
    body = format_annotated_tree(rows)
    return f"```text\n{body}\n```", len(rows)


def update_readme_slot(readme_path, slot, snippet, append_if_missing=True):
    if not SLOT_RE.fullmatch(slot):
        raise ValueError(f"Invalid slot name {slot!r}")
    path = Path(readme_path)
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    start = f"<!-- md-viz:start:{slot} -->"
    end = f"<!-- md-viz:end:{slot} -->"
    block = f"{start}\n{snippet}\n{end}"
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pat.search(text):
        path.write_text(pat.sub(lambda _: block, text, count=1), encoding="utf-8")
        return "replaced"
    if not append_if_missing:
        raise ValueError(f"Slot {slot!r} not found in {path}")
    sep = "" if not text else ("\n\n" if not text.endswith("\n") else ("\n" if not text.endswith("\n\n") else ""))
    path.write_text(f"{text}{sep}{block}\n", encoding="utf-8")
    return "appended"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Target repository directory to inspect")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum directory depth (default: 3)")
    parser.add_argument("--roles", type=Path, default=None, help="Optional JSON file mapping relative paths to role descriptions")
    parser.add_argument("--exclude", action="append", default=[], help="Extra directory/file names to exclude")
    parser.add_argument("--readme", type=Path, default=None, help="Optional README.md to embed the tree into")
    parser.add_argument("--slot", default=None, help="Slot id for <!-- md-viz:start:<slot> -->")
    parser.add_argument("--no-append", action="store_true", help="Fail if slot is missing instead of appending")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    args = parser.parse_args()

    roles = json.loads(args.roles.read_text(encoding="utf-8")) if args.roles else {}
    fence, count = render_tree_fence(args.root, max_depth=args.max_depth, roles=roles, excludes=args.exclude)
    meta = {"root": str(args.root.resolve()), "entries": count, "markdown": fence}
    if args.readme:
        if not args.slot:
            parser.error("--slot is required when --readme is set")
        meta["readme_action"] = update_readme_slot(args.readme.resolve(), args.slot, fence, append_if_missing=not args.no_append)
        meta["readme"] = str(args.readme.resolve())

    if args.json:
        print(json.dumps(meta, ensure_ascii=False, indent=2))
    else:
        print(fence)


if __name__ == "__main__":
    main()
