"""Record actual token vectors and every attention head from a pinned small model."""
import argparse,hashlib,json,platform,time
from pathlib import Path
from importlib.metadata import version
from metrics import cosine
ROOT=Path(__file__).resolve().parent
MODEL='distilbert/distilgpt2';REVISION='2290a62682d06624634c1f46a6ad5be0f47f38aa'
TEXTS=['The river bank is quiet.','The money bank is quiet.']
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=a.offline)
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,use_safetensors=True,local_files_only=a.offline);model.eval()
    data={'metadata':{'model':MODEL,'revision':REVISION,'recorded_on':time.strftime('%Y-%m-%d',time.gmtime()),'python':platform.python_version(),'packages':{n:version(n) for n in ['torch','transformers','tokenizers','numpy','huggingface-hub','safetensors']},'device':'cpu','threads':2,'layers':model.config.n_layer,'heads':model.config.n_head,'dimensions':model.config.n_embd,'sha256':{}},'inputs':[]}
    for name in ['record.py','metrics.py','PROTOCOL.md']:
        raw=(ROOT/name).read_bytes();(a.output/name).write_bytes(raw);data['metadata']['sha256'][name]=hashlib.sha256(raw).hexdigest()
    target=tokenizer.encode(' bank',add_special_tokens=False);assert len(target)==1
    for text in TEXTS:
        ids=tokenizer.encode(text,add_special_tokens=False);assert ids.count(target[0])==1
        tensor=torch.tensor([ids])
        with torch.inference_mode():
            result=model(tensor,output_attentions=True,output_hidden_states=True)
            embeddings=model.transformer.wte(tensor)[0].tolist()
        data['inputs'].append({'text':text,'ids':ids,'pieces':[tokenizer.decode([i]) for i in ids],'target_position':ids.index(target[0]),'vectors':{'token_embedding':embeddings,'input_hidden':result.hidden_states[0][0].tolist(),'final_hidden':result.hidden_states[-1][0].tolist()},'attention':[t[0].tolist() for t in result.attentions]})
    x,y=data['inputs'];assert x['target_position']==y['target_position'];i=x['target_position']
    data['target_cosines']={stage:cosine(x['vectors'][stage][i],y['vectors'][stage][i]) for stage in x['vectors']}
    (a.output/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps(data['target_cosines'],indent=2))
if __name__=='__main__':main()
