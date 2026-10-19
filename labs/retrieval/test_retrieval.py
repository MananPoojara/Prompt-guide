import unittest
from retrieval import bm25,rank,evidence_covered,windows
class RetrievalTests(unittest.TestCase):
 def test_exact_word_ranks(self):
  scores=bm25('cursor',[{'text':'cursor next cursor'},{'text':'unrelated document'}]);self.assertGreater(scores[0],scores[1])
 def test_empty_query(self):self.assertEqual(bm25('',[{'text':'a'},{'text':''}]),[0,0])
 def test_ties_stable(self):self.assertEqual(rank([{'id':'b'},{'id':'a'}],[0,0]),[1,0])
 def test_windows(self):self.assertEqual(list(windows(10,4,1)),[(0,4),(3,7),(6,10)])
 def test_bad_windows(self):
  for n,size,overlap in [(10,0,0),(10,3,3),(10,3,-1)]:
   with self.assertRaises(ValueError):list(windows(n,size,overlap))
 def test_evidence_across_chunks(self):
  q={'document_id':'x','start':3,'end':9}
  self.assertTrue(evidence_covered(q,[{'document_id':'x','start':0,'end':6},{'document_id':'x','start':6,'end':10}]))
  self.assertFalse(evidence_covered(q,[{'document_id':'x','start':0,'end':5},{'document_id':'x','start':6,'end':10}]))
 def test_wrong_document(self):self.assertFalse(evidence_covered({'document_id':'x','start':0,'end':2},[{'document_id':'y','start':0,'end':10}]))

class EvaluationTests(unittest.TestCase):
 def test_document_hit_is_not_evidence_coverage(self):
  from retrieval import evaluate
  rows=evaluate([{'id':'q','split':'evaluation','document_id':'x','start':10,'end':20}],[{'id':'x:0','document_id':'x','start':0,'end':5,'text':'short'}],[[1.]])
  self.assertTrue(rows[0]['document_hit_at_1']);self.assertFalse(rows[0]['evidence_coverage_at_1']);self.assertEqual(rows[0]['retrieved_characters_at_3'],5)
 def test_empty_corpus(self):
  self.assertEqual(bm25('query',[]),[]);self.assertEqual(bm25('query',[{'text':''}]),[0.])
 def test_no_windows_for_empty_input(self):self.assertEqual(list(windows(0,4,1)),[])
