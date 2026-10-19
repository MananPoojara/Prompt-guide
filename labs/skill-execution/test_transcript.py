import unittest
from run import public_event


class TranscriptTests(unittest.TestCase):
    def test_initialization_omits_account_and_session_fields(self):
        result = public_event(
            {
                "type": "system",
                "subtype": "init",
                "model": "test",
                "skills": ["a"],
                "session_id": "private",
                "email": "private",
                "apiKey": "private",
            }
        )
        self.assertEqual(
            result,
            {"type": "system", "subtype": "init", "model": "test", "skills": ["a"]},
        )

    def test_reasoning_and_signatures_not_published(self):
        result = public_event(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "thinking",
                            "thinking": "private",
                            "signature": "private",
                        },
                        {"type": "text", "text": "public"},
                    ]
                },
            }
        )
        self.assertEqual(
            result,
            {"type": "assistant", "content": [{"type": "text", "text": "public"}]},
        )

    def test_tool_evidence_retained(self):
        block = {
            "type": "tool_use",
            "id": "tool-1",
            "name": "Skill",
            "input": {"skill": "prompt-guide:inspect-evidence"},
        }
        self.assertEqual(
            public_event({"type": "assistant", "message": {"content": [block]}})[
                "content"
            ],
            [block],
        )

    def test_unknown_event_omitted(self):
        self.assertIsNone(public_event({"type": "account", "token": "private"}))

    def test_result_keeps_accounting_not_identity(self):
        result = public_event(
            {
                "type": "result",
                "result": "answer",
                "total_cost_usd": 0.1,
                "email": "private",
            }
        )
        self.assertEqual(
            result, {"type": "result", "result": "answer", "total_cost_usd": 0.1}
        )
