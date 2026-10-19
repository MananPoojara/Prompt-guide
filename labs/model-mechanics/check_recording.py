"""Verify artifacts and math without downloading or running the model."""
import hashlib
import json
import math
from pathlib import Path
from sampling import probabilities
ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results/recording-2026-10-19'

def main():
    data=json.loads((RUN/'data.json').read_text())
    for name,digest in data['metadata']['sha256'].items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest()==digest,name
    assert len(data['tokenizations'])==7
    for row in data['tokenizations']:
        assert row['text']==row['decoded']
        assert len(row['ids'])==len(row['pieces'])==len(row['vocabulary_pieces'])
    assert len(data['prefixes'])==2
    for row in data['prefixes']:
        candidates=row['first_candidates'];assert len(candidates)==50
        logits=[c['logit'] for c in candidates]
        assert logits==sorted(logits,reverse=True)
        for temperature in [.2,.4,1,1.6,2]:
            p=probabilities(logits,temperature)
            assert math.isclose(sum(p),1,abs_tol=1e-12)
        assert probabilities(logits,.4)[0]>=probabilities(logits,1.6)[0]
        assert {(r['temperature'],r['seed']) for r in row['runs']}=={(0,None),*[(t,s) for t in [.4,1,1.6] for s in [7,23,41]]}
        for run in row['runs']:
            assert 0<len(run['new_ids'])<=20
            assert run['new_ids']==[step['token_id'] for step in run['trace']]
            assert run['text']==row['prefix']+run['continuation']
            assert all(1<=step['candidate_rank']<=50 and 0<=step['probability_within_top_k']<=1 for step in run['trace'])
            if run['temperature']==0:assert all(step['candidate_rank']==1 for step in run['trace'])
    js=(ROOT/'data.js').read_text()
    expected='/* Generated from the retained recording; run build_view.py to refresh. */\nwindow.MODEL_MECHANICS_DATA = '+json.dumps(data,ensure_ascii=False)+';\n'
    assert js==expected
    print('Seven tokenizations, 20 continuations, frozen source hashes, sampling math, and browser data verified.')

if __name__=='__main__':main()
