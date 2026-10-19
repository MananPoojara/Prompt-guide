import unittest
from uncertainty import wilson, cluster_bootstrap, quantile


class UncertaintyTests(unittest.TestCase):
    def test_all_success_is_not_certainty(self):
        low, high = wilson(10, 10)
        self.assertAlmostEqual(low, 0.7224672, places=6)
        self.assertAlmostEqual(high, 1)

    def test_no_success_bounds(self):
        low, high = wilson(0, 10)
        self.assertAlmostEqual(low, 0)
        self.assertAlmostEqual(high, 0.2775328, places=6)

    def test_invalid_counts(self):
        for k, n in [(0, 0), (-1, 10), (11, 10), (1.5, 10)]:
            with self.assertRaises(ValueError):
                wilson(k, n)

    def test_quantile_interpolates(self):
        self.assertEqual(quantile([0, 10], 0.25), 2.5)

    def test_identical_pairs_degenerate(self):
        result = cluster_bootstrap(
            [{"cluster": "a", "delta": 0}, {"cluster": "b", "delta": 0}], 100, 7
        )
        self.assertEqual(result["interval"], [0, 0])
        self.assertEqual(result["clusters"], 2)

    def test_shared_cluster_stays_together(self):
        result = cluster_bootstrap(
            [{"cluster": "a", "delta": 1}, {"cluster": "a", "delta": -1}], 100, 7
        )
        self.assertEqual(result["interval"], [0, 0])
        self.assertEqual(result["clusters"], 1)

    def test_repeatable(self):
        rows = [{"cluster": "a", "delta": 1}, {"cluster": "b", "delta": 0}]
        self.assertEqual(
            cluster_bootstrap(rows, 100, 9), cluster_bootstrap(rows, 100, 9)
        )

    def test_invalid_bootstrap(self):
        with self.assertRaises(ValueError):
            cluster_bootstrap([], 10, 1)
        with self.assertRaises(ValueError):
            cluster_bootstrap([{"cluster": "a", "delta": 0}], 0, 1)
