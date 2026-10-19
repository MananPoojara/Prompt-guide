"""Replay recorded tool decisions offline and independently grade the final answer."""
import hashlib,json,sys
from pathlib import Path
from agent import initial,act
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'evidence-grounding'))
from grounding import grade,expected
out=ROOT/'results/resumed-2026-10-19';state=json.loads((out/'state.json').read_text())
for name,digest in state['hashes'].items():assert hashlib.sha256((out/'frozen'/name).read_bytes()).hexdigest()==digest
s=initial(state['limit']);docs=json.loads((out/'frozen/corpus.json').read_text())
for record in state['history']:
    n=record['call'];assert n==s['calls']+1;s['calls']=n
    request=(out/'frozen/prompt.txt').read_text()+'\nHistory:\n'+json.dumps(s['history'])+'\nCalls remaining including this one: '+str(s['limit']-n+1)
    assert (out/f'{n}.input.txt').read_text()==request
    assert record['status']==0
    assert json.loads((out/f'{n}.output.txt').read_text())==record['decision']
    assert act(s,record['decision'],docs)==record['result']
    s['history'].append(record)
    checkpoint=json.loads((out/f'{n}.checkpoint.json').read_text())
    assert checkpoint['history']==s['history'] and checkpoint['read']==s['read']
assert s['done'] and s['calls']<=s['limit'] and s['read']==state['read']
score=grade(json.dumps(s['history'][-1]['result']['answers']),expected('current_top1'),docs)
assert score['passed']==3 and score['resolved']==3
print(f"Verified {s['calls']} calls, checkpoint replay, and 3/3 final answers")
