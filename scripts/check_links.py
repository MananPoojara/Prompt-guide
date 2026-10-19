"""Check repository-local Markdown link targets, not external URLs or anchors."""
from pathlib import Path
import re
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
errors = []
for source in root.rglob('*.md'):
    if '.git' in source.parts:
        continue
    for target in re.findall(r'\]\(([^\s)]+)\)', source.read_text()):
        if '://' in target or target.startswith(('#', 'mailto:')):
            continue
        path = unquote(target.split('#')[0])
        if path and not (source.parent / path).exists():
            errors.append(f'{source.relative_to(root)}: {target}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('All local Markdown link targets exist.')
