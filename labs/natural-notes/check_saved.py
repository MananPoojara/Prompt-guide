"""Recompute the pilot from its saved scorer and frozen inputs, without inference."""
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results/pilot-2026-10-19'
if __name__=='__main__':
    spec=importlib.util.spec_from_file_location('saved_runner',RUN/'shared-runner.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    m=json.loads((RUN/'manifest.json').read_text())
    for name,digest in m['sha256'].items():
        assert hashlib.sha256((RUN/'frozen'/name).read_bytes()).hexdigest()==digest,name
    cases=[r for r in json.loads((RUN/'frozen/dataset.json').read_text()) if r['split']=='heldout']
    assert len(cases)==12 and len({r['id'] for r in cases})==12
    assert len(m['trials'])==9
    assert [{k:r[k] for k in ['repeat','arm']} for r in m['trials']]==module.schedule(3)
    for r in m['trials']:
        prompt=(RUN/'frozen/prompts'/f'{r["arm"]}.txt').read_text()
        assert (RUN/(r['trial']+'.input.txt')).read_text()==module.assemble(prompt,cases)
        assert (RUN/(r['trial']+'.log.txt')).exists()
    assert module.summarize(m['trials'],RUN,cases)==json.loads((RUN/'scores.json').read_text())
    print('Naturalistic pilot frozen inputs, schedule, requests, and scores verified.')
