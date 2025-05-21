import unittest
import re
from unittest.mock import patch, MagicMock
from src.CurrencyManager import CurrencyManager
from datetime import datetime


class TestCurrencyManager(unittest.TestCase):

    def setUp(self):
        self.cm = CurrencyManager()

    # Checking available currencies
    @patch("builtins.print")
    def test_show_available_currencies(self, mock_print):
        self.cm.show_available_currencies()

        expected_calls = [
            unittest.mock.call("Available currencies:"),
            unittest.mock.call("-", "USD"),
            unittest.mock.call("-", "EUR"),
            unittest.mock.call("-", "CHF"),
            unittest.mock.call("-", "GBP"),
            unittest.mock.call("-", "JPY"),
            unittest.mock.call("-", "NOK"),
            unittest.mock.call("-", "SEK"),
        ]

        for call in expected_calls:
            self.assertIn(call, mock_print.mock_calls)

    # Test fetch data
    @patch("builtins.print")
    @patch("builtins.input", side_effect=[
        "fetch-data",
        "USD",
        "2024-01-02",
        "2024-01-04",
        "exit"
    ])
    def test_fetch_real_data_3days(self, mock_input, mock_print):
        from main import main
        main()

        expected = [
            ('2024-01-02', 3.9432),
            ('2024-01-03', 3.9909),
            ('2024-01-04', 3.9684)
        ]

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        filtered = [
            arg for arg in printed_args
            if isinstance(arg, tuple)
               and len(arg) == 2
               and isinstance(arg[0], str)
               and re.match(r"\d{4}-\d{2}-\d{2}", arg[0])
               and isinstance(arg[1], float)
        ]

        self.assertEqual(len(filtered), len(expected))

        for exp, act in zip(expected, filtered):
            self.assertEqual(exp[0], act[0])
            self.assertAlmostEqual(exp[1], act[1], places=4)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=[
        "fetch-data",
        "USD",
        "invalid-date",  # Invalid start date
        "2024-01-05",
        "exit"
    ])
    def test_invalid_date_error_message_printed(self, mock_input, mock_print):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid start date or end date", printed_args)


    @patch("builtins.print")
    @patch("builtins.input", side_effect=[
        "export",
        "csv",
        "USD",
        "2020-01-01",
        "2020-01-10",
        "exit"
    ])
    def test_valid_csv_export(self, mock_input, mock_print):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Data exported to output.csv", printed_args)

        results = [
            ('Date', 'Exchange Rate'),
            ('2020-01-02', 3.8),
            ('2020-01-03', 3.8213),
            ('2020-01-07', 3.7861),
            ('2020-01-08', 3.8123),
            ('2020-01-09', 3.8251),
            ('2020-01-10', 3.8272)]

        with open("output.csv", "r") as file:
            first_line = file.readline().strip()
            self.assertEqual(first_line, ",".join(results[0]))

            for i, line in enumerate(file):
                with self.subTest(i=i):
                    expected = ",".join(map(str,results[i+1]))
                    self.assertEqual(line.rstrip("\n"), expected)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=[
        "export",
        "wrongInput",
        "exit"
    ])
    def test_invalid_export_type(self, mock_input, mock_print):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Unsupported export format.", printed_args)

class TestMainFlow(unittest.TestCase):
    @patch("builtins.input", side_effect=["list-currencies", "exit"])
    @patch("builtins.print")
    @patch("src.CurrencyManager.CurrencyManager.show_available_currencies")
    def test_main_list_currencies(self, mock_show, mock_print, mock_input):
        from main import main
        main()
        mock_show.assert_called_once()
