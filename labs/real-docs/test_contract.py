import unittest
from contract import pack, grade


class ContractTests(unittest.TestCase):
    def test_skip_oversized_without_losing_later_fit(self):
        chunks = [{"id": "big", "text": "x" * 100}, {"id": "small", "text": "ok"}]
        selected, packet, count = pack(chunks, [0, 1], lambda s: len(s), 30)
        self.assertEqual([c["id"] for c in selected], ["small"])
        self.assertEqual(count, len(packet))
        self.assertLessEqual(count, 30)

    def test_full_packet_recount_and_no_partial_chunks(self):
        chunks = [{"id": "a", "text": "one"}, {"id": "b", "text": "two"}]
        selected, packet, count = pack(chunks, [0, 1], len, 10)
        self.assertEqual(len(selected), 1)
        self.assertEqual(packet, "[a]\none")
        self.assertEqual(count, 7)

    def test_bad_budget(self):
        with self.assertRaises(ValueError):
            pack([], [], len, 0)

    def fixture(self):
        return {"answers": ["file://"], "evidence": "MUST use file://"}, [
            {"id": "a", "text": "Roots MUST use file:// here."}
        ]

    def test_supported(self):
        q, c = self.fixture()
        r = grade(
            {
                "status": "answered",
                "answer": "file://",
                "chunk_id": "a",
                "quote": "MUST use file://",
            },
            q,
            c,
        )
        self.assertTrue(r["answer_correct"])
        self.assertTrue(r["supported"])

    def test_fabricated_quote_and_wrong_citation(self):
        q, c = self.fixture()
        for chunk, quote in [
            ("b", "MUST use file://"),
            ("a", "MUST use file:// invented"),
        ]:
            r = grade(
                {
                    "status": "answered",
                    "answer": "file://",
                    "chunk_id": chunk,
                    "quote": quote,
                },
                q,
                c,
            )
            self.assertTrue(r["answer_correct"])
            self.assertFalse(r["supported"])

    def test_valid_quote_wrong_answer(self):
        q, c = self.fixture()
        r = grade(
            {
                "status": "answered",
                "answer": "https://",
                "chunk_id": "a",
                "quote": "MUST use file://",
            },
            q,
            c,
        )
        self.assertFalse(r["answer_correct"])
        self.assertFalse(r["supported"])

    def test_missing_and_invalid(self):
        q, c = self.fixture()
        r = grade(
            {
                "status": "insufficient_evidence",
                "answer": None,
                "chunk_id": None,
                "quote": None,
            },
            q,
            c,
        )
        self.assertTrue(r["schema_valid"])
        self.assertFalse(r["answer_correct"])
        for output in [
            [],
            {},
            {"status": "answered", "answer": 2, "chunk_id": "a", "quote": "x"},
        ]:
            self.assertFalse(grade(output, q, c)["schema_valid"])


if __name__ == "__main__":
    unittest.main()
