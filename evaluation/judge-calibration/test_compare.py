import copy
import unittest
from compare import compare


def packet():
    return dict(
        evidence_type="synthetic_fixture",
        reference_provenance=dict(type="synthetic", reviewer=None, independent=False),
        judge_provenance=dict(type="scripted", model=None, prompt_revision=None),
        rows=[
            dict(
                id="c", group="c", split="calibration", reference="pass", judge="pass"
            ),
            dict(id="a", group="a", split="test", reference="pass", judge="pass"),
            dict(id="b", group="b", split="test", reference="fail", judge="pass"),
            dict(id="d", group="d", split="test", reference="pass", judge="fail"),
            dict(id="e", group="e", split="test", reference="fail", judge="abstain"),
        ],
    )


class ComparisonTests(unittest.TestCase):
    def test_hand_computed_confusion_and_coverage(self):
        result = compare(packet())
        test = result["splits"]["test"]
        self.assertEqual(
            test["matrix"],
            {
                "pass": {"pass": 1, "fail": 1, "abstain": 0, "missing": 0},
                "fail": {"pass": 1, "fail": 0, "abstain": 1, "missing": 0},
            },
        )
        self.assertEqual(
            test["decision_coverage"], dict(numerator=3, denominator=4, value=0.75)
        )
        self.assertEqual(test["agreement_on_decided"]["numerator"], 1)
        self.assertEqual(test["false_acceptances"], ["b"])
        self.assertEqual(test["false_rejections"], ["d"])
        self.assertEqual(test["judge_abstentions"], ["e"])
        self.assertEqual(result["evidence_status"], "synthetic demonstration only")

    def test_missing_and_uncertain_never_agreements(self):
        data = packet()
        data["rows"].extend(
            [
                dict(
                    id="u",
                    group="u",
                    split="test",
                    reference="unreviewed",
                    judge="pass",
                ),
                dict(
                    id="v", group="v", split="test", reference="uncertain", judge="fail"
                ),
            ]
        )
        result = compare(data)["splits"]["test"]
        self.assertEqual(result["reference_coverage"]["value"], 4 / 6)
        self.assertEqual(result["decision_coverage"]["denominator"], 4)
        self.assertEqual(result["excluded_reference"], ["u", "v"])

    def test_zero_denominator_is_null(self):
        data = packet()
        data["rows"] = []
        test = compare(data)["splits"]["test"]
        self.assertIsNone(test["agreement_on_decided"]["value"])
        self.assertIsNone(test["decision_coverage"]["value"])

    def test_group_leakage_and_duplicates_rejected(self):
        data = packet()
        data["rows"][1]["group"] = "c"
        with self.assertRaises(ValueError):
            compare(data)
        data = packet()
        data["rows"].append(copy.deepcopy(data["rows"][1]))
        with self.assertRaises(ValueError):
            compare(data)

    def test_bad_verdict_and_missing_field_rejected(self):
        data = packet()
        data["rows"][0]["judge"] = "PASS"
        with self.assertRaises(ValueError):
            compare(data)
        data = packet()
        del data["rows"][0]["reference"]
        with self.assertRaises(ValueError):
            compare(data)

    def test_metadata_does_not_certify_independence(self):
        data = packet()
        data["evidence_type"] = "submitted_comparison"
        data["reference_provenance"] = dict(
            type="human", reviewer="reviewer-1", independent=True
        )
        data["judge_provenance"] = dict(
            type="model", model="declared-model", prompt_revision="v1"
        )
        result = compare(data)
        self.assertIn("self-reported", result["evidence_status"])
        self.assertFalse(result["independent_review_verified"])
        self.assertFalse(result["calibration_certified"])

    def test_missing_judge_is_not_an_abstention(self):
        data = packet()
        data["rows"][-1]["judge"] = "missing"
        test = compare(data)["splits"]["test"]
        self.assertEqual(test["missing_judgments"], ["e"])
        self.assertEqual(test["judge_abstentions"], [])
        self.assertEqual(test["decision_coverage"]["value"], 0.75)

    def test_bad_provenance_rejected(self):
        for mutate in [
            lambda d: d.update(evidence_type="unknown"),
            lambda d: d.update(rows={}),
            lambda d: d.update(reference_provenance={}),
            lambda d: d["reference_provenance"].update(reviewer=""),
            lambda d: d["reference_provenance"].update(type="human"),
            lambda d: d.update(judge_provenance={}),
            lambda d: d["judge_provenance"].update(type="model"),
            lambda d: d["reference_provenance"].update(independent=True),
            lambda d: d["rows"][0].update(id=""),
        ]:
            data = packet()
            mutate(data)
            with self.assertRaises(ValueError):
                compare(data)
        with self.assertRaises(ValueError):
            compare([])


if __name__ == "__main__":
    unittest.main()
