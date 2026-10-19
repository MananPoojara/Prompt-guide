"""Adapter failure fixtures only; no hosted model calls."""

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import run


class RunnerTests(unittest.TestCase):
    def invoke(self, out, generate, resume=False):
        args = ["run.py", "--output", str(out)] + (["--resume"] if resume else [])
        with (
            patch.object(sys, "argv", args),
            patch.object(run.subprocess, "check_output", return_value="fixture-cli"),
            patch.object(run.subprocess, "run", side_effect=generate),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            run.main()

    def test_timeout_stops_without_retry(self):
        calls = []

        def generate(command, **kwargs):
            calls.append(command)
            raise subprocess.TimeoutExpired(command, 180)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            self.invoke(out, generate)
            state = json.loads((out / "state.json").read_text())
            self.assertEqual(len(calls), 1)
            self.assertEqual(state["phase"], "process_failed")
            self.assertFalse(state["pending"])
            self.assertEqual(state["runs"][0]["status"], "timeout")

    def test_invalid_responses_consume_budget(self):
        calls = []

        def generate(command, **kwargs):
            calls.append(command)
            Path(command[command.index("--output-last-message") + 1]).write_text(
                "not JSON"
            )
            return types.SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            self.invoke(out, generate)
            state = json.loads((out / "state.json").read_text())
            self.assertEqual(len(calls), 6)
            self.assertEqual(state["phase"], "budget_exhausted")
            self.assertTrue(
                all(h["result"]["error"] == "invalid_json" for h in state["history"])
            )
            with self.assertRaises(FileExistsError):
                self.invoke(out, generate)

    def test_changed_checkpoint_sources_refuse_resume(self):
        def generate(command, **kwargs):
            Path(command[command.index("--output-last-message") + 1]).write_text(
                '{"action":"read","id":"decision"}'
            )
            return types.SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            self.invoke(out, generate)
            self.assertTrue((out / "pause-state.json").exists())
            (out / "frozen/prompt.txt").write_text("changed")
            with self.assertRaises(ValueError):
                self.invoke(out, generate, True)

    def test_oversized_request_stops_before_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            with patch.object(run, "request", side_effect=ValueError("overflow")):
                self.invoke(out, lambda *a, **kw: self.fail("Unexpected model call"))
            self.assertEqual(
                json.loads((out / "state.json").read_text())["phase"], "input_limit"
            )


if __name__ == "__main__":
    unittest.main()
