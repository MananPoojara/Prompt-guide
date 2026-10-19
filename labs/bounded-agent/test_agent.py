import unittest
from agent import act, initial
DOCS=[{'id':'current','text':'Capacity 20','status':'current'}]
class AgentTests(unittest.TestCase):
    def test_unknown_tool_denied(self):
        s=initial(3); self.assertIn('error',act(s,{'action':'delete'},DOCS)); self.assertEqual(s['read'],[])
    def test_read_requires_known_id(self):
        self.assertIn('error',act(initial(3),{'action':'read','id':'../../secret'},DOCS))
    def test_search_does_not_read(self):
        s=initial(3); result=act(s,{'action':'search','query':'capacity'},DOCS)
        self.assertNotIn('text',result['documents'][0]);self.assertEqual(s['read'],[])
    def test_citation_requires_read(self):
        s=initial(3); answer=[{'id':'capacity','answer':'20','status':'supported','sources':['current']}]
        self.assertIn('error',act(s,{'action':'final','answers':answer},DOCS))
        act(s,{'action':'read','id':'current'},DOCS)
        self.assertTrue(act(s,{'action':'final','answers':answer},DOCS)['accepted'])
    def test_invalid_args(self):
        for decision in [[],{'action':[]},{'action':'read','id':[]},{'action':'search','query':4}]:
            self.assertIn('error',act(initial(3),decision,DOCS))
    def test_extra_args_denied(self):
        self.assertIn('error',act(initial(3),{'action':'read','id':'current','path':'x'},DOCS))
if __name__=='__main__':unittest.main()
