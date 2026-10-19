import unittest
from search import search_products

class SearchTests(unittest.TestCase):
    def setUp(self):
        self.products = ['Desk Lamp', 'lamp shade', 'Chair']
    def test_normalized_query(self):
        self.assertEqual(search_products(self.products, '  LAMP '), self.products[:2])
    def test_order(self):
        self.assertEqual(search_products(self.products, 'lamp'), self.products[:2])
    def test_unknown(self):
        self.assertEqual(search_products(self.products, 'sofa'), [])
    def test_empty(self):
        self.assertEqual(search_products(self.products, ''), self.products)
    def test_whitespace(self):
        self.assertEqual(search_products(self.products, '   '), self.products)

if __name__ == '__main__':
    unittest.main()
