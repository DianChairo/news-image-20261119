#!/usr/bin/env python3
"""Entrypoint: place the rendered front page where make.fun expects it.

Copies ``entry.png`` (rendered by build_image.py, sitting next to this file)
into the output directory given by the ``MAKEFUN_OUTPUT_DIR`` environment
variable, defaulting to ``/output``. The copy is byte-for-byte and its size
is checked against the source before the script exits successfully.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def here() -> Path:
    return Path(__file__).resolve().parent


def output_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path("/output")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_front_page(source: Path, destination: Path) -> int:
    """Copy the PNG, verify size and hash, and return bytes written."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    written = destination.stat().st_size
    expected = source.stat().st_size
    if written != expected:
        raise RuntimeError(
            "copy incomplete: wrote %d bytes, source has %d" % (written, expected)
        )
    if sha256_of(destination) != sha256_of(source):
        raise RuntimeError("copy failed integrity check: hash mismatch")
    return written


def main() -> int:
    source = here() / "entry.png"
    if not source.is_file():
        print("entry.png not found next to main.py; run build_image.py first",
              file=sys.stderr)
        return 1
    destination = output_dir() / "entry.png"
    size = copy_front_page(source, destination)
    print("copied %s (%d bytes) -> %s" % (source.name, size, destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
