"""Small strict application contract; schema checks are not truth checks."""
import datetime,json,re

def unique_object(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:raise ValueError('Duplicate JSON key')
        obj[key]=value
    return obj

def parse(raw):return json.loads(raw,object_pairs_hook=unique_object,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Non-finite JSON number')))

def validate(raw,documents):
    try:data=parse(raw)
    except (ValueError,TypeError):return ['Response must be one JSON object with unique keys']
    if not isinstance(data,dict) or set(data)!={'status','records'}:return ['Expected status and records only']
    if not isinstance(data['status'],str) or data['status'] not in ['ready','needs_review']:return ['Invalid status']
    if not isinstance(data['records'],list):return ['records must be an array']
    if not documents and data!={'status':'needs_review','records':[]}:return ['No evidence: return needs_review with no records']
    if data['status']=='ready' and not data['records']:return ['ready requires at least one record']
    known={d['id'] for d in documents};errors=[]
    for i,row in enumerate(data['records']):
        if not isinstance(row,dict) or set(row)!={'task','owner','deadline','sources'}:
            errors.append(f'record {i}: invalid fields');continue
        if not isinstance(row['task'],str) or not row['task'].strip():errors.append(f'record {i}: task must be nonempty text')
        if row['owner'] is not None and (not isinstance(row['owner'],str) or not row['owner'].strip()):errors.append(f'record {i}: owner must be text or null')
        date=row['deadline']
        if date is not None:
            try:
                if not isinstance(date,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date):raise ValueError()
                datetime.date.fromisoformat(date)
            except ValueError:errors.append(f'record {i}: deadline must be a valid YYYY-MM-DD date or null')
        citations=row['sources']
        if not isinstance(citations,list) or not citations or not all(isinstance(s,str) and s in known for s in citations):errors.append(f'record {i}: cite supplied document IDs')
    return errors

def check_reference(raw,expected):
    try:return parse(raw)==expected
    except (ValueError,TypeError):return False
