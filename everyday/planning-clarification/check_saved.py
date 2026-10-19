"""Check exact recording integrity and reconstructed conversation, not answer meaning."""

import hashlib, json
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / "results/run-2026-10-19"
frozen = out / "frozen"
data = json.loads((out / "manifest.json").read_text())
for name, digest in data["sha256"].items():
    assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == digest, name
planning = (
    (frozen / "planning.prompt.txt").read_text()
    + "\nSUPPLIED FACTS\n"
    + (frozen / "planning.input.txt").read_text()
)
question = (
    (frozen / "clarification.prompt.txt").read_text()
    + "\nREQUEST\n"
    + (frozen / "clarification.input.txt").read_text()
)
assert [c["name"] for c in data["calls"]] == ["planning", "question", "followup"]
expected = {
    "planning": planning,
    "question": question,
    "followup": "Continue this scripted conversation. Answer the latest user reply. Do not use tools.\n\nUSER\n"
    + question
    + "\nASSISTANT\n"
    + (out / "question.output.txt").read_text()
    + "\nUSER\n"
    + (frozen / "user-reply.txt").read_text(),
}
for call in data["calls"]:
    name = call["name"]
    request = (out / f"{name}.input.txt").read_bytes()
    answer = (out / f"{name}.output.txt").read_bytes()
    assert call["status"] == 0
    assert request.decode() == expected[name]
    assert hashlib.sha256(request).hexdigest() == call["input_sha256"]
    assert hashlib.sha256(answer).hexdigest() == call["output_sha256"]
for filename, response_names in [
    ("planning.md", ["planning"]),
    ("clarification.md", ["question", "followup"]),
]:
    page = (root / filename).read_text()
    for name in response_names:
        quoted = "\n".join(
            ("> " + line if line else ">")
            for line in (out / f"{name}.output.txt").read_text().splitlines()
        )
        assert quoted in page, f"Recorded response changed in {filename}"
print(
    "Verified three recorded responses and exact scripted conversation; semantic review is documented separately"
)
