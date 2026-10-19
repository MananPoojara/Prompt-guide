import tempfile
import unittest
from pathlib import Path
from memory import Store, Conflict


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "memory.sqlite"
        self.store = Store(self.path, "team-a")

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def put(
        self, value="Room A", expected=0, observed="2027-03-01", expires="2027-03-20"
    ):
        return self.store.put(
            "meeting-room", value, "decision-1", observed, expires, expected
        )

    def test_correction(self):
        self.put()
        self.put("Room B", 1, "2027-03-03")
        self.assertEqual(
            self.store.get("meeting-room", "2027-03-04")["value"], "Room B"
        )
        self.assertEqual(
            self.store.get("meeting-room", "2027-03-02")["value"], "Room A"
        )

    def test_stale_write_rejected(self):
        self.put()
        with self.assertRaises(Conflict):
            self.put("wrong", 0)
        self.assertEqual(len(self.store.history("meeting-room")), 1)

    def test_expired_correction_does_not_resurrect_old_value(self):
        self.put()
        self.put("Room B", 1, "2027-03-03", "2027-03-08")
        result = self.store.get("meeting-room", "2027-03-08")
        self.assertEqual(result["status"], "expired")
        self.assertIsNone(result["value"])

    def test_retraction(self):
        self.put()
        self.store.retract("meeting-room", "decision-2", "2027-03-03", 1)
        self.assertEqual(
            self.store.get("meeting-room", "2027-03-04")["status"], "retracted"
        )

    def test_namespace_isolation(self):
        self.put()
        other = Store(self.path, "team-b")
        try:
            self.assertEqual(
                other.get("meeting-room", "2027-03-04")["status"], "missing"
            )
        finally:
            other.close()

    def test_future_not_visible(self):
        self.put()
        self.assertEqual(
            self.store.get("meeting-room", "2027-02-28")["status"], "missing"
        )

    def test_persists_after_reopen(self):
        self.put()
        self.store.close()
        self.store = Store(self.path, "team-a")
        self.assertEqual(
            self.store.get("meeting-room", "2027-03-02")["value"], "Room A"
        )

    def test_bad_dates_and_backdating(self):
        with self.assertRaises(ValueError):
            self.put(observed="2027-02-30")
        with self.assertRaises(ValueError):
            self.put(expires="2027-02-28")
        self.put()
        with self.assertRaises(ValueError):
            self.put("Room B", 1, "2027-02-28")

    def test_sql_like_key_remains_data(self):
        key = "x'); DROP TABLE facts; --"
        self.store.put(key, "safe", "source", "2027-03-01", None, 0)
        self.assertEqual(self.store.get(key, "2027-03-02")["value"], "safe")
        self.put()

    def test_two_connections_cannot_overwrite_same_revision(self):
        self.put()
        other = Store(self.path, "team-a")
        try:
            other.put("meeting-room", "Room B", "source", "2027-03-03", None, 1)
            with self.assertRaises(Conflict):
                self.put("Room C", 1, "2027-03-04")
        finally:
            other.close()
