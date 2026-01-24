#!/usr/bin/env python3
"""Validate that image links referenced in Markdown files exist on disk.
Scans README.md and all files in reports/ for pattern ![...](path) and checks file existence relative to repo root.
Exits with code 0 if all OK, non-zero otherwise.
"""
import re
from pathlib import Path
import sys

repo_root = Path(__file__).resolve().parents[1]
md_files = [repo_root / "README.md"] + sorted((repo_root / "reports").glob("*.md"))
pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

errors = []
for md in md_files:
    text = md.read_text(encoding="utf8")
    for m in pattern.finditer(text):
        path = m.group(1)
        # ignore absolute URLs
        if path.startswith("http://") or path.startswith("https://"):
            continue
        # resolve relative to the markdown file location
        candidate = (md.parent / path).resolve()
        if not candidate.exists():
            errors.append(f"Missing: {path} referenced in {md}")

if errors:
    print("Found missing image links:")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("All image links exist.")
    sys.exit(0)
