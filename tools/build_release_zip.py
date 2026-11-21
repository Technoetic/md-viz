"""Build a deterministic, UTC-normalized slim plugin ZIP and SHA256SUMS.txt using only the Python stdlib."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "md-viz"
DEFAULT_EPOCH = 1795305600  # 2026-11-22T00:00:00Z


def fixed_zip_time(epoch):
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def normalize_bytes(path):
    raw = path.read_bytes()
    if path.suffix.lower() in {".png", ".gif", ".jpg", ".jpeg", ".webp"}:
        return raw
    return raw.replace(b"\r\n", b"\n")


def collect_plugin_files():
    files = []
    for path in sorted(PLUGIN_DIR.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        rel = path.relative_to(PLUGIN_DIR).as_posix()
        files.append((f"md-viz/{rel}", path))
    return files


def build_zip(version, out_dir, epoch=None):
    clean_ver = version.lstrip("v")
    manifest_ver = json.loads((PLUGIN_DIR / "plugin.json").read_text(encoding="utf-8"))["version"]
    if clean_ver != manifest_ver:
        raise ValueError(f"Version mismatch: requested {clean_ver}, plugin.json has {manifest_ver}")

    ts = fixed_zip_time(int(os.environ.get("SOURCE_DATE_EPOCH", DEFAULT_EPOCH)) if epoch is None else epoch)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"md-viz-plugin-{clean_ver}.zip"
    zip_path = out_dir / zip_name

    entries = collect_plugin_files()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for arcname, src in entries:
            info = zipfile.ZipInfo(filename=arcname, date_time=ts)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix
            info.external_attr = 0o644 << 16
            zf.writestr(info, normalize_bytes(src))

    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sums_path = out_dir / "SHA256SUMS.txt"
    sums_path.write_bytes(f"{digest}  {zip_name}\n".encode("utf-8"))
    return {
        "zip_path": str(zip_path),
        "zip_name": zip_name,
        "bytes": zip_path.stat().st_size,
        "sha256": digest,
        "entries": [arc for arc, _ in entries],
        "sums_path": str(sums_path),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Release version (e.g. v0.3.0 or 0.3.0)")
    parser.add_argument("--out", type=Path, default=ROOT / "dist", help="Output directory")
    parser.add_argument("--epoch", type=int, default=None, help="Optional UTC Unix timestamp override")
    args = parser.parse_args()
    result = build_zip(args.version, args.out, epoch=args.epoch)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
