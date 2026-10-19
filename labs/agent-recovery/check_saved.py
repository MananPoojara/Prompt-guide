"""Replay fault injection and model choices; separately regrade final answers."""
import argparse,hashlib,json,sys
from pathlib import Path
from agent import initial
from recovery import dispatch
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'evidence-grounding'))
from grounding import expected,grade
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();reports=[]
for condition in ['transient','denied']:
    out=ROOT/f'results/{condition}-2026-10-19';state=json.loads((out/'state.json').read_text())
    for name,digest in state['hashes'].items():assert hashlib.sha256((out/'frozen'/name).read_bytes()).hexdigest()==digest
    docs=json.loads((out/'frozen/corpus.json').read_text());s=initial(6);s['condition']=condition;s['fault_used']=False
    for item in state['history']:
        n=item['call'];assert n==s['calls']+1;s['calls']=n
        request=(out/'frozen/prompt.txt').read_text()+'\nHistory:\n'+json.dumps(s['history'])+'\nCalls remaining including this one: '+str(s['limit']-n+1)
        assert (out/f'{n}.input.txt').read_text()==request
        assert item['status']==0 and json.loads((out/f'{n}.output.txt').read_text())==item['decision']
        assert dispatch(s,item['decision'],docs,condition)==item['result'];s['history'].append(item)
        checkpoint=json.loads((out/f'{n}.checkpoint.json').read_text())
        assert checkpoint['history']==s['history'] and checkpoint['read']==s['read'] and checkpoint['fault_used']==s['fault_used']
    assert s['calls']<=6 and s['done']==state['done'] and s['read']==state['read']
    final=s['history'][-1]['result'].get('answers',[])
    score=grade(json.dumps(final),expected('current_top1' if condition=='transient' else 'no_evidence'),docs)
    reports.append({'condition':condition,'calls':s['calls'],'completed':s['done'],'read_documents':s['read'],'tool_errors':[r['result']['error'] for r in s['history'] if 'error' in r['result']],'score':score})
report={'grounding_sha256':hashlib.sha256((ROOT.parent/'evidence-grounding/grounding.py').read_bytes()).hexdigest(),'runs':reports}
path=ROOT/'results/scores.json'
if args.write:path.write_text(json.dumps(report,indent=2)+'\n')
else:assert json.loads(path.read_text())==report
print(json.dumps(report,indent=2))
