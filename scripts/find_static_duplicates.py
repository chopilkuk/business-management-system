#!/usr/bin/env python3
"""
Scan all app `static/` folders and report duplicate destination paths
that would collide when running `collectstatic`.

Output: `static_duplicates.json` at project root with mapping of dest -> [sources]

Usage:
  python scripts/find_static_duplicates.py
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
out = {}

for p in ROOT.rglob('static/**'):
    if p.is_file():
        # compute relative path under static/ to use as destination
        try:
            rel = p.relative_to(ROOT / 'static')
        except Exception:
            # find first occurrence of '/static/' in path
            parts = p.parts
            if 'static' in parts:
                idx = parts.index('static')
                rel = Path(*parts[idx+1:])
            else:
                continue
        key = str(rel.as_posix())
        out.setdefault(key, []).append(str(p))

duplicates = {k: v for k, v in out.items() if len(v) > 1}

report_path = ROOT / 'static_duplicates.json'
report_path.write_text(json.dumps({'duplicates': duplicates}, indent=2, ensure_ascii=False))
print(f'Wrote duplicate report: {report_path} ({len(duplicates)} duplicates)')
