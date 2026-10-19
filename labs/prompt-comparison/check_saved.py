"""Verify retained experiment provenance and recompute scores without a model call."""
import hashlib
import json
from pathlib import Path
from experiment import assemble, schedule, summarize

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results/pilot-low-2026-10-19'

def main():
    manifest=json.loads((RUN/'manifest.json').read_text())
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((RUN/'frozen'/name).read_bytes()).hexdigest()==digest, name
    cases=json.loads((RUN/'frozen/dataset.json').read_text())
    assert len({c['id'] for c in cases})==len(cases)==24
    heldout=[c for c in cases if c['split']=='heldout']
    assert len(heldout)==16
    assert all(sum(c['category']==category for c in heldout)==2 for category in {c['category'] for c in heldout})
    expected_schedule=schedule(manifest['repeats'])
    assert manifest['schedule']==expected_schedule
    assert [{k:r[k] for k in ('repeat','arm')} for r in manifest['trials']]==expected_schedule
    for row in manifest['trials']:
        prefix=RUN/row['trial']
        prompt=(RUN/'frozen/prompts'/f'{row["arm"]}.txt').read_text()
        assert Path(str(prefix)+'.input.txt').read_text()==assemble(prompt,heldout)
        assert Path(str(prefix)+'.log.txt').exists()
        if row['status']==0: assert Path(str(prefix)+'.output.txt').exists()
    calculated=summarize(manifest['trials'],RUN,heldout)
    assert calculated==json.loads((RUN/'scores.json').read_text())
    print('Frozen inputs, nine-trial schedule, raw artifacts, and recomputed scores verified.')

if __name__=='__main__': main()
