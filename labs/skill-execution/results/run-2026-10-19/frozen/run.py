"""Record native plugin execution and a baseline in isolated read-only Claude Code sessions."""

import argparse, hashlib, json, shutil, subprocess, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CLAIM = 'Check the claim "the longer prompt is more accurate" against labs/prompt-contract/. Inspect the saved evidence. Do not modify files or run new model trials.'


def file_hashes(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


def public_event(event):
    kind = event.get("type")
    if kind == "system" and event.get("subtype") == "init":
        return {
            k: event[k]
            for k in ["type", "subtype", "model", "tools", "skills", "plugins"]
            if k in event
        }
    if kind in ["assistant", "user"]:
        message = event.get("message", {})
        blocks = message.get("content", [])
        if not isinstance(blocks, list):
            return None
        kept = [
            block
            for block in blocks
            if isinstance(block, dict)
            and block.get("type") in ["text", "tool_use", "tool_result"]
        ]
        return {"type": kind, "content": kept} if kept else None
    if kind == "result":
        return {
            k: event[k]
            for k in [
                "type",
                "subtype",
                "is_error",
                "result",
                "duration_ms",
                "duration_api_ms",
                "num_turns",
                "total_cost_usd",
                "usage",
                "modelUsage",
                "permission_denials",
            ]
            if k in event
        }
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    frozen = a.output / "frozen"
    frozen.mkdir()
    for name in ["run.py", "PROTOCOL.md"]:
        (frozen / name).write_bytes((ROOT / name).read_bytes())
    shutil.copytree(REPO / "examples/claude-plugin", frozen / "plugin")
    shutil.copytree(
        REPO / "labs/prompt-contract",
        frozen / "evidence",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    report = {
        "cli": subprocess.check_output(["claude", "--version"], text=True).strip(),
        "model_alias": "sonnet",
        "effort": "low",
        "sha256": file_hashes(frozen),
        "runs": [],
    }
    for condition in ["baseline", "skill"]:
        with tempfile.TemporaryDirectory(
            prefix=f"prompt-guide-native-{condition}-"
        ) as cwd:
            workspace = Path(cwd)
            (workspace / "labs").mkdir()
            shutil.copytree(frozen / "evidence", workspace / "labs/prompt-contract")
            before = file_hashes(workspace / "labs")
            prompt = (
                CLAIM
                if condition == "baseline"
                else "Invoke the prompt-guide:inspect-evidence skill to perform this review. "
                + CLAIM
            )
            (a.output / f"{condition}.input.txt").write_text(prompt)
            cmd = [
                "claude",
                "-p",
                "--model",
                "sonnet",
                "--effort",
                "low",
                "--restricted",
                "--setting-sources",
                "",
                "--settings",
                '{"disableAllHooks":true}',
                "--strict-mcp-config",
                "--no-session-persistence",
                "--permission-mode",
                "dontAsk",
                "--tools",
                "Read,Glob,Grep,Skill",
                "--allowedTools",
                "Read,Glob,Grep,Skill",
                "--max-budget-usd",
                "1",
                "--output-format",
                "stream-json",
                "--verbose",
            ]
            if condition == "baseline":
                cmd += ["--disable-slash-commands"]
            else:
                shutil.copytree(frozen / "plugin", workspace / "plugin")
                cmd += ["--plugin-dir", str(workspace / "plugin")]
            cmd.append(prompt)
            start = time.monotonic()
            try:
                r = subprocess.run(
                    cmd, cwd=cwd, text=True, capture_output=True, timeout=240
                )
                status = r.returncode
                stdout = r.stdout
                stderr = r.stderr
            except subprocess.TimeoutExpired as exc:
                status = "timeout"
                stdout = (
                    (exc.stdout or b"").decode()
                    if isinstance(exc.stdout, bytes)
                    else (exc.stdout or "")
                )
                stderr = "Process timeout"
            private = Path(tempfile.mkdtemp(prefix="prompt-guide-native-private-"))
            (private / "stdout.jsonl").write_text(stdout)
            (private / "stderr.txt").write_text(stderr)
            events = []
            for line in stdout.splitlines():
                try:
                    event = public_event(json.loads(line))
                except ValueError:
                    continue
                if event is not None:
                    events.append(event)
            (a.output / f"{condition}.events.json").write_text(
                json.dumps(events, indent=2) + "\n"
            )
            final = next(
                (
                    e.get("result", "")
                    for e in reversed(events)
                    if e["type"] == "result"
                ),
                "",
            )
            (a.output / f"{condition}.output.txt").write_text(final + "\n")
            report["runs"].append(
                {
                    "condition": condition,
                    "status": status,
                    "elapsed_seconds": round(time.monotonic() - start, 3),
                    "command": cmd,
                    "evidence_before": before,
                    "evidence_after": file_hashes(workspace / "labs"),
                    "event_types": [e["type"] for e in events],
                }
            )
            (a.output / "manifest.json").write_text(json.dumps(report, indent=2) + "\n")
            print(
                condition,
                status,
                len(events),
                "public events; final response characters",
                len(final),
                flush=True,
            )


if __name__ == "__main__":
    main()
