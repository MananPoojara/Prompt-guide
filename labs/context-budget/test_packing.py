import unittest
from packing import pack, truncate


class PackingTests(unittest.TestCase):
    def test_preserves_required_and_skips_oversize_document(self):
        result = pack(
            "I",
            "Q",
            [{"id": "large", "text": "x" * 100}, {"id": "small", "text": "fact"}],
            20,
            4,
            len,
        )
        self.assertEqual(result["selected"], ["small"])
        self.assertIn("I", result["text"])
        self.assertIn("Q", result["text"])
        self.assertLessEqual(len(result["text"]) + 4, 20)

    def test_required_cannot_fit(self):
        with self.assertRaises(ValueError):
            pack("instructions", "question", [], 10, 5, len)

    def test_invalid_budget(self):
        for capacity, reserve in [(0, 0), (10, 10), (10, -1), (True, 0)]:
            with self.assertRaises(ValueError):
                pack("I", "Q", [], capacity, reserve, len)

    def test_document_priority(self):
        result = pack(
            "I",
            "Q",
            [{"id": "a", "text": "aaa"}, {"id": "b", "text": "bbb"}],
            12,
            1,
            len,
        )
        self.assertEqual(result["selected"], ["a"])

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            pack(
                "I",
                "Q",
                [{"id": "a", "text": "x"}, {"id": "a", "text": "y"}],
                100,
                0,
                len,
            )

    def test_cutting_token_ids(self):
        self.assertEqual(truncate(list(range(8)), 3, "prefix"), [0, 1, 2])
        self.assertEqual(truncate(list(range(8)), 3, "suffix"), [5, 6, 7])
        with self.assertRaises(ValueError):
            truncate([1], 1, "middle")

    def test_complete_text_is_recounted(self):
        calls = []

        def count(value):
            calls.append(value)
            return len(value)

        result = pack("I", "Q", [{"id": "a", "text": "fact"}], 30, 1, count)
        self.assertIn(result["text"], calls)
