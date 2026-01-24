#!/usr/bin/env python3
import pathlib

repo = pathlib.Path('.')
reports = repo / 'reports'
out = repo / 'tmp_sanitized'
out.mkdir(exist_ok=True)
replacements = [
    ('CO₂', 'CO$_2$'),
    ('≈', '~'),
    ('⸻', '---'),
    ('../outputs/figures', 'outputs/figures'),
]
for f in sorted(reports.glob('*.md')):
    txt = f.read_text(encoding='utf-8')
    # remove leading ```markdown if present
    if txt.startswith('```markdown'):
        # remove the initial fence and any following newline
        txt = txt.split('\n', 1)[1] if '\n' in txt else ''
    # remove trailing ``` if present
    if txt.rstrip().endswith('```'):
        # remove the last fence
        txt = txt.rstrip()
        if txt.endswith('```'):
            txt = txt[: -3].rstrip() + '\n'
    for a, b in replacements:
        txt = txt.replace(a, b)
    # Replace standalone YAML-style horizontal rules '---' with asterisks '***'
    # to avoid Pandoc interpreting them as YAML front-matter in some cases.
    lines = []
    for line in txt.splitlines():
        if line.strip() == '---':
            lines.append('***')
        else:
            lines.append(line)
    txt = '\n'.join(lines) + '\n'
    out_f = out / f.name
    out_f.write_text(txt, encoding='utf-8')
    print(f"Sanitized {f} -> {out_f}")
print('Done')
