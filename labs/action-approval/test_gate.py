import tempfile, unittest
from pathlib import Path
from gate import Gate, Rejected, sha


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "plan.txt").write_text("old\n")
        self.gate = Gate(self.root)
        self.proposal = {
            "target": "plan.txt",
            "before_sha256": sha(b"old\n"),
            "content": "new\n",
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_unapproved_blocked(self):
        with self.assertRaises(Rejected):
            self.gate.apply(self.proposal)
        self.assertEqual((self.root / "plan.txt").read_text(), "old\n")

    def test_exact_approved_apply_and_replay(self):
        self.gate.approve(self.proposal)
        self.assertEqual(self.gate.apply(self.proposal), "applied")
        self.assertEqual(self.gate.apply(self.proposal), "already_applied")

    def test_mutation_invalidates_approval(self):
        self.gate.approve(self.proposal)
        self.proposal["content"] = "tampered"
        with self.assertRaises(Rejected):
            self.gate.apply(self.proposal)

    def test_stale_target_rejected(self):
        self.gate.approve(self.proposal)
        (self.root / "plan.txt").write_text("someone else changed it")
        with self.assertRaises(Rejected):
            self.gate.apply(self.proposal)

    def test_path_and_extra_approval_fields_rejected(self):
        for value in ["../plan.txt", "/tmp/plan.txt", "other.txt"]:
            with self.assertRaises(Rejected):
                self.gate.approve({**self.proposal, "target": value})
        with self.assertRaises(Rejected):
            self.gate.approve({**self.proposal, "approved": True})

    def test_symlink_rejected(self):
        (self.root / "plan.txt").unlink()
        (self.root / "other.txt").write_text("old\n")
        (self.root / "plan.txt").symlink_to(self.root / "other.txt")
        self.gate.approve(self.proposal)
        with self.assertRaises(Rejected):
            self.gate.apply(self.proposal)

    def test_invalid_payloads(self):
        for value in [
            None,
            [],
            {},
            {**self.proposal, "content": 3},
            {**self.proposal, "before_sha256": "bad"},
        ]:
            with self.assertRaises(Rejected):
                self.gate.approve(value)


class ParsingTests(unittest.TestCase):
    def test_duplicate_keys_rejected_before_review(self):
        from gate import parse_proposal

        with self.assertRaises(Rejected):
            parse_proposal('{"target":"plan.txt","target":"other.txt"}')

    def test_non_json_rejected(self):
        from gate import parse_proposal

        with self.assertRaises(Rejected):
            parse_proposal("not JSON")
