import json,unittest
from contract import validate,check_reference
DOCS=[{'id':'note-1','text':'Morgan proposed owning the export. Nobody accepted.'}]
GOOD={'status':'ready','records':[{'task':'export','owner':None,'deadline':None,'sources':['note-1']}]}
class ContractTests(unittest.TestCase):
 def test_valid(self):self.assertEqual(validate(json.dumps(GOOD),DOCS),[])
 def test_syntax(self):self.assertTrue(validate('{"status":',DOCS))
 def test_duplicate_keys(self):self.assertTrue(validate('{"status":"ready","status":"needs_review","records":[]}',DOCS))
 def test_wrong_type(self):self.assertTrue(validate('{"status":true,"records":[]}',DOCS))
 def test_unknown_citation(self):
  x=json.loads(json.dumps(GOOD));x['records'][0]['sources']=['fake'];self.assertTrue(validate(json.dumps(x),DOCS))
 def test_schema_does_not_establish_truth(self):
  x=json.loads(json.dumps(GOOD));x['records'][0]['owner']='Morgan';self.assertEqual(validate(json.dumps(x),DOCS),[]);self.assertFalse(check_reference(json.dumps(x),GOOD))
 def test_no_source_requires_review(self):
  self.assertTrue(validate(json.dumps(GOOD),[]));self.assertEqual(validate('{"status":"needs_review","records":[]}',[]),[])
 def test_bad_calendar_date(self):
  x=json.loads(json.dumps(GOOD));x['records'][0]['deadline']='2027-02-30';self.assertTrue(validate(json.dumps(x),DOCS))
 def test_empty_citations(self):
  x=json.loads(json.dumps(GOOD));x['records'][0]['sources']=[];self.assertTrue(validate(json.dumps(x),DOCS))
