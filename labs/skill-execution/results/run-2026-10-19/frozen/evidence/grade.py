"""Re-score saved outputs without any model calls or external dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def grade(text, expected):
    try:
        actual = json.loads(text)
    except json.JSONDecodeError:
        return {"valid_json": False, "passed": 0, "total": len(expected), "exact": False}
    if not isinstance(actual, list):
        return {"valid_json": True, "passed": 0, "total": len(expected), "exact": False}
    return {"valid_json": True,
            "passed": sum(a == b for a, b in zip(actual, expected)),
            "total": len(expected), "exact": actual == expected}

if __name__ == '__main__':
    expected = json.loads((ROOT / 'expected.json').read_text())
    results = {name: grade((ROOT / 'results' / (name + '.txt')).read_text(), expected)
               for name in ('baseline', 'candidate')}
    print(json.dumps(results, indent=2))
    raise SystemExit(0 if all(r['exact'] for r in results.values()) else 1)
