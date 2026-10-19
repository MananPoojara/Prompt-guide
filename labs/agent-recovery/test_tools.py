import unittest
from recovery import dispatch
DOCS=[{'id':'current-plan','text':'Start 14:00','status':'current'}]
class FaultTests(unittest.TestCase):
 def state(self):return {'read':[],'done':False,'fault_used':False}
 def test_transient_once_then_success(self):
  s=self.state();self.assertTrue(dispatch(s,{'action':'read','id':'current-plan'},DOCS,'transient')['retryable']);self.assertEqual(s['read'],[])
  self.assertIn('document',dispatch(s,{'action':'read','id':'current-plan'},DOCS,'transient'));self.assertEqual(s['read'],['current-plan'])
 def test_denied_never_reads(self):
  s=self.state()
  for _ in range(2):self.assertFalse(dispatch(s,{'action':'read','id':'current-plan'},DOCS,'denied')['retryable'])
  self.assertEqual(s['read'],[])
 def test_search_not_faulted(self):self.assertIn('documents',dispatch(self.state(),{'action':'search','query':'start'},DOCS,'transient'))
 def test_invalid_not_converted_to_network_error(self):self.assertIn('error',dispatch(self.state(),{'action':'read','id':[]},DOCS,'transient'))
