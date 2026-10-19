"""Pure-Python checks for saved vectors and causal attention weights."""
import math

def cosine(a,b):
    if not a or len(a)!=len(b) or not all(math.isfinite(x) for x in a+b):raise ValueError('Expected equal finite nonempty vectors')
    na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0:raise ValueError('Cosine undefined for zero vector')
    return sum(x*y for x,y in zip(a,b))/(na*nb)

def check_attention(matrix):
    n=len(matrix)
    if not n:raise ValueError('Empty attention matrix')
    for i,row in enumerate(matrix):
        if len(row)!=n or not all(math.isfinite(x) and 0<=x<=1+1e-6 for x in row):raise ValueError('Invalid attention values')
        if abs(sum(row)-1)>1e-5:raise ValueError('Attention row does not sum to one')
        if any(abs(row[j])>1e-7 for j in range(i+1,n)):raise ValueError('Future-token attention violates causal mask')
