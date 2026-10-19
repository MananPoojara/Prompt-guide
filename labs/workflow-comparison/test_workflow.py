import unittest
from workflow import select_current, initial_payload, summarize

DOCS = [
    {"id": "draft", "status": "superseded", "text": "old"},
    {"id": "a", "status": "current", "text": "one"},
    {"id": "b", "status": "current", "text": "two"},
]


class WorkflowTests(unittest.TestCase):
    def test_preserves_both_current_sources(self):
        self.assertEqual([d["id"] for d in select_current(DOCS)], ["a", "b"])

    def test_no_current_means_no_evidence(self):
        self.assertEqual(select_current(DOCS[:1]), [])

    def test_single_and_fixed_differ_only_by_document_selection(self):
        single = initial_payload("single", DOCS)
        fixed = initial_payload("fixed", DOCS)
        self.assertEqual(single["questions"], fixed["questions"])
        self.assertEqual(len(single["documents"]), 3)
        self.assertEqual(len(fixed["documents"]), 2)

    def test_metrics_do_not_call_success_correctness(self):
        result = summarize(
            [
                {"status": 0, "elapsed_seconds": 1.5, "request_characters": 20},
                {"status": "timeout", "elapsed_seconds": 180, "request_characters": 50},
            ]
        )
        self.assertEqual(
            result,
            {
                "calls": 2,
                "process_successes": 1,
                "sum_call_seconds": 181.5,
                "request_characters": 70,
            },
        )
