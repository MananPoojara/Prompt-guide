"""Compare submitted annotations with gold labels without granting automatic approval."""
import argparse
import json
from pathlib import Path

def audit(packet,gold):
    expected={r['id']:r['expected'] for r in gold}
    rows=packet['cases'];ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected):
        raise ValueError('Exactly one annotation per expected case is required')
    result={'reviewed':0,'unreviewed':0,'uncertain':0,'agreements':0,'disagreements':[],
            'reviewer_declaration':packet['reviewer'],'approval':'not automatically granted'}
    for row in rows:
        if row['judgment'] not in {'unreviewed','uncertain','confirmed'}:
            raise ValueError('Unknown judgment')
        if row['judgment']=='unreviewed':result['unreviewed']+=1;continue
        if any(row[k] is not None and not isinstance(row[k],str) for k in ['owner','deadline']):
            raise ValueError('Labels must be strings or null')
        result['reviewed']+=1
        result['uncertain']+=row['judgment']=='uncertain'
        wrong=[k for k in ['owner','deadline'] if row[k]!=expected[row['id']][k]]
        if wrong:
            result['disagreements'].append({'id':row['id'],'fields':wrong,'comment':row.get('comment','')})
        else:result['agreements']+=1
    reviewer=packet['reviewer']
    result['eligible_for_maintainer_review']=(result['unreviewed']==0 and result['uncertain']==0
        and not result['disagreements'] and reviewer.get('type')=='human'
        and reviewer.get('independent') is True and bool(reviewer.get('name','').strip()))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet',type=Path)
    args=parser.parse_args()
    gold=[r for r in json.loads((Path(__file__).resolve().parents[1]/'dataset.json').read_text()) if r['split']=='heldout']
    print(json.dumps(audit(json.loads(args.packet.read_text()),gold),indent=2))
