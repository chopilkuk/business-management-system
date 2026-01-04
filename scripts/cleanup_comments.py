"""
cleanup_comments.py

도움말:
- 저장소의 파이썬 파일을 검사하여 연속된 주석 블록(3줄 이상)을 "드라이런"으로 보고합니다.
- --apply 플래그를 주면 원본 파일을 `.bak`로 백업한 뒤 제거를 수행합니다n
주의: 모든 주석을 제거하지 않습니다. `# TODO`, `# FIXME`, 그리고 모듈/함수 설명(도큐스트링)은 유지합니다.
"""

import re
import argparse
from pathlib import Path

IGNORED_COMMENT_MARKERS = ("# TODO", "# FIXME", "# NOTE")

COMMENT_BLOCK_RE = re.compile(r"(?:^[ \t]*#.*\n){3,}", re.MULTILINE)


def is_ignored_block(block: str) -> bool:
    for m in IGNORED_COMMENT_MARKERS:
        if m in block:
            return True
    return False


def scan_file(p: Path):
    text = p.read_text(encoding='utf-8')
    blocks = []
    for m in COMMENT_BLOCK_RE.finditer(text):
        block = m.group(0)
        if is_ignored_block(block):
            continue
        # skip if block looks like commented code with "def " or "class " within
        if re.search(r"\b(def|class)\b", block):
            continue
        blocks.append((m.start(), m.end(), block))
    return blocks


def apply_strip(p: Path, blocks):
    text = p.read_text(encoding='utf-8')
    new_text = ''
    last = 0
    for s,e,block in blocks:
        new_text += text[last:s]
        last = e
    new_text += text[last:]
    bak = p.with_suffix(p.suffix + '.bak')
    p.rename(bak)
    bak.write_text(text, encoding='utf-8')
    p.write_text(new_text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--root', default='.', help='검색 루트')
    args = parser.parse_args()

    root = Path(args.root)
    pyfiles = list(root.rglob('*.py'))
    report = []
    for p in pyfiles:
        # skip venv or migrations
        if 'venv' in p.parts or 'migrations' in p.parts:
            continue
        blocks = scan_file(p)
        if blocks:
            report.append((p, blocks))
    for p,blocks in report:
        print(f"{p}: {len(blocks)} candidate blocks")
        for i,(s,e,block) in enumerate(blocks,1):
            print('---')
            print(block[:1000])
            print('---')
    print(f"Scanned {len(pyfiles)} .py files, {len(report)} files with candidates")
    if args.apply and report:
        for p,blocks in report:
            apply_strip(p, blocks)
        print('Applied changes and backed up original files with .bak suffix')

if __name__ == '__main__':
    main()
