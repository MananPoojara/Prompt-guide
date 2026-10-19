"""Standard-library scoring and immutable, bounded Codex trials."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
ARMS = ('short', 'rules', 'examples')

def score(text, cases):
    result = {'schema_valid': False, 'passed': 0, 'total': len(cases), 'exact': False, 'cases': []}
    def unique_object(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj: raise ValueError("duplicate JSON key")
            obj[key] = value
        return obj
    try:
        actual = json.loads(text, object_pairs_hook=unique_object)
    except (ValueError, TypeError):
        actual = None
    valid = isinstance(actual, list) and len(actual) == len(cases)
    if valid:
        for row, case in zip(actual, cases):
            if (not isinstance(row, dict) or set(row) != {'id', 'owner', 'deadline'}
                    or row['id'] != case['id']
                    or any(row[k] is not None and not isinstance(row[k], str) for k in ('owner','deadline'))):
                valid = False
                break
            if row['deadline'] is not None:
                try:
                    valid = date.fromisoformat(row['deadline']).isoformat() == row['deadline']
                except ValueError:
                    valid = False
                if not valid: break
    result['schema_valid'] = valid
    for index, case in enumerate(cases):
        wrong = [k for k in ('owner','deadline') if not valid or actual[index][k] != case['expected'][k]]
        result['cases'].append({'id': case['id'], 'category': case['category'],
                                'passed': not wrong, 'wrong_fields': wrong})
    result['passed'] = sum(row['passed'] for row in result['cases'])
    result['exact'] = result['passed'] == len(cases) and valid
    return result

def assemble(prompt, cases):
    # Gold answers and rationales never enter held-out requests.
    return prompt + '\nNotes to extract:\n' + json.dumps(
        [{'id': c['id'], 'note': c['note']} for c in cases], indent=2) + '\n'

def schedule(repeats):
    if repeats < 1:
        raise ValueError('repeats must be positive')
    return [{'repeat': r+1, 'arm': ARMS[(position+r)%3]} for r in range(repeats) for position in range(3)]

def summarize(rows, directory, cases):
    trials=[]
    for row in rows:
        output=directory / (row.get('trial','missing')+'.output.txt')
        graded=score(output.read_text() if row['status']==0 and output.exists() else '',cases)
        trials.append({**row, 'score': graded})
    arms={}
    for arm in ARMS:
        selected=[r for r in trials if r['arm']==arm]
        if not selected: continue
        counts=[r['score']['passed'] for r in selected]
        categories={}
        for r in selected:
            for c in r['score']['cases']:
                cat=categories.setdefault(c['category'],{'passed':0,'total':0})
                cat['passed']+=c['passed'];cat['total']+=1
        arms[arm]={'passed':sum(counts),'total':len(cases)*len(selected),
                   'batch_exact':sum(r['score']['exact'] for r in selected),
                   'trials':len(selected),'per_trial_passed':counts,
                   'schema_failures':sum(not r['score']['schema_valid'] for r in selected),
                   'execution_failures':sum(r['status']!=0 for r in selected),
                   'median_elapsed_seconds':round(statistics.median(r['elapsed_seconds'] for r in selected),3),
                   'categories':categories}
    paired={}
    for left,right in [('short','rules'),('rules','examples')]:
        counts={'improved':0,'regressed':0,'both_pass':0,'both_fail':0}
        for repeat in sorted({r['repeat'] for r in trials}):
            a=next((r for r in trials if r['arm']==left and r['repeat']==repeat),None)
            b=next((r for r in trials if r['arm']==right and r['repeat']==repeat),None)
            if a is None or b is None: continue
            for x,y in zip(a['score']['cases'],b['score']['cases']):
                key=('both_pass' if x['passed'] else 'improved') if y['passed'] else ('regressed' if x['passed'] else 'both_fail')
                counts[key]+=1
        paired[f'{left}_to_{right}']=counts
    return {'arms':arms,'paired_case_observations':paired,'trials':trials}

def run(output, repeats, model, timeout):
    if repeats < 1 or timeout <= 0: raise ValueError('positive repeats and timeout required')
    output.mkdir(parents=True,exist_ok=False)
    cases=[c for c in json.loads((ROOT/'dataset.json').read_text()) if c['split']=='heldout']
    files=[ROOT/'dataset.json',ROOT/'PROTOCOL.md',*sorted((ROOT/'prompts').glob('*.txt'))]
    frozen={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    metadata={'model':model,'cli':subprocess.check_output(['codex','--version'],text=True).strip(),
              'repeats':repeats,'timeout_seconds':timeout,'reasoning_effort':'low','sha256':frozen,
              'schedule':schedule(repeats),'trials':[]}
    for p in files:
        target=output/'frozen'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
    (output/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
    for trial in metadata['schedule']:
        name=f'{trial["repeat"]}-{trial["arm"]}'
        prompt=assemble((ROOT/'prompts'/f'{trial["arm"]}.txt').read_text(),cases)
        (output/(name+'.input.txt')).write_text(prompt)
        with tempfile.TemporaryDirectory(prefix='prompt-comparison-') as cwd:
            command=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check',
                     '--sandbox','read-only','-m',model,'-c','model_reasoning_effort="low"',
                     '-C',cwd,'--output-last-message',str((output/(name+'.output.txt')).resolve()),'-']
            started=time.monotonic()
            try:
                completed=subprocess.run(command,input=prompt,text=True,capture_output=True,timeout=timeout)
                status=completed.returncode;log=completed.stdout+'\n'+completed.stderr
            except subprocess.TimeoutExpired as exc:
                status='timeout'
                def decode(value): return value.decode(errors='replace') if isinstance(value,bytes) else (value or '')
                log=decode(exc.stdout)+'\n'+decode(exc.stderr)
            (output/(name+'.log.txt')).write_text(log)
            metadata['trials'].append({**trial,'trial':name,'status':status,
                'elapsed_seconds':round(time.monotonic()-started,3),'command':command})
        (output/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
        print(name,status,flush=True)
    report=summarize(metadata['trials'],output,cases)
    (output/'scores.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0 if all(r['status']==0 for r in metadata['trials']) else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--repeats',type=int,default=3)
    parser.add_argument('--model',default='gpt-6.1-sol')
    parser.add_argument('--timeout',type=int,default=180)
    parser.add_argument('--rescore',action='store_true',help='Recheck frozen saved run; no model call')
    args=parser.parse_args()
    if args.rescore:
        manifest=json.loads((args.output/'manifest.json').read_text())
        cases=[c for c in json.loads((args.output/'frozen/dataset.json').read_text()) if c['split']=='heldout']
        print(json.dumps(summarize(manifest['trials'],args.output,cases),indent=2))
    else:
        raise SystemExit(run(args.output,args.repeats,args.model,args.timeout))
