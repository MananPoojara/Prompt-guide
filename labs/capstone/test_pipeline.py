import json
import unittest
from pipeline import retrieve, assemble, grade, parse


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.docs = [
            dict(
                id="a",
                revision="v1",
                scope="public",
                current=True,
                text="Retry limit is three attempts.",
            )
        ]
        self.q = dict(
            question="What is the retry limit?",
            scope="public",
            expected_status="answered",
            answers=["three"],
            required_docs=["a"],
        )

    def test_scope_and_superseded_filtered_before_ranking(self):
        docs = self.docs + [
            dict(self.docs[0], id="private", scope="secret"),
            dict(self.docs[0], id="old", current=False),
        ]
        chunks = retrieve(docs, self.q)
        self.assertEqual({x["document_id"] for x in chunks}, {"a"})

    def test_windows_reconstruct_exact_sources(self):
        self.docs[0]["text"] = "retry " * 40
        for c in retrieve(self.docs, self.q):
            self.assertEqual(c["text"], self.docs[0]["text"][c["start"] : c["end"]])

    def test_budget_recounts_full_request_without_cutting_question(self):
        ranked = retrieve(self.docs, self.q)
        base, _ = assemble(self.q, [], 3, len, 10000)
        request, selected = assemble(self.q, ranked, 3, len, len(base))
        self.assertEqual(selected, [])
        self.assertIn(self.q["question"], request)
        with self.assertRaises(ValueError):
            assemble(self.q, ranked, 3, len, 1)

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):
            parse('{"status": "answered", "status": "insufficient_evidence"}')

    def test_correct_answer_and_citation_separate(self):
        chunks = retrieve(self.docs, self.q)
        answer = dict(
            status="answered",
            answer="three",
            citations=[dict(document_id="a", revision="v1", start=0, end=29)],
            unresolved_reason=None,
        )
        self.assertTrue(grade(answer, self.q, chunks)["passed"])
        answer["answer"] = "nine"
        result = grade(answer, self.q, chunks)
        self.assertTrue(result["citations_valid"])
        self.assertFalse(result["reference_correct"])
        answer["citations"][0]["revision"] = "v0"
        self.assertFalse(grade(answer, self.q, chunks)["citations_valid"])

    def test_bad_schema_and_boolean_offsets(self):
        for answer in [
            [],
            {},
            dict(
                status="answered",
                answer="three",
                citations=[],
                unresolved_reason=None,
                approved=True,
            ),
        ]:
            self.assertFalse(grade(answer, self.q, [])["passed"])
        answer = dict(
            status="answered",
            answer="three",
            citations=[dict(document_id="a", revision="v1", start=False, end=29)],
            unresolved_reason=None,
        )
        self.assertFalse(
            grade(answer, self.q, retrieve(self.docs, self.q))["citations_valid"]
        )

    def test_missing_and_conflict_contracts(self):
        missing = dict(
            self.q,
            expected_status="insufficient_evidence",
            answers=[],
            required_docs=[],
        )
        answer = dict(
            status="insufficient_evidence",
            answer=None,
            citations=[],
            unresolved_reason="No evidence",
        )
        self.assertTrue(grade(answer, missing, [])["passed"])
        answer["unresolved_reason"] = ""
        self.assertFalse(grade(answer, missing, [])["passed"])
        conflict = dict(
            self.q,
            expected_status="conflicting_evidence",
            answers=[],
            required_docs=["a", "b"],
        )
        answer = dict(
            status="conflicting_evidence",
            answer=None,
            citations=[],
            unresolved_reason="Conflict",
        )
        self.assertFalse(grade(answer, conflict, [])["passed"])

    def test_selected_limit_and_valid_json(self):
        ranked = retrieve(self.docs + [dict(self.docs[0], id="b")], self.q)
        request, selected = assemble(self.q, ranked, 1, len, 10000)
        self.assertEqual(len(selected), 1)
        self.assertIn(selected[0]["text"], request)
        self.assertEqual(parse('{"x": 1}'), {"x": 1})
        with self.assertRaises(ValueError):
            parse(" " * 8193)

    def test_invalid_states_and_citation_shapes(self):
        base = dict(
            status="answered", answer="three", citations=[], unresolved_reason=None
        )
        for answer in [base, dict(base, status="approved"), dict(base, citations=[{}])]:
            self.assertFalse(grade(answer, self.q, [])["schema_valid"])

    def test_end_to_end_fixture_conflict_and_missing_scope(self):
        from pathlib import Path

        root = Path(__file__).resolve().parent
        docs = json.loads((root / "documents.json").read_text())
        questions = json.loads((root / "questions.json").read_text())
        q = next(q for q in questions if q["id"] == "conflict")
        ranked = retrieve(docs, q)
        _, selected = assemble(q, ranked, 3, len, 10000)
        citations = [
            dict(
                document_id=c["document_id"],
                revision=c["revision"],
                start=c["start"],
                end=c["end"],
            )
            for c in selected
        ]
        answer = dict(
            status="conflicting_evidence",
            answer=None,
            citations=citations,
            unresolved_reason="Two current decisions differ",
        )
        self.assertTrue(grade(answer, q, selected)["passed"])
        answer["citations"] = citations[:1]
        self.assertFalse(grade(answer, q, selected)["passed"])
        scoped = next(q for q in questions if q["id"] == "scope")
        request, selected = assemble(scoped, retrieve(docs, scoped), 3, len, 10000)
        self.assertNotIn("ORCHID", request)
        self.assertNotIn("restricted", request)


if __name__ == "__main__":
    unittest.main()
