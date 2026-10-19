"""Check all saved repair requests, model outputs, and before/after judgments offline."""

import hashlib, json
from pathlib import Path
from contract import validate, check_reference

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/pilot-2026-10-19"
m = json.loads((out / "manifest.json").read_text())
for name, digest in m["sha256"].items():
    assert hashlib.sha256((out / "frozen" / name).read_bytes()).hexdigest() == digest
fixtures = json.loads((out / "frozen/fixtures.json").read_text())
assert len(m["trials"]) == len(fixtures) == 3
for f, t in zip(fixtures, m["trials"]):
    assert f["id"] == t["id"]
    assert t["status"] == 0
    errors = validate(f["candidate"], f["documents"])
    request = (
        (out / "frozen/prompt.txt").read_text()
        + "\nINPUT:\n"
        + json.dumps(
            {
                "documents": f["documents"],
                "candidate": f["candidate"],
                "validation_errors": errors,
            },
            indent=2,
        )
        + "\n"
    )
    assert (out / (f["id"] + ".input.txt")).read_text() == request
    raw = (out / (f["id"] + ".output.txt")).read_text()
    assert t["before"] == {
        "contract_errors": errors,
        "reference_match": check_reference(f["candidate"], f["expected"]),
    }
    assert t["after"] == {
        "contract_errors": validate(raw, f["documents"]),
        "reference_match": check_reference(raw, f["expected"]),
    }
    assert not t["after"]["contract_errors"] and t["after"]["reference_match"]
print(
    "Verified three retained repairs, exact requests, contract checks, and reference checks"
)
