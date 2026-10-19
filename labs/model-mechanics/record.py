"""Record actual tokenizer and CPU model outputs; no paid API or account required."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import random
import time
from importlib.metadata import version
from sampling import probabilities, choose

MODEL='distilbert/distilgpt2'
REVISION='2290a62682d06624634c1f46a6ad5be0f47f38aa'
PREFIXES=['The capital of France is','The capital of Japan is']
TEXTS=['Hello world',' Hello world','hello world','antidisestablishmentarianism','नमस्ते','🧠','deadline: 2027-02-11']
TEMPERATURES=[0.4,1.0,1.6]
SEEDS=[7,23,41]
TOP_K=50
STEPS=20
ROOT=Path(__file__).resolve().parent

def token_record(tokenizer,text):
    ids=tokenizer.encode(text,add_special_tokens=False)
    decoded=tokenizer.decode(ids,clean_up_tokenization_spaces=False)
    assert decoded==text
    return {'text':text,'ids':ids,'pieces':[tokenizer.decode([i],clean_up_tokenization_spaces=False) for i in ids],
            'vocabulary_pieces':tokenizer.convert_ids_to_tokens(ids),'decoded':decoded}

def candidates(model,torch,ids,tokenizer):
    with torch.inference_mode():
        logits=model(torch.tensor([ids],dtype=torch.long)).logits[0,-1]
    values,indices=torch.topk(logits,TOP_K)
    return [{'id':i,'piece':tokenizer.decode([i],clean_up_tokenization_spaces=False),'logit':v}
            for i,v in zip(indices.tolist(),values.double().tolist())]

def continuation(model,torch,tokenizer,initial,temperature,seed):
    ids=list(initial);rng=random.Random(seed);trace=[]
    for _ in range(STEPS):
        choices=candidates(model,torch,ids,tokenizer)
        probs=probabilities([x['logit'] for x in choices],temperature) if temperature else [1.0]+[0.0]*(TOP_K-1)
        selected=choose(probs,rng) if temperature else 0
        token=choices[selected]
        trace.append({'token_id':token['id'],'piece':token['piece'],'candidate_rank':selected+1,
                      'probability_within_top_k':probs[selected]})
        ids.append(token['id'])
        if token['id']==tokenizer.eos_token_id: break
    return {'temperature':temperature,'seed':seed,'new_ids':ids[len(initial):],
            'text':tokenizer.decode(ids,clean_up_tokenization_spaces=False),
            'continuation':tokenizer.decode(ids[len(initial):],clean_up_tokenization_spaces=False),'trace':trace}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--text',help='Use one custom prefix instead of the two recorded defaults')
    parser.add_argument('--tokenize-only',action='store_true')
    parser.add_argument('--offline',action='store_true',help='Require previously cached model/tokenizer files')
    args=parser.parse_args()
    if args.tokenize_only and args.text is None: parser.error('--tokenize-only requires --text')
    if not args.tokenize_only and args.output is None: parser.error('--output is required for model recordings')
    if args.text is not None and (not args.text.strip() or len(args.text)>500): parser.error('text must contain 1–500 characters and not be whitespace-only')
    if not args.tokenize_only: args.output.mkdir(parents=True,exist_ok=False)
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=args.offline)
    if args.tokenize_only:
        print(json.dumps(token_record(tokenizer,args.text),indent=2,ensure_ascii=False));return
    import torch
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,use_safetensors=True,local_files_only=args.offline)
    model.eval()
    prefixes=[args.text] if args.text is not None else PREFIXES
    data={'metadata':{'model':MODEL,'revision':REVISION,'model_card':f'https://huggingface.co/{MODEL}/tree/{REVISION}',
            'recorded_on':time.strftime('%Y-%m-%d',time.gmtime()),'python':platform.python_version(),
            'packages':{name:version(name) for name in ['torch','transformers','tokenizers','numpy','huggingface-hub','safetensors']},
            'device':'cpu','threads':2,'top_k':TOP_K,'max_new_tokens':STEPS,'temperatures':TEMPERATURES,'seeds':SEEDS,
            'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['record.py','sampling.py','PROTOCOL.md']}},
          'tokenizations':[token_record(tokenizer,t) for t in TEXTS], 'prefixes':[]}
    for name in data['metadata']['sha256']:
        (args.output/name).write_bytes((ROOT/name).read_bytes())
    started=time.monotonic()
    for prefix in prefixes:
        ids=tokenizer.encode(prefix,add_special_tokens=False)
        entry={'prefix':prefix,'input_ids':ids,'first_candidates':candidates(model,torch,ids,tokenizer),'runs':[]}
        entry['runs'].append(continuation(model,torch,tokenizer,ids,0,None))
        for temperature in TEMPERATURES:
            for seed in SEEDS:
                entry['runs'].append(continuation(model,torch,tokenizer,ids,temperature,seed))
        data['prefixes'].append(entry)
        print('Recorded:',prefix,flush=True)
    data['metadata']['elapsed_seconds']=round(time.monotonic()-started,3)
    (args.output/'data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved:',args.output/'data.json')

if __name__=='__main__': main()
