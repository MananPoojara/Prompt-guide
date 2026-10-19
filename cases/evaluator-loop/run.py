"""Run the unchanged Anthropic evaluator text on fixed fixtures in Codex.
Uses account usage. No external Python dependencies. Never overwrites a run.
"""
import argparse, json, subprocess, tempfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--repeats',type=int,default=3)
    args=parser.parse_args()
    if args.repeats<1: parser.error('--repeats must be positive')
    args.output.mkdir(parents=True,exist_ok=False)
    prompt=(REPO/'originals/vendor/anthropic-cookbook/evaluator_prompt.txt').read_text()
    task=(ROOT/'fixtures/task.txt').read_text()
    version=subprocess.check_output(['codex','--version'],text=True).strip()
    manifest=[]
    with tempfile.TemporaryDirectory(prefix='prompt-guide-evaluator-') as cwd:
        for repeat in range(args.repeats):
            order=['buggy','correct'] if repeat%2==0 else ['correct','buggy']
            for variant in order:
                name=f'{repeat+1}-{variant}'
                assembled=f'{prompt}\nOriginal task: {task}\nContent to evaluate: {(ROOT/"fixtures"/(variant+".py")).read_text()}'
                (args.output/(name+'.input.txt')).write_text(assembled)
                output=(args.output/(name+'.output.txt')).resolve()
                command=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-C',cwd,'--output-last-message',str(output),'-']
                start=time.monotonic()
                try:
                    result=subprocess.run(command,input=assembled,text=True,capture_output=True,timeout=180)
                    (args.output/(name+'.log.txt')).write_text(result.stdout+'\n'+result.stderr)
                    status=result.returncode
                except subprocess.TimeoutExpired:
                    status='timeout'
                manifest.append({'trial':name,'cli':version,'exit_status':status,'elapsed_seconds':round(time.monotonic()-start,3),'command':command,'prompt_source':'AC-evaluator','variant':variant})
                (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
                print(name,status,flush=True)
    return 0 if all(x['exit_status']==0 for x in manifest) else 1

if __name__=='__main__': raise SystemExit(main())
