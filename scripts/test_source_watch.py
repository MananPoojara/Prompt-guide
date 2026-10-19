import unittest
from source_watch import inspect
class WatchTests(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(inspect({'repository':'a/b','commit':'abc'},lambda r:'abc')['status'],'unchanged')
    def test_changed(self):
        self.assertEqual(inspect({'repository':'a/b','commit':'abc'},lambda r:'def')['status'],'review_needed')
    def test_failure_is_not_unchanged(self):
        def fail(r):raise RuntimeError('network unavailable')
        self.assertEqual(inspect({'repository':'a/b','commit':'abc'},fail)['status'],'error')
