"""Offline evidence regression gate. Runs no model calls and makes no network requests."""
import argparse,json,statistics,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CHECKS=['scripts/check_links.py','scripts/check_originals.py','labs/prompt-comparison/check_saved.py','labs/example-design/check_saved.py','labs/model-mechanics/check_recording.py','labs/representations/check_saved.py','labs/context-budget/check_saved.py','labs/retrieval/check_saved.py','labs/real-docs/check_saved.py','labs/output-repair/check_saved.py','labs/natural-notes/check_saved.py','labs/evidence-grounding/check_saved.py','labs/bounded-agent/check_saved.py','labs/agent-recovery/check_saved.py','labs/memory-lifecycle/check_saved.py','labs/workflow-comparison/check_saved.py','labs/action-approval/check_saved.py','labs/trust-boundaries/check_saved.py','labs/eval-uncertainty/check_saved.py','labs/skill-execution/check_saved.py']

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    checks=[]
    for path in CHECKS:
        r=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,text=True,capture_output=True,timeout=120)
        checks.append({'path':path,'passed':r.returncode==0,'output':r.stdout+r.stderr})
    timings=[]
    for label,path in [('natural-notes','labs/natural-notes/results/pilot-2026-10-19/manifest.json'),('evidence-grounding','labs/evidence-grounding/results/pilot-2026-10-19/manifest.json'),('bounded-agent','labs/bounded-agent/results/resumed-2026-10-19/state.json')]:
        data=json.loads((ROOT/path).read_text());trials=data.get('trials',data.get('history',[]));values=[t['elapsed_seconds'] for t in trials]
        timings.append({'experiment':label,'source':path,'calls':len(trials),'process_successes':sum(t['status']==0 for t in trials),'sum_call_seconds':round(sum(values),3),'median_call_seconds':round(statistics.median(values),3),'billing_cost':None})
    report={'scope':'Saved evidence integrity and deterministic regrading; no fresh inference','checks':checks,'runtime_observations':timings,'independent_human_review':'pending','judge_calibration':'not performed','production_readiness':'not established'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(timings,indent=2));print(f"{sum(c['passed'] for c in checks)}/{len(checks)} evidence checks passed")
    return int(not all(c['passed'] for c in checks))
if __name__=='__main__':raise SystemExit(main())
