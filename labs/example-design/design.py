"""Fixed comparison assembly; scorer reused from the first extraction pilot."""

from datetime import date
import json


def score(text, cases):
    result = {
        "schema_valid": False,
        "passed": 0,
        "total": len(cases),
        "exact": False,
        "cases": [],
    }

    def unique_object(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate JSON key")
            obj[key] = value
        return obj

    try:
        actual = json.loads(text, object_pairs_hook=unique_object)
    except (ValueError, TypeError):
        actual = None
    valid = isinstance(actual, list) and len(actual) == len(cases)
    if valid:
        for row, case in zip(actual, cases):
            if (
                not isinstance(row, dict)
                or set(row) != {"id", "owner", "deadline"}
                or row["id"] != case["id"]
                or any(
                    row[k] is not None and not isinstance(row[k], str)
                    for k in ("owner", "deadline")
                )
            ):
                valid = False
                break
            if row["deadline"] is not None:
                try:
                    valid = (
                        date.fromisoformat(row["deadline"]).isoformat()
                        == row["deadline"]
                    )
                except ValueError:
                    valid = False
                if not valid:
                    break
    result["schema_valid"] = valid
    for index, case in enumerate(cases):
        wrong = [
            k
            for k in ("owner", "deadline")
            if not valid or actual[index][k] != case["expected"][k]
        ]
        result["cases"].append(
            {
                "id": case["id"],
                "category": case["category"],
                "passed": not wrong,
                "wrong_fields": wrong,
            }
        )
    result["passed"] = sum(row["passed"] for row in result["cases"])
    result["exact"] = result["passed"] == len(cases) and valid
    return result


ARMS = ("none", "simple", "boundary", "reversed", "decomposed")


def schedule():
    return [
        {"repeat": r + 1, "arm": ARMS[(position + r) % 5]}
        for r in range(2)
        for position in range(5)
    ]


def assemble(rules, examples, cases):
    demos = [{"note": c["note"], "answer": c["expected"]} for c in examples]
    return (
        rules
        + "\nDEMONSTRATIONS\n"
        + json.dumps(demos, indent=2)
        + "\nTASK INPUT\n"
        + json.dumps([{"id": c["id"], "note": c["note"]} for c in cases], indent=2)
        + "\n"
    )
