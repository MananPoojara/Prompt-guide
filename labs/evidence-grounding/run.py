"""Execute the evidence-availability pilot; uses Codex account usage."""
import argparse,hashlib,json,subprocess,tempfile,time
from pathlib import Path
from grounding import conditions,expected,grade
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    corpus=json.loads((ROOT/'corpus.json').read_text());questions=json.loads((ROOT/'questions.json').read_text())
    selected=conditions(corpus);order=list(selected)
    manifest={'model':'gpt-6.1-sol','reasoning_effort':'low','cli':subprocess.check_output(['codex','--version'],text=True).strip(),'trials':[],'sha256':{}}
    frozen=a.output/'frozen';frozen.mkdir()
    for name in ['corpus.json','questions.json','prompt.txt','PROTOCOL.md','grounding.py','run.py']:
        data=(ROOT/name).read_bytes();(frozen/name).write_bytes(data);manifest['sha256'][name]=hashlib.sha256(data).hexdigest()
    (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for repeat in [1,2]:
        for condition in order if repeat==1 else reversed(order):
            name=f'{repeat}-{condition}'
            request=(ROOT/'prompt.txt').read_text()+'\nQuestions:\n'+json.dumps(questions,indent=2)+'\nDocuments:\n'+json.dumps(selected[condition],indent=2)+'\n'
            (a.output/(name+'.input.txt')).write_text(request)
            output=(a.output/(name+'.output.txt')).resolve()
            with tempfile.TemporaryDirectory(prefix='prompt-guide-grounding-') as cwd:
                cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-m','gpt-6.1-sol','-c','model_reasoning_effort="low"','-C',cwd,'--output-last-message',str(output),'-']
                start=time.monotonic()
                try:
                    r=subprocess.run(cmd,input=request,text=True,capture_output=True,timeout=180);status=r.returncode;log=r.stdout+'\n'+r.stderr
                except subprocess.TimeoutExpired as exc:status='timeout';log=str(exc)
                (a.output/(name+'.log.txt')).write_text(log)
                result=grade(output.read_text() if status==0 and output.exists() else '',expected(condition),selected[condition])
                manifest['trials'].append({'trial':name,'repeat':repeat,'condition':condition,'document_ids':[d['id'] for d in selected[condition]],'status':status,'elapsed_seconds':round(time.monotonic()-start,3),'command':cmd,'score':result})
                (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
                print(name,status,result['passed'],result['resolved'],flush=True)
    return 0 if all(r['status']==0 for r in manifest['trials']) else 1

if __name__=='__main__':raise SystemExit(main())
