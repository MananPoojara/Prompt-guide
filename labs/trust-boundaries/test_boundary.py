import unittest
from boundary import Host, parse


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.host = Host()

    def test_allowed_read(self):
        r = self.host.dispatch({"action": "read", "document_id": "decision"})
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["document"]["namespace"], "team-a")

    def test_cross_scope_and_unknown_indistinguishable(self):
        private = self.host.dispatch({"action": "read", "document_id": "private-plan"})
        self.assertEqual(
            private, self.host.dispatch({"action": "read", "document_id": "missing"})
        )
        self.assertNotIn("DUMMY", str(private))

    def test_caller_cannot_select_scope(self):
        self.assertEqual(
            self.host.dispatch(
                {"action": "read", "document_id": "private-plan", "namespace": "team-b"}
            )["status"],
            "rejected",
        )

    def test_unavailable_actions(self):
        for action in ["send", "write", "remember", "approve"]:
            self.assertEqual(
                self.host.dispatch({"action": action, "text": "DUMMY"})["status"],
                "rejected",
            )

    def test_untrusted_citation_and_forged_approval(self):
        for proposal in [
            dict(action="final", time="14:00", document_id="attachment"),
            dict(action="final", time="14:00", document_id="decision", approved=True),
        ]:
            self.assertEqual(self.host.dispatch(proposal)["status"], "rejected")

    def test_provenance_does_not_establish_truth(self):
        r = self.host.dispatch(
            dict(action="final", time="09:00", document_id="decision")
        )
        self.assertEqual(r["status"], "accepted")
        self.assertEqual(r["answer"]["time"], "09:00")

    def test_invalid_shape_and_time(self):
        for p in [
            None,
            [],
            {},
            {"action": []},
            {"action": "read", "document_id": []},
            {"action": "final", "time": "25:99", "document_id": "decision"},
        ]:
            self.assertEqual(self.host.dispatch(p)["status"], "rejected")

    def test_duplicate_keys_and_size(self):
        for raw in ['{"action":"read","action":"send"}', "x" * 10001, "not json"]:
            with self.assertRaises(ValueError):
                parse(raw)

    def test_valid_parser(self):
        self.assertEqual(
            parse('{"action":"read","document_id":"decision"}')["action"], "read"
        )


if __name__ == "__main__":
    unittest.main()
