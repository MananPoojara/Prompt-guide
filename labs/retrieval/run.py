"""Record lexical/dense retrieval and chunk-size comparisons on fictional developer docs."""
import argparse,hashlib,json,platform,time
from pathlib import Path
from importlib.metadata import version
from retrieval import windows,bm25,evaluate
ROOT=Path(__file__).resolve().parent
MODEL='sentence-transformers/all-MiniLM-L6-v2';REVISION='1110a243fdf4706b3f48f1d95db1a4f5529b4d41'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--offline',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    frozen=a.output/'frozen';frozen.mkdir();hashes={}
    for name in ['corpus.json','queries.json','PROTOCOL.md','retrieval.py','run.py']:
        raw=(ROOT/name).read_bytes();(frozen/name).write_bytes(raw);hashes[name]=hashlib.sha256(raw).hexdigest()
    import torch
    from transformers import AutoTokenizer,AutoModel
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,local_files_only=a.offline)
    model=AutoModel.from_pretrained(MODEL,revision=REVISION,use_safetensors=True,local_files_only=a.offline);model.eval()
    corpus=json.loads((frozen/'corpus.json').read_text());queries=json.loads((frozen/'queries.json').read_text())
    for q in queries:
        text=next(d['text'] for d in corpus if d['id']==q['document_id']);assert text.count(q['evidence'])==1
        q['start']=text.index(q['evidence']);q['end']=q['start']+len(q['evidence'])
    def encode(texts):
        output=[]
        for start in range(0,len(texts),16):
            batch=texts[start:start+16]
            assert all(len(tokenizer.encode(t))<=256 for t in batch),'Input would be truncated'
            encoded=tokenizer(batch,padding=True,truncation=False,return_tensors='pt')
            with torch.inference_mode():
                states=model(**encoded).last_hidden_state;mask=encoded['attention_mask'].unsqueeze(-1)
                pooled=(states*mask).sum(1)/mask.sum(1);vectors=torch.nn.functional.normalize(pooled,p=2,dim=1)
            output.extend(vectors.tolist())
        return output
    query_vectors=encode([q['question'] for q in queries]);conditions=[]
    for size in [48,128,254]:
        chunks=[]
        for doc in corpus:
            offsets=tokenizer(doc['text'],add_special_tokens=False,return_offsets_mapping=True)['offset_mapping']
            intervals=[(0,min(254,len(offsets)))] if size==254 else list(windows(len(offsets),size,16))
            for start,end in intervals:
                lo,hi=offsets[start][0],offsets[end-1][1]
                chunks.append({'id':f"{doc['id']}:{start}-{end}",'document_id':doc['id'],'start':lo,'end':hi,'token_start':start,'token_end':end,'text':doc['text'][lo:hi]})
        started=time.monotonic();vectors=encode([c['text'] for c in chunks]);elapsed=time.monotonic()-started
        for method in (['dense'] if size==254 else ['bm25','dense']):
            score_rows=[bm25(q['question'],chunks) for q in queries] if method=='bm25' else [[sum(x*y for x,y in zip(qv,cv)) for cv in vectors] for qv in query_vectors]
            condition={'name':f'{method}-{size}','method':method,'window_tokens':size,'overlap_tokens':0 if size==254 else 16,'chunks':chunks,'chunk_vectors':vectors if method=='dense' else None,'encoding_seconds':round(elapsed,3) if method=='dense' else None,'results':evaluate(queries,chunks,score_rows)}
            conditions.append(condition)
            selected=[r for r in condition['results'] if r['split']=='evaluation'];print(condition['name'],len(chunks),'chunks','evidence@1',sum(r['evidence_coverage_at_1'] for r in selected),'evidence@3',sum(r['evidence_coverage_at_3'] for r in selected),flush=True)
    data={'metadata':{'model':MODEL,'revision':REVISION,'recorded_on':time.strftime('%Y-%m-%d',time.gmtime()),'python':platform.python_version(),'packages':{n:version(n) for n in ['torch','transformers','tokenizers','numpy','huggingface-hub','safetensors']},'sha256':hashes,'device':'cpu','threads':2},'queries':queries,'query_vectors':query_vectors,'conditions':conditions}
    (a.output/'data.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
if __name__=='__main__':main()
