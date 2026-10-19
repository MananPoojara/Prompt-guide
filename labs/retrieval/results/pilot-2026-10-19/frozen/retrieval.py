"""Transparent lexical ranking and evidence-coverage metrics; no model dependencies."""
import math,re
from collections import Counter

def windows(n,size,overlap):
    if size<=0 or overlap<0 or overlap>=size:raise ValueError('Require 0 <= overlap < size')
    for start in range(0,n,size-overlap):
        end=min(n,start+size);yield start,end
        if end==n:break

def bm25(query,chunks,k1=1.2,b=.75):
    tokenize=lambda text:re.findall(r'\w+',text.lower())
    terms=set(tokenize(query));counts=[Counter(tokenize(c['text'])) for c in chunks]
    lengths=[sum(c.values()) for c in counts];n=len(counts)
    average=sum(lengths)/n if n else 0
    if not average:return [0.0]*n
    df={term:sum(term in c for c in counts) for term in terms}
    scores=[]
    for c,length in zip(counts,lengths):
        value=0.0
        for term in terms:
            tf=c[term];idf=math.log(1+(n-df[term]+.5)/(df[term]+.5))
            value+=idf*tf*(k1+1)/(tf+k1*(1-b+b*length/average))
        scores.append(value)
    return scores

def rank(chunks,scores):return sorted(range(len(chunks)),key=lambda i:(-scores[i],chunks[i]['id']))

def evidence_covered(query,chunks):
    cursor=query['start']
    for chunk in sorted((c for c in chunks if c['document_id']==query['document_id']),key=lambda c:c['start']):
        if chunk['start']>cursor:break
        cursor=max(cursor,chunk['end'])
        if cursor>=query['end']:return True
    return False

def evaluate(queries,chunks,score_rows):
    rows=[]
    for query,scores in zip(queries,score_rows):
        order=rank(chunks,scores)
        row={'query_id':query['id'],'split':query['split'],'ranking':[{'chunk_id':chunks[i]['id'],'score':scores[i]} for i in order]}
        for k in [1,3]:
            selected=[chunks[i] for i in order[:k]]
            row[f'document_hit_at_{k}']=any(c['document_id']==query['document_id'] for c in selected)
            row[f'evidence_coverage_at_{k}']=evidence_covered(query,selected)
            row[f'retrieved_characters_at_{k}']=sum(len(c['text']) for c in selected)
        rows.append(row)
    return rows
