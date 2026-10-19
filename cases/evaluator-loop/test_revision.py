"""Independent behavior checks on the exact generated revision."""
import importlib.util
from pathlib import Path
import random
import unittest
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generated_revision',ROOT/'results/revision.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RevisionTests(unittest.TestCase):
    def test_duplicate_minima(self):
        stack=module.MinStack()
        for value in [3,1,1]: stack.push(value)
        self.assertEqual(stack.pop(),1)
        self.assertEqual(stack.getMin(),1)
        self.assertEqual(stack.pop(),1)
        self.assertEqual(stack.getMin(),3)
    def test_empty(self):
        stack=module.MinStack()
        with self.assertRaises(IndexError): stack.pop()
        with self.assertRaises(IndexError): stack.getMin()
    def test_reuse_after_empty(self):
        stack=module.MinStack();stack.push(-3)
        self.assertEqual(stack.pop(),-3)
        stack.push(7);self.assertEqual(stack.getMin(),7)
    def test_mixed_operations_against_reference(self):
        rng=random.Random(1729);stack=module.MinStack();reference=[]
        for _ in range(500):
            if not reference or rng.random()<0.6:
                value=rng.randint(-20,20);reference.append(value);stack.push(value)
            else:
                self.assertEqual(stack.pop(),reference.pop())
            if reference:self.assertEqual(stack.getMin(),min(reference))
            else:
                with self.assertRaises(IndexError):stack.getMin()

if __name__=='__main__':unittest.main()
