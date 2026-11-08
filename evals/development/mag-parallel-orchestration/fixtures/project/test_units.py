import unittest
from pricing import amount_due
from security import can_read


class UnitTests(unittest.TestCase):
    def test_floor(self):
        self.assertEqual(amount_due(101, 5), 106)

    def test_owner(self):
        self.assertTrue(can_read(True, False))
