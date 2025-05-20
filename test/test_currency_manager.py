import sys
import os
import unittest
from datetime import datetime, timedelta
from unittest.mock import mock_open
from io import StringIO
from unittest.mock import patch
from contextlib import redirect_stdout
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.CurrencyManager import CurrencyManager

class TestCurrencyManager(unittest.TestCase):
    def setUp(self):
        self.today = datetime.today().replace(microsecond=0)
        self.delta = timedelta(seconds=5)
        self.cm = CurrencyManager()

    def test_show_help_output(self):
        buffer = StringIO()

        with redirect_stdout(buffer):
            self.cm.show_help()

        output = buffer.getvalue()

        self.assertIn("Available commands:", output)
        self.assertIn("fetch-data", output)
        self.assertIn("list-currencies", output)
        self.assertIn("help", output)
        self.assertIn("export csv", output)

    def test_show_available_currencies_output(self):
        expected_output = "Available currencies:\n- USD\n- EUR\n- CHF\n- GBP\n- JPY\n- NOK\n- SEK\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.cm.show_available_currencies()
            assert fake_out.getvalue() == expected_output

    def test_export_to_csv(self):
        data = [["2023-01-01", 4.5], ["2023-01-02", 4.6]]
        mock_file = mock_open()

        with patch("builtins.open", mock_file), \
             patch("csv.writer") as mock_writer_class, \
             patch("builtins.print") as mock_print:

            mock_writer = mock_writer_class.return_value
            self.cm.export_to_csv(data, "test.csv")

            mock_file.assert_called_once_with("test.csv", mode='w', newline='')

            mock_writer.writerow.assert_called_once_with(["Date", "Exchange Rate"])
            mock_writer.writerows.assert_called_once_with(data)

            mock_print.assert_called_once_with("Data exported to test.csv")

    def compare_dates(self, result_start, result_end, expected_start, expected_end):
        self.assertAlmostEqual(result_start.timestamp(), expected_start.timestamp(), delta=self.delta.total_seconds())
        self.assertAlmostEqual(result_end.timestamp(), expected_end.timestamp(), delta=self.delta.total_seconds())

    def test_1w(self):
        expected_start = self.today - timedelta(weeks=1)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("1w")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_2w(self):
        expected_start = self.today - timedelta(weeks=2)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("2w")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_1m(self):
        expected_start = self.today - timedelta(days=30)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("1m")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_1q(self):
        expected_start = self.today - timedelta(days=90)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("1q")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_6m(self):
        expected_start = self.today - timedelta(days=180)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("6m")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_1y(self):
        expected_start = self.today - timedelta(days=365)
        expected_end = self.today
        result_start, result_end = self.cm.get_period_dates("1y")
        self.compare_dates(result_start, result_end, expected_start, expected_end)

    def test_invalid_period(self):
        with self.assertRaises(ValueError):
            self.cm.get_period_dates("invalid")

    def test_all_up(self):
        data = [(1, 100), (2, 105), (3, 110)]
        expected = {"up": 2, "down": 0, "stable": 0}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_all_down(self):
        data = [(1, 100), (2, 95), (3, 90)]
        expected = {"up": 0, "down": 2, "stable": 0}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_all_stable(self):
        data = [(1, 100), (2, 100), (3, 100)]
        expected = {"up": 0, "down": 0, "stable": 2}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_mixed_trends(self):
        data = [(1, 100), (2, 105), (3, 105), (4, 100)]
        expected = {"up": 1, "down": 1, "stable": 1}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_single_element(self):
        data = [(1, 100)]
        expected = {"up": 0, "down": 0, "stable": 0}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_empty_data(self):
        data = []
        expected = {"up": 0, "down": 0, "stable": 0}
        self.assertEqual(self.cm.session_analysis(data), expected)

    def test_fetch_data_returns_data(self):
        data = self.cm.fetch_data('USD', '2023-01-01', '2023-01-10')

        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(len(data), 6, "Expected 6 data points for the date range")
        for i, entry in enumerate(data):
            with self.subTest(i=i):
                self.assertIsInstance(entry, tuple, f"Entry {i} is not a tuple")
        self.assertEqual(len(data[0]), 2, "Expected tuple to have exactly 2 elements")
        self.assertIsInstance(data[0][0], str, "Expected first element of tuple to be a string (date)")
        self.assertIsInstance(data[0][1], (float, int),"Expected second element of tuple to be a number (exchange rate)")

        data = self.cm.fetch_data('USD', '2020-01-01', '2023-01-10')
        self.assertEqual(len(data), 767, f"Expected 767 record. Got: {len(data)}")


    def test_fetch_data_invalid_currency(self):
        data = self.cm.fetch_data('U5D', '2023-01-01', '2023-01-10')

        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(data, [], "Expected empty list for invalid currency code")

    def test_fetch_data_invalid_dates(self):

        # Test with invalid start date format
        with self.assertRaises(ValueError):
            self.cm.fetch_data('USD', '2023-13-01', '2023-01-10')

        # Test with end date earlier than start date
        data = self.cm.fetch_data('USD', '2023-01-10', '2023-01-01')
        self.assertIsInstance(data, list, "Expected result to be a list")
        self.assertEqual(data, [], "Expected empty list when end date is before start date")


    def test_compute_statistics_typical_data(self):
        data = [("2023-01-01", 11), ("2023-01-02", 12), ("2023-01-03", 14), ("2023-01-04", 12)]
        result = self.cm.compute_statistics(data)
        self.assertEqual(result["median"], 12)
        self.assertEqual(result["mode"], 12)
        self.assertGreater(result["std_dev"], 0)
        self.assertGreater(result["cv"], 0)

    def test_compute_statistics_single_element(self):
        data = [("2023-01-01", 10)]
        result = self.cm.compute_statistics(data)
        self.assertEqual(result, {})

    def test_compute_statistics_empty_data(self):
        data = []
        result = self.cm.compute_statistics(data)
        self.assertEqual(result, {})

    def test_compute_statistics_all_equal(self):
        data = [("2023-01-01", 5), ("2023-01-02", 5), ("2023-01-03", 5)]
        result = self.cm.compute_statistics(data)
        self.assertEqual(result["median"], 5)
        self.assertEqual(result["mode"], 5)
        self.assertEqual(result["std_dev"], 0)
        self.assertEqual(result["cv"], 0)

    def test_compute_statistics_float_values(self):
        data = [("2023-01-01", 4.5), ("2023-01-02", 5.5), ("2023-01-03", 6.5)]
        result = self.cm.compute_statistics(data)
        self.assertAlmostEqual(result["median"], 5.5)
        self.assertEqual(result["mode"], 4.5)
        self.assertAlmostEqual(result["std_dev"], 1.0)
        self.assertGreater(result["cv"], 0)
        
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.show")
    def test_generate_histogram(self, mock_show, mock_savefig):
        data = [("2023-01-01", 4.5), ("2023-01-02", 4.6), ("2023-01-03", 4.7)]
        self.cm.generate_histogram(data, title="Test Histogram")

        mock_savefig.assert_called_once_with("histogram.png")
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
