"""Recalculate every saved rank and evidence score without model dependencies."""
import hashlib,json,math
from pathlib import Path
from retrieval import bm25,evaluate
ROOT=Path(__file__).resolve().parent;out=ROOT/'results/pilot-2026-10-19'
data=json.loads((out/'data.json').read_text())
for name,digest in data['metadata']['sha256'].items():assert hashlib.sha256((out/'frozen'/name).read_bytes()).hexdigest()==digest
corpus={d['id']:d for d in json.loads((out/'frozen/corpus.json').read_text())}
assert len(data['queries'])==12 and sum(q['split']=='evaluation' for q in data['queries'])==10
for q in data['queries']:assert corpus[q['document_id']]['text'][q['start']:q['end']]==q['evidence']
assert [c['name'] for c in data['conditions']]==['bm25-48','dense-48','bm25-128','dense-128','dense-254']
for vector in data['query_vectors']:
    assert len(vector)==384 and abs(sum(x*x for x in vector)-1)<1e-5
for c in data['conditions']:
    chunks=c['chunks'];assert len({x['id'] for x in chunks})==len(chunks)
    for x in chunks:assert corpus[x['document_id']]['text'][x['start']:x['end']]==x['text']
    if c['method']=='bm25':scores=[bm25(q['question'],chunks) for q in data['queries']]
    else:
        assert len(c['chunk_vectors'])==len(chunks)
        for v in c['chunk_vectors']:assert len(v)==384 and all(math.isfinite(x) for x in v) and abs(sum(x*x for x in v)-1)<1e-5
        scores=[[sum(x*y for x,y in zip(qv,cv)) for cv in c['chunk_vectors']] for qv in data['query_vectors']]
    fresh=evaluate(data['queries'],chunks,scores)
    for actual,saved in zip(fresh,c['results']):
        for left,right in zip(actual['ranking'],saved['ranking']):
            assert left['chunk_id']==right['chunk_id'] and abs(left['score']-right['score'])<1e-10
        assert {k:v for k,v in actual.items() if k!='ranking'}=={k:v for k,v in saved.items() if k!='ranking'}
print('Verified all five retrieval conditions, vectors, complete rankings, evidence spans, and hashes')
