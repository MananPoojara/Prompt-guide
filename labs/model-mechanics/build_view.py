"""Create the offline browser data file from the retained JSON recording."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    data=json.loads((ROOT/'results/recording-2026-10-19/data.json').read_text())
    (ROOT/'data.js').write_text('/* Generated from the retained recording; run build_view.py to refresh. */\nwindow.MODEL_MECHANICS_DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
    print('Offline browser data refreshed from recorded JSON.')
