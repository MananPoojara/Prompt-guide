import unittest
from design import assemble, schedule, score


class DesignTests(unittest.TestCase):
    def test_order_changes_only_demonstration_order(self):
        examples = [
            {"id": "d1", "note": "first", "expected": {"owner": "A", "deadline": None}},
            {
                "id": "d2",
                "note": "second",
                "expected": {"owner": None, "deadline": None},
            },
        ]
        cases = [
            {
                "id": "e1",
                "note": "input",
                "expected": {"owner": "SECRET", "deadline": None},
                "rationale": "SECRET",
            }
        ]
        a = assemble("RULES", examples, cases)
        b = assemble("RULES", list(reversed(examples)), cases)
        self.assertNotEqual(a, b)
        self.assertNotIn("SECRET", a)
        self.assertEqual(a.split("TASK INPUT\n")[1], b.split("TASK INPUT\n")[1])
        self.assertEqual(a.count("first"), 1)

    def test_schedule_fixed_two_repetitions(self):
        rows = schedule()
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0], {"repeat": 1, "arm": "none"})
        for repeat in [1, 2]:
            self.assertEqual(len({r["arm"] for r in rows if r["repeat"] == repeat}), 5)

    def test_grade_rejects_duplicates_invalid_dates_and_wrong_ids(self):
        cases = [
            {
                "id": "e",
                "category": "test",
                "expected": {"owner": "A", "deadline": None},
            }
        ]
        for raw in [
            '[{"id":"e","owner":"A","owner":"B","deadline":null}]',
            '[{"id":"e","owner":"A","deadline":"2026-02-30"}]',
            '[{"id":"x","owner":"A","deadline":null}]',
        ]:
            self.assertFalse(score(raw, cases)["schema_valid"])

    def test_valid_value_error_is_not_schema_error(self):
        cases = [
            {
                "id": "e",
                "category": "test",
                "expected": {"owner": "A", "deadline": None},
            }
        ]
        result = score('[{"id":"e","owner":"B","deadline":null}]', cases)
        self.assertTrue(result["schema_valid"])
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["cases"][0]["wrong_fields"], ["owner"])


class MoreScoreTests(unittest.TestCase):
    def test_exact_and_bad_batches(self):
        import json

        cases = [
            {
                "id": "e",
                "category": "test",
                "expected": {"owner": None, "deadline": "2027-01-01"},
            }
        ]
        valid = [{"id": "e", "owner": None, "deadline": "2027-01-01"}]
        self.assertTrue(score(json.dumps(valid), cases)["exact"])
        for value in [
            None,
            [],
            [{"id": "e", "owner": 7, "deadline": None}],
            [{"id": "e", "owner": None, "deadline": "20270101"}],
            [{"id": "e", "owner": None, "deadline": None, "extra": 1}],
        ]:
            self.assertFalse(score(json.dumps(value), cases)["schema_valid"])
        self.assertFalse(score("not json", cases)["schema_valid"])


if __name__ == "__main__":
    unittest.main()
