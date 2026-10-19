import unittest
from grounding import retrieve, grade, conditions

DOCS=[{'id':'old','status':'superseded','text':'club club club time time'},
      {'id':'new','status':'current','text':'club time'}]

class RetrievalTests(unittest.TestCase):
    def test_keyword_score_can_prefer_stale(self):
        self.assertEqual(retrieve(DOCS,'club time')[0]['id'],'old')
    def test_filter_changes_available_evidence(self):
        self.assertEqual(retrieve(DOCS,'club time',current_only=True)[0]['id'],'new')
    def test_empty_query_and_no_matches(self):
        self.assertEqual(retrieve(DOCS,''),[])
        self.assertEqual(retrieve(DOCS,'banana'),[])
    def test_ties_are_deterministic(self):
        self.assertEqual(retrieve([DOCS[1],{**DOCS[1],'id':'aaa'}],'club')[0]['id'],'aaa')

class GradeTests(unittest.TestCase):
    def setUp(self):
        self.expected=[{'id':'start','answer':'14:00','status':'supported','required_sources':['new']}]
        self.docs=[DOCS[1]]
    def test_correct_supported_answer(self):
        self.assertEqual(grade('[{"id":"start","answer":"14:00","status":"supported","sources":["new"]}]',self.expected,self.docs)['passed'],1)
    def test_unsupported_or_wrong_citation(self):
        for sources in ['[]','["missing"]']:
            self.assertEqual(grade('[{"id":"start","answer":"14:00","status":"supported","sources":'+sources+'}]',self.expected,self.docs)['passed'],0)
    def test_correct_abstention_not_resolved(self):
        expected=[{'id':'start','answer':None,'status':'insufficient_evidence','required_sources':[]}]
        r=grade('[{"id":"start","answer":null,"status":"insufficient_evidence","sources":[]}]',expected,[])
        self.assertEqual(r['passed'],1);self.assertEqual(r['resolved'],0)
    def test_schema_errors(self):
        for text in ['null','[]','[3]','```json\n[]\n```','[{"id":"start","answer":14,"status":"supported","sources":["new"]}]']:
            self.assertEqual(grade(text,self.expected,self.docs)['passed'],0)
    def test_either_current_source_can_support_shared_undecided_state(self):
        gold=[{'id':'registration','answer':None,'status':'undecided','required_sources':[],
               'any_sources':['current-plan','alternate-current']}]
        docs=[{'id':'current-plan'},{'id':'alternate-current'}]
        text='[{"id":"registration","answer":null,"status":"undecided","sources":["alternate-current"]}]'
        self.assertEqual(grade(text,gold,docs)['passed'],1)
        self.assertEqual(grade(text.replace('["alternate-current"]','[]'),gold,docs)['passed'],0)
    def test_nonstr_status_is_schema_failure(self):
        self.assertEqual(grade('[{"id":"start","answer":null,"status":[],"sources":[]}]',self.expected,self.docs)['passed'],0)
    def test_conflict_needs_both_sources(self):
        expected=[{'id':'start','answer':None,'status':'conflict','required_sources':['old','new']}]
        r=grade('[{"id":"start","answer":null,"status":"conflict","sources":["new"]}]',expected,DOCS)
        self.assertEqual(r['passed'],0)

if __name__=='__main__':unittest.main()
