import unittest
from review import audit

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.gold=[{'id':'x','expected':{'owner':'A','deadline':None}}]
    def packet(self,judgment='unreviewed',owner=None):
        return {'reviewer':{'name':'Reviewer','type':'human','independent':True},'cases':[{'id':'x','owner':owner,'deadline':None,'judgment':judgment,'comment':''}]}
    def test_blanks_are_not_agreements(self):
        r=audit(self.packet(),self.gold)
        self.assertEqual(r['reviewed'],0);self.assertEqual(r['agreements'],0)
        self.assertFalse(r['eligible_for_maintainer_review'])
    def test_disagreement_retained(self):
        r=audit(self.packet('confirmed','B'),self.gold)
        self.assertEqual(r['disagreements'][0]['fields'],['owner'])
        self.assertFalse(r['eligible_for_maintainer_review'])
    def test_human_declaration_does_not_autoapprove(self):
        r=audit(self.packet('confirmed','A'),self.gold)
        self.assertTrue(r['eligible_for_maintainer_review'])
        self.assertEqual(r['approval'],'not automatically granted')
    def test_uncertainty_blocks_gate(self):
        r=audit(self.packet('uncertain','A'),self.gold)
        self.assertFalse(r['eligible_for_maintainer_review'])
    def test_missing_duplicate_unknown_rejected(self):
        for ids in [[],['x','x'],['other']]:
            p=self.packet();p['cases']=[{**p['cases'][0],'id':i} for i in ids]
            with self.assertRaises(ValueError):audit(p,self.gold)
    def test_model_review_not_independent_human(self):
        p=self.packet('confirmed','A');p['reviewer']['type']='model'
        self.assertFalse(audit(p,self.gold)['eligible_for_maintainer_review'])
    def test_invalid_judgment_rejected(self):
        with self.assertRaises(ValueError):audit(self.packet('looks-good'),self.gold)

if __name__=='__main__':unittest.main()
