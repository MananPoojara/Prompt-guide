import unittest
from grade import grade

class GradeTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(grade('[{"owner":null}]', [{"owner":None}])['exact'])
    def test_invented_owner(self):
        self.assertEqual(grade('[{"owner":"Alex"}]', [{"owner":None}])['passed'], 0)
    def test_extra_record(self):
        self.assertFalse(grade('[1,2]', [1])['exact'])
    def test_missing_record(self):
        self.assertFalse(grade('[]', [1])['exact'])
    def test_invalid_format(self):
        self.assertFalse(grade('```json\n[]\n```', [])['valid_json'])
    def test_wrong_type(self):
        self.assertFalse(grade('{}', [])['exact'])

if __name__ == '__main__':
    unittest.main()
