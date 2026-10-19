import unittest
from source_watch import inspect


class WatchTests(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(
            inspect({"repository": "a/b", "commit": "abc"}, lambda r: "abc")["status"],
            "unchanged",
        )

    def test_changed(self):
        self.assertEqual(
            inspect({"repository": "a/b", "commit": "abc"}, lambda r: "def")["status"],
            "review_needed",
        )

    def test_failure_is_not_unchanged(self):
        def fail(r):
            raise RuntimeError("network unavailable")

        self.assertEqual(
            inspect({"repository": "a/b", "commit": "abc"}, fail)["status"], "error"
        )


class SourceListTests(unittest.TestCase):
    def test_merge_keeps_scope_and_rejects_duplicates(self):
        from source_watch import source_list

        source = {
            "repository": "owner/project",
            "commit": "a" * 40,
            "watch_scope": "README baseline",
        }
        self.assertEqual(source_list([source], []), [source])
        with self.assertRaises(ValueError):
            source_list([source], [source])

    def test_invalid_repository_or_revision_rejected(self):
        from source_watch import source_list

        for repository, commit in [
            ("bad/repo/extra", "a" * 40),
            ("owner/repo", "HEAD"),
            ("../repo", "a" * 40),
        ]:
            with self.assertRaises(ValueError):
                source_list([], [{"repository": repository, "commit": commit}])
