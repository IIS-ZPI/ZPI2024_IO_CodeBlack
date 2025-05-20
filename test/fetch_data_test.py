import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.CurrencyManager import CurrencyManager

class TestCurrencyManager(unittest.TestCase):
    def test_fetch_data_returns_data(self):
        cm = CurrencyManager()
        data = cm.fetch_data('USD', '2023-01-01', '2023-01-10')

        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(len(data), 6, "Expected 6 data points for the date range")
        for i, entry in enumerate(data):
            with self.subTest(i=i):
                self.assertIsInstance(entry, tuple, f"Entry {i} is not a tuple")
        self.assertEqual(len(data[0]), 2, "Expected tuple to have exactly 2 elements")
        self.assertIsInstance(data[0][0], str, "Expected first element of tuple to be a string (date)")
        self.assertIsInstance(data[0][1], (float, int),"Expected second element of tuple to be a number (exchange rate)")

    def test_fetch_data_invalid_currency(self):
        cm = CurrencyManager()
        data = cm.fetch_data('U5D', '2023-01-01', '2023-01-10')

        self.assertIsInstance(data, list, "Expected result to be a list")
        # For an invalid currency code, the returned list should be empty
        self.assertEqual(data, [], "Expected empty list for invalid currency code")

    def test_fetch_data_invalid_dates(self):
        cm = CurrencyManager()

        # Test with invalid start date format
        data = cm.fetch_data('USD', '2023-13-01', '2023-01-10')
        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(data, [], "Expected empty list for invalid start date format")

        # Test with end date earlier than start date
        data = cm.fetch_data('USD', '2023-01-10', '2023-01-01')
        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(data, [], "Expected empty list when end date is before start date")


if __name__ == '__main__':
    unittest.main()
