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

    # Test for correct data
    @patch("builtins.input", side_effect=["session-analysis", "EUR", "1m", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Up: 8, Down: 11, Stable: 0", printed_args)

    # Test invalid currency value
    # @patch("builtins.input", side_effect=["session-analysis", "EU", "1m", "exit"])
    # @patch("builtins.print")
    # def test_session_analysis_flow(self, mock_print, mock_input):
    #     from main import main
    #     main()
    #
    #     printed_args = [call.args[0] for call in mock_print.call_args_list]
    #
    #     self.assertIn("Up: 8, Down: 11, Stable: 0", printed_args)

    # Test invalid period value
    @patch("builtins.input", side_effect=["session-analysis", "EUR", "1l", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid period", printed_args)

    # Test invalid command
    @patch("builtins.input", side_effect=["session-analysi","exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Unknown command. Type 'help' to see available commands.", printed_args)

    # Test statistics correct input
    @patch("builtins.input", side_effect=["statistics", "CHF","1m","exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("median: 4.5523", printed_args)
        self.assertIn("mode: 4.5919", printed_args)
        self.assertIn("std_dev: 0.022783140119048792", printed_args)
        self.assertIn("cv: 0.5", printed_args)


    # Test statistics invalid currency
    @patch("builtins.input", side_effect=["statistics", "CHF", "1m", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("median: 4.5523", printed_args)
        self.assertIn("mode: 4.5919", printed_args)
        self.assertIn("std_dev: 0.022783140119048792", printed_args)
        self.assertIn("cv: 0.5", printed_args)

    # Test statistics invalid period
    @patch("builtins.input", side_effect=["statistics", "CHF", "1a", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid period", printed_args)

    # Test change histogram invalid pair
    @patch("builtins.input", side_effect=["change-histogram", "USD", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid format. Use USD/EUR.", printed_args)

    # Test change histogram invalid date
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR","1m","p" "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid date format.", printed_args)

    # Test change histogram period
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "k", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        # Write a return error
        self.assertIn("Invalid date format.", printed_args)


class TestMainFlow(unittest.TestCase):
    @patch("builtins.input", side_effect=["list-currencies", "exit"])
    @patch("builtins.print")
    @patch("src.CurrencyManager.CurrencyManager.show_available_currencies")
    def test_main_list_currencies(self, mock_show, mock_print, mock_input):
        from main import main
        main()
        mock_show.assert_called_once()