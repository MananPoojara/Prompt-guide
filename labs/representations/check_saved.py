"""Verify archived vectors, attention and browser payload without loading a model."""
import hashlib,json
from pathlib import Path
from metrics import cosine,check_attention
ROOT=Path(__file__).resolve().parent
out=ROOT/'results/recording-2026-10-19';raw=(out/'data.json').read_text();data=json.loads(raw)
for name,digest in data['metadata']['sha256'].items():assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest
assert len(data['inputs'])==2
for x in data['inputs']:
    n=len(x['ids']);assert len(x['pieces'])==n
    assert len(x['attention'])==data['metadata']['layers']
    for layer in x['attention']:
        assert len(layer)==data['metadata']['heads']
        for head in layer:assert len(head)==n;check_attention(head)
    for stage,vectors in x['vectors'].items():
        assert len(vectors)==n and all(len(v)==data['metadata']['dimensions'] for v in vectors)
a,b=data['inputs'];i=a['target_position'];assert i==b['target_position'] and a['ids'][i]==b['ids'][i]
for stage,value in data['target_cosines'].items():assert abs(cosine(a['vectors'][stage][i],b['vectors'][stage][i])-value)<1e-12
assert a['vectors']['token_embedding'][i]==b['vectors']['token_embedding'][i]
assert a['vectors']['input_hidden'][i]==b['vectors']['input_hidden'][i]
assert a['vectors']['final_hidden'][i]!=b['vectors']['final_hidden'][i]
assert (ROOT/'data.js').read_text()=='window.REPRESENTATION_DATA = '+raw.strip()+';\n'
print('Verified two inputs, all 144 attention matrices, vectors, hashes, and browser data')
