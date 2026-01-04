#!/usr/bin/env python3
"""
Simple helper to consolidate per-app `static/menu/` assets into project `static/menu/`.

Usage:
  python scripts/organize_static.py

It will copy files (not remove) and print a short report. Intended as a developer convenience only.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'static' / 'menu'
DEST.mkdir(parents=True, exist_ok=True)

copied = 0
skipped = 0
for p in ROOT.rglob('static/menu/*'):
    if p.is_file():
        dest = DEST / p.name
        if dest.exists():
            skipped += 1
            continue
        shutil.copy2(p, dest)
        copied += 1

print(f'Copied: {copied}, Skipped(existing): {skipped}, Destination: {DEST}')
