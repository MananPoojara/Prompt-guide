"""Verify saved upstream prompt bytes and notebook extraction without a network."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
entries=json.loads((ROOT/'originals/manifest.json').read_text())
for entry in entries:
    data=(ROOT/entry['local_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==entry['sha256'], entry['id']+' changed'
    assert (ROOT/entry['license_path']).is_file(), entry['id']+' missing license'
    assert len(entry['commit'])==40 and entry['commit'] in entry['source_url']
notebook=json.loads((ROOT/'originals/vendor/anthropic-cookbook/evaluator_optimizer.ipynb').read_text())
values={node.targets[0].id:node.value.value for node in ast.parse(''.join(notebook['cells'][3]['source'])).body if isinstance(node,ast.Assign) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str)}
for name in ['generator_prompt','evaluator_prompt']:
    assert (ROOT/'originals/vendor/anthropic-cookbook'/f'{name}.txt').read_bytes()==values[name].encode()
print(f'{len(entries)} original prompt artifacts match their hashes; both notebook extractions match.')
