"""Read upstream commit IDs; produce a review queue, never publish advice."""

import argparse, datetime, json, os, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_list(toolkit, additional):
    sources = toolkit + additional
    seen = set()
    for source in sources:
        repo, revision = source["repository"], source["commit"]
        if not re.fullmatch(
            r"[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+", repo
        ) or not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Invalid repository or pinned revision")
        if repo in seen:
            raise ValueError("Duplicate watched repository")
        seen.add(repo)
    return sources


def inspect(source, fetch):
    row = {
        "repository": source["repository"],
        "inspected_commit": source["commit"],
        "watch_scope": source.get(
            "watch_scope",
            "Toolkit source baseline; HEAD changes require content review",
        ),
    }
    try:
        row["current_commit"] = fetch(source["repository"])
        row["status"] = (
            "unchanged"
            if row["current_commit"] == source["commit"]
            else "review_needed"
        )
    except (RuntimeError, subprocess.SubprocessError) as exc:
        row["status"] = "error"
        row["error"] = type(exc).__name__
    return row


def fetch(repo):
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/commits/HEAD", "--jq", ".sha"],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    sha = result.stdout.strip()
    if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise RuntimeError("Invalid revision")
    return sha


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    sources = source_list(
        json.loads((ROOT / "toolkit/sources.json").read_text()),
        json.loads((ROOT / "research/watch-sources.json").read_text()),
    )
    rows = [inspect(s, fetch) for s in sources]
    report = {
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": f"{len(sources)} configured primary/toolkit repositories; HEAD changes only, no automatic content review",
        "sources": rows,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    text = "# Upstream source review queue\n\nHEAD changes are review candidates, not evidence that guidance is wrong. Coverage is limited to the configured toolkit and primary-source repositories; no website or paper-feed monitoring.\n\n| Repository | Status | Baseline | Current | Review scope |\n|---|---|---|---|---|\n"
    for r in rows:
        text += f"| {r['repository']} | {r['status']} | {r['inspected_commit'][:12]} | {r.get('current_commit', 'unavailable')[:12]} | {r['watch_scope']} |\n"
    (args.output / "report.md").write_text(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
            stream.write(text)
    print(text)
    return int(any(r["status"] == "error" for r in rows))


if __name__ == "__main__":
    raise SystemExit(main())
