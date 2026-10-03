"""Maintain the Markdown inventory in index.md while preserving manual content."""
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- document-index:start -->'
END = '<!-- document-index:end -->'
EXCLUDED = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'tmp'}


def main():
    index = ROOT / 'index.md'
    original = index.read_text(encoding='utf-8')
    documents = sorted(
        (p for p in ROOT.rglob('*.md')
         if not EXCLUDED.intersection(p.relative_to(ROOT).parts)),
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )
    lines = [START, '## 자동 문서 목록', '',
             f'Markdown 총 {len(documents)}개. 이 목록은 `Tools/sync_document_index.py`로 갱신한다.', '']
    group = None
    for path in documents:
        relative = path.relative_to(ROOT)
        current = relative.parent.as_posix()
        if current != group:
            group = current
            lines.extend([f'### {"루트" if group == "." else group}', ''])
        title = next((line[2:].strip() for line in path.read_text(encoding='utf-8').splitlines()
                      if line.startswith('# ')), path.stem)
        title = title.replace('[', r'\[').replace(']', r'\]')
        target = relative.as_posix()
        for character, encoded in [('%', '%25'), (' ', '%20'), ('(', '%28'), (')', '%29'), ('#', '%23')]:
            target = target.replace(character, encoded)
        lines.append(f'- [{title}]({target})')
    lines.extend(['', END])
    block = '\n'.join(lines)
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1 or original.index(START) > original.index(END):
            raise ValueError('Invalid document inventory markers')
        updated = original[:original.index(START)] + block + original[original.index(END) + len(END):]
    else:
        updated = original.rstrip() + '\n\n' + block + '\n'
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', updated):
        if target.startswith(('https:', 'http:', 'mailto:', '#')):
            continue
        local_path = unquote(target.split('#')[0])
        if not (ROOT / local_path).exists():
            raise FileNotFoundError(f'Broken index link: {target}')
    if updated != original:
        index.write_text(updated, encoding='utf-8')
    print(f'Indexed {len(documents)} Markdown documents; index file links verified.')


if __name__ == '__main__':
    main()
