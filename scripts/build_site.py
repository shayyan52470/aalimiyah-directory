#!/usr/bin/env python3
"""Assemble the small static GitHub Pages artifact."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "_site"

if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir()

for name in ("index.html", "data.html", "submit.html", "methodology.html", "404.html", ".nojekyll"):
    shutil.copy2(ROOT / name, DEST / name)
for name in ("assets", "data"):
    shutil.copytree(ROOT / name, DEST / name)

print(f"Built static site in {DEST}")

