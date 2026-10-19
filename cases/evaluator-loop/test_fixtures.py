"""Independent behavioral evidence for the two fixtures; no model required."""
import importlib.util
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parent

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'fixtures' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MinStack

class FixtureEvidence(unittest.TestCase):
    def test_correct_duplicate_minimum(self):
        stack=load('correct')()
        for value in [3,1,1]: stack.push(value)
        self.assertEqual(stack.pop(),1)
        self.assertEqual(stack.getMin(),1)
        self.assertEqual(stack.pop(),1)
        self.assertEqual(stack.getMin(),3)
    def test_buggy_duplicate_minimum_is_wrong(self):
        stack=load('buggy')()
        for value in [3,1,1]: stack.push(value)
        stack.pop()
        self.assertEqual(stack.getMin(),3)  # Observed bug: requirement says 1.
    def test_correct_empty(self):
        stack=load('correct')()
        with self.assertRaises(IndexError): stack.pop()
        with self.assertRaises(IndexError): stack.getMin()
    def test_correct_negative_values(self):
        stack=load('correct')()
        for value in [0,-4,2,-4]: stack.push(value)
        self.assertEqual(stack.getMin(),-4)
        self.assertEqual(stack.pop(),-4)
        self.assertEqual(stack.getMin(),-4)

if __name__=='__main__': unittest.main()
