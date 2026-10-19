import copy
import unittest
from workflow import initial, dispatch, reserve, recover

DOCS = [
    dict(
        id="decision",
        revision="v2",
        scope="team-a",
        current=True,
        text="Approved start: 14:00.",
    )
]


class WorkflowTests(unittest.TestCase):
    def test_transient_read_survives_checkpoint(self):
        state = initial()
        self.assertEqual(
            dispatch(state, {"action": "read", "id": "decision"}, DOCS)["error"],
            "temporary_unavailable",
        )
        state = recover(copy.deepcopy(state))
        self.assertEqual(
            dispatch(state, {"action": "read", "id": "decision"}, DOCS)["document"][
                "id"
            ],
            "decision",
        )
        self.assertEqual(state["read"], ["decision"])

    def test_denied_unknown_same_and_scope_cannot_change(self):
        docs = DOCS + [
            dict(DOCS[0], id="private", scope="team-b"),
            dict(DOCS[0], id="old", current=False),
        ]
        state = initial()
        results = [
            dispatch(state, dict(action="read", id=id), docs)
            for id in ["private", "old", "unknown"]
        ]
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])
        self.assertFalse(results[0]["retryable"])
        self.assertIn(
            "error",
            dispatch(state, dict(action="search", query="start", scope="team-b"), docs),
        )

    def test_budget_and_pending_cannot_resume(self):
        state = initial()
        reserve(state)
        with self.assertRaises(ValueError):
            recover(state)
        state["pending"] = False
        state["calls"] = state["limit"]
        with self.assertRaises(ValueError):
            reserve(state)

    def test_proposal_requires_read_and_exact_unique_quote(self):
        state = initial()
        p = dict(
            action="propose",
            target="plan.txt",
            before_sha256=state["before_sha256"],
            content="Start: 14:00\nCapacity: 20\n",
            evidence=dict(
                document_id="decision", revision="v2", quote="Approved start: 14:00."
            ),
        )
        self.assertIn("error", dispatch(state, p, DOCS))
        state["fault_used"] = True
        dispatch(state, dict(action="read", id="decision"), DOCS)
        self.assertEqual(dispatch(state, p, DOCS)["status"], "awaiting_review")
        self.assertEqual(state["resolved_evidence"]["start"], 0)
        self.assertEqual(state["phase"], "awaiting_review")

    def test_forged_approval_wrong_target_and_revision_rejected(self):
        state = initial()
        state["fault_used"] = True
        dispatch(state, dict(action="read", id="decision"), DOCS)
        p = dict(
            action="propose",
            target="plan.txt",
            before_sha256=state["before_sha256"],
            content="x",
            evidence=dict(
                document_id="decision", revision="v2", quote="Approved start: 14:00."
            ),
        )
        for bad in [
            dict(p, approved=True),
            dict(p, target="../other"),
            dict(p, before_sha256="0" * 64),
            dict(p, evidence=dict(p["evidence"], revision="v1")),
            dict(p, evidence=dict(p["evidence"], quote="invented")),
        ]:
            self.assertIn("error", dispatch(state, bad, DOCS))
        self.assertEqual(state["phase"], "running")

    def test_search_excludes_unavailable_records(self):
        state = initial()
        docs = DOCS + [
            dict(DOCS[0], id="secret", scope="team-b"),
            dict(DOCS[0], id="old", current=False),
        ]
        self.assertEqual(
            dispatch(state, dict(action="search", query="start"), docs)["documents"],
            [dict(id="decision", revision="v2")],
        )
        for action in [
            [],
            dict(action="approve"),
            dict(action="search", query=[]),
            dict(action="search", query=""),
        ]:
            self.assertIn("error", dispatch(state, action, docs))

    def test_unresolved_and_stopped_host(self):
        state = initial()
        self.assertIn(
            "error", dispatch(state, dict(action="unresolved", reason=""), DOCS)
        )
        self.assertEqual(
            dispatch(
                state, dict(action="unresolved", reason="Permission denied"), DOCS
            )["status"],
            "unresolved",
        )
        self.assertIn(
            "error", dispatch(state, dict(action="read", id="decision"), DOCS)
        )
        with self.assertRaises(ValueError):
            reserve(state)
        state = initial()
        state["calls"] = 7
        with self.assertRaises(ValueError):
            recover(state)

    def test_duplicate_quote_and_bad_evidence_rejected(self):
        state = initial()
        state["fault_used"] = True
        state["read"] = ["decision"]
        p = dict(
            action="propose",
            target="plan.txt",
            before_sha256=state["before_sha256"],
            content="x",
            evidence=dict(document_id="decision", revision="v2", quote="Approved"),
        )
        docs = [dict(DOCS[0], text="Approved Approved")]
        self.assertIn("error", dispatch(state, p, docs))
        self.assertIn(
            "error", dispatch(state, dict(p, evidence={"quote": "Approved"}), docs)
        )

    def test_integrated_scripted_review_and_apply(self):
        from review_fixture import review
        from workflow import EXPECTED

        state = initial()
        state["fault_used"] = True
        docs = [
            dict(
                DOCS[0],
                text="Approved workshop decision: change the start time to 14:00. Keep capacity at 20.",
            )
        ]
        dispatch(state, dict(action="read", id="decision"), docs)
        proposal = dict(
            action="propose",
            target="plan.txt",
            before_sha256=state["before_sha256"],
            content=EXPECTED,
            evidence=dict(document_id="decision", revision="v2", quote=docs[0]["text"]),
        )
        dispatch(state, proposal, docs)
        result = review(state)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["final_content"], EXPECTED)
        self.assertEqual(
            [
                e.get("result")
                for e in result["events"]
                if e["step"] != "scripted_approval"
            ],
            ["rejected", "rejected", "rejected", "applied", "already_applied"],
        )
        state["proposal"]["content"] = "Wrong replacement"
        self.assertFalse(review(state)["accepted"])

    def test_parser_and_request_ceiling(self):
        from run import parse, request

        for raw in ['{"action":"read","action":"approve"}', " " * 8193, "not JSON"]:
            with self.assertRaises(ValueError):
                parse(raw)
        self.assertEqual(parse('{"action":"unresolved"}'), {"action": "unresolved"})
        with self.assertRaises(ValueError):
            request(initial(), "x" * 16001)


if __name__ == "__main__":
    unittest.main()
