"""Authored adapter-failure fixtures; these do not call a model or measure quality."""

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
    def test_timeout_failure_and_invalid_json_retained_without_retry(self):
        calls = []
        tokenizer = types.SimpleNamespace(
            encode=lambda text, **kwargs: list(range(len(text) // 4))
        )
        loader_calls = []

        def load(*args, **kwargs):
            loader_calls.append(kwargs)
            return tokenizer

        fake_module = types.SimpleNamespace(
            AutoTokenizer=types.SimpleNamespace(from_pretrained=load)
        )

        def generate(command, **kwargs):
            calls.append(command)
            if len(calls) == 1:
                raise subprocess.TimeoutExpired(command, 180)
            if len(calls) == 2:
                return types.SimpleNamespace(returncode=7)
            destination = Path(command[command.index("--output-last-message") + 1])
            destination.write_text("not JSON")
            return types.SimpleNamespace(returncode=0)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "fixture-run"
            with (
                patch.object(
                    sys, "argv", ["run.py", "--offline", "--output", str(out)]
                ),
                patch.dict(sys.modules, {"transformers": fake_module}),
                patch("importlib.metadata.version", return_value="fixture"),
                patch.object(
                    run.subprocess, "check_output", return_value="fixture-cli"
                ),
                patch.object(run.subprocess, "run", side_effect=generate),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                run.main()
            data = json.loads((out / "manifest.json").read_text())
            evaluation = [r for r in data["rows"] if r["split"] == "evaluation"]
            self.assertEqual(len(calls), 16)
            self.assertEqual([r["status"] for r in evaluation[:2]], ["timeout", 7])
            self.assertTrue(all(not r["grade"]["passed"] for r in evaluation))
            self.assertIsNone(evaluation[0]["output_sha256"])
            self.assertIsNotNone(evaluation[2]["output_sha256"])
            self.assertTrue(loader_calls[0]["local_files_only"])
            self.assertEqual(
                len([r for r in data["rows"] if r["status"] == "not_called"]), 4
            )
            self.assertTrue(all("hidden_reasoning" not in r for r in data["rows"]))

    def test_existing_destination_refused_before_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch.object(sys, "argv", ["run.py", "--output", tmp]),
                patch.object(run.subprocess, "run") as call,
            ):
                with self.assertRaises(FileExistsError):
                    run.main()
                call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
