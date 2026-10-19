import math
import random
import unittest
from sampling import probabilities, choose

class SamplingTests(unittest.TestCase):
    def test_normalizes_and_handles_large_logits(self):
        p=probabilities([10000,9999,9998],1)
        self.assertAlmostEqual(sum(p),1)
        self.assertTrue(p[0]>p[1]>p[2]>0)
    def test_uniform_logits(self):
        self.assertEqual(probabilities([0,0],.5),[.5,.5])
    def test_colder_is_more_concentrated(self):
        self.assertGreater(probabilities([3,2,1],.4)[0],probabilities([3,2,1],1.6)[0])
    def test_extreme_temperature_stays_finite(self):
        p=probabilities([3,2,1],.00001)
        self.assertEqual(p,[1,0,0])
    def test_rejects_invalid_inputs(self):
        for logits,temp in [([],1),([1],0),([1],-1),([math.nan],1),([math.inf],1),([1],math.inf)]:
            with self.subTest(logits=logits,temp=temp):
                with self.assertRaises(ValueError): probabilities(logits,temp)
    def test_seeded_sampling_is_repeatable(self):
        a=random.Random(7);b=random.Random(7)
        self.assertEqual([choose([.2,.8],a) for _ in range(20)],[choose([.2,.8],b) for _ in range(20)])
    def test_zero_probability_not_selected(self):
        rng=random.Random(9)
        self.assertEqual([choose([0,1,0],rng) for _ in range(100)],[1]*100)
    def test_sampler_rejects_invalid_distribution(self):
        for p in [[],[-.1,1.1],[.2,.2],[math.nan,1]]:
            with self.assertRaises(ValueError): choose(p,random.Random(1))

if __name__=='__main__': unittest.main()
