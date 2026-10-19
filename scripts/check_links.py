"""Check repository-local Markdown link targets, not external URLs or anchors."""
from pathlib import Path
import re
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
# Frozen evidence keeps its original bytes and original link base. Do not rewrite
# historical artifacts just because their archive location differs.
SNAPSHOT_BASES = {
    "labs/skill-execution/results/run-2026-10-19/frozen/plugin/README.md":
        root / "examples/claude-plugin",
}
errors = []
for source in root.rglob('*.md'):
    if '.git' in source.parts:
        continue
    for target in re.findall(r'\]\(([^\s)]+)\)', source.read_text()):
        if '://' in target or target.startswith(('#', 'mailto:')):
            continue
        path = unquote(target.split('#')[0])
        base = SNAPSHOT_BASES.get(source.relative_to(root).as_posix(), source.parent)
        if path and not (base / path).exists():
            errors.append(f'{source.relative_to(root)}: {target}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('All local Markdown link targets exist.')
