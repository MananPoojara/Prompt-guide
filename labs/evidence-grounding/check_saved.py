"""Verify frozen source/input artifacts and retain corrected and original scores."""
import hashlib,importlib.util,json
from pathlib import Path
from grounding import conditions,expected,grade
ROOT=Path(__file__).resolve().parent;RUN=ROOT/'results/pilot-2026-10-19'

def report():
    m=json.loads((RUN/'manifest.json').read_text())
    for name,digest in m['sha256'].items():assert hashlib.sha256((RUN/'frozen'/name).read_bytes()).hexdigest()==digest
    corpus=json.loads((RUN/'frozen/corpus.json').read_text());selected=conditions(corpus)
    questions=json.loads((RUN/'frozen/questions.json').read_text())
    spec=importlib.util.spec_from_file_location('original_grounding',RUN/'frozen/grounding.py')
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    assert len(m['trials'])==10
    expected_order=[f'{r}-{c}' for r in [1,2] for c in (list(selected) if r==1 else list(reversed(selected)))]
    assert [r['trial'] for r in m['trials']]==expected_order
    result={'scoring_amendment':'../../SCORING-AMENDMENT.md','conditions':{},'trials':[]}
    for row in m['trials']:
        name=row['trial'];condition=row['condition']
        request=(RUN/'frozen/prompt.txt').read_text()+'\nQuestions:\n'+json.dumps(questions,indent=2)+'\nDocuments:\n'+json.dumps(selected[condition],indent=2)+'\n'
        assert request==(RUN/(name+'.input.txt')).read_text()
        text=(RUN/(name+'.output.txt')).read_text() if row['status']==0 else ''
        assert original.grade(text,original.expected(condition),selected[condition])==row['score']
        corrected=grade(text,expected(condition),selected[condition])
        result['trials'].append({'trial':name,'original_score':row['score'],'corrected_score':corrected})
        aggregate=result['conditions'].setdefault(condition,{'passed':0,'resolved':0,'total':0,'calls':0,'execution_failures':0})
        for key in ['passed','resolved','total']:aggregate[key]+=corrected[key]
        aggregate['calls']+=1;aggregate['execution_failures']+=row['status']!=0
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    calculated=report();target=RUN/'corrected-scores.json'
    if a.write:target.write_text(json.dumps(calculated,indent=2)+'\n')
    else:assert calculated==json.loads(target.read_text())
    print(json.dumps(calculated['conditions'],indent=2))
