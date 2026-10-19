import unittest
from metrics import cosine, check_attention


class MetricsTests(unittest.TestCase):
    def test_cosine(self):
        self.assertAlmostEqual(cosine([1, 0], [1, 0]), 1)
        self.assertAlmostEqual(cosine([1, 0], [0, 1]), 0)
        self.assertAlmostEqual(cosine([1, 0], [-1, 0]), -1)

    def test_bad_vectors(self):
        for a, b in [([0, 0], [1, 0]), ([1], [1, 2]), ([float("nan")], [1])]:
            with self.assertRaises(ValueError):
                cosine(a, b)

    def test_causal_attention(self):
        check_attention([[1, 0], [0.25, 0.75]])

    def test_invalid_attention(self):
        for matrix in [
            [[0.5, 0.5], [0.5, 0.5]],
            [[1, 0], [0.2, 0.2]],
            [[1, 0], [-0.2, 1.2]],
            [[1], [1, 0]],
        ]:
            with self.assertRaises(ValueError):
                check_attention(matrix)
