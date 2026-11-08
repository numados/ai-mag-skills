import unittest
from report import invoice_total


class IntegrationTests(unittest.TestCase):
    def test_numeric_total(self):
        self.assertEqual(invoice_total(101, 5), 106)
