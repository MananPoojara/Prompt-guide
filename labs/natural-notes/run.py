"""Run the frozen naturalistic-note pilot through the shared Codex runner."""
import argparse
import importlib.util
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'prompt-comparison/experiment.py'
spec=importlib.util.spec_from_file_location('shared_experiment',SOURCE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.ROOT=ROOT

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--repeats',type=int,default=3)
    args=parser.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    # Snapshot before calling the shared runner; it creates its own output directory.
    snapshot=SOURCE.read_bytes()
    try:
        code=module.run(args.output,args.repeats,'gpt-6.1-sol',180)
    finally:
        if args.output.exists():(args.output/'shared-runner.py').write_bytes(snapshot)
    raise SystemExit(code)
