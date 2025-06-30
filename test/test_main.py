import unittest
import re
from unittest.mock import patch, MagicMock
from src.CurrencyManager import CurrencyManager

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


    # Test for correct data
    @patch("builtins.input", side_effect=["session-analysis", "EUR", "1m", "exit"])
    @patch("builtins.print")
    def test_session_analysis_flow(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        pattern = r"Up:\s*\d+,\s*Down:\s*\d+,\s*Stable:\s*\d+"
        self.assertTrue(any(re.search(pattern, arg) for arg in printed_args))

    # Test invalid currency value
    @patch("builtins.input", side_effect=["session-analysis", "EU","EUR", "1m", "exit"])
    @patch("builtins.print")
    def test_session_invalid_currency(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args for call in mock_print.call_args_list]

        expected_lines = [
            ("Invalid currency.",),
            ("Available currencies:",),
            ("-", "USD"),
            ("-", "EUR"),
            ("-" ,"CHF"),
            ("-" ,"GBP"),
            ("-" ,"JPY"),
            ("-" ,"NOK"),
            ("-" ,"SEK"),
        ]

        for line in expected_lines:
            self.assertIn(line, printed_args)

    # Test invalid period value
    @patch("builtins.input", side_effect=["session-analysis", "EUR", "1l","1m", "exit"])
    @patch("builtins.print")
    def test_session_analysis_invalid_period(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid period. Valid options: 1w, 2w, 1m, 1q, 6m, 1y", printed_args)
        pattern = r"Up:\s*\d+,\s*Down:\s*\d+,\s*Stable:\s*\d+"
        self.assertTrue(any(re.search(pattern, arg) for arg in printed_args))

    # Test invalid command
    @patch("builtins.input", side_effect=["session-analysi","exit"])
    @patch("builtins.print")
    def test_invalid_command(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Unknown command. Type 'help' to see available commands.", printed_args)

    # Test statistics invalid currency
    @patch("builtins.input", side_effect=["statistics", "CHF", "1m", "exit"])
    @patch("builtins.print")
    def test_statistic_invalid_currency(self, mock_print, mock_input):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        patterns = [
            r"median:\s*\d+\.\d+",
            r"mode:\s*\d+\.\d+",
            r"std_dev:\s*\d+\.\d+",
            r"cv:\s*\d+(\.\d+)?",
        ]

        for pattern in patterns:
            self.assertTrue(
                any(re.search(pattern, arg) for arg in printed_args),
                msg=f"Pattern not found: {pattern}"
            )

    # Test change histogram invalid pair
    @patch("matplotlib.pyplot.show")
    @patch("builtins.input", side_effect=["change-histogram", "USD","USD/EUR","1m","2024-01-01", "exit"])
    @patch("builtins.print")
    def test_change_histogram_invalid_pair(self, mock_print, mock_input,mock_show):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid format. Use exactly one '/' like USD/EUR.", printed_args)

    # Test change histogram invalid date
    @patch("matplotlib.pyplot.show")
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR","1m","dffff","2024-01-01", "exit"])
    @patch("builtins.print")
    def test_change_histogram_invalid_date(self, mock_print, mock_input,mock_show):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        self.assertIn("Invalid date format or date. Please use YYYY-MM-DD.", printed_args)

    # Test change histogram invalid period
    @patch("matplotlib.pyplot.show")
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "k","1m","2024-01-01", "exit"])
    @patch("builtins.print")
    def test_change_histogram_invalid_period(self, mock_print, mock_input,mock_show):
        from main import main
        main()

        printed_args = [call.args[0] for call in mock_print.call_args_list]

        # Write a return error
        self.assertIn("Invalid period. Use '1m' for one month or '1q' for one quarter.", printed_args)

    @patch("matplotlib.pyplot.show")
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "xyz", "1m", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_invalid_period(self, mock_print, mock_input, mock_show):
        from main import main
        main()
        self.assertIn("Invalid period. Use '1m' for one month or '1q' for one quarter.",
                      [call.args[0] for call in mock_print.call_args_list])

    @patch("matplotlib.pyplot.show")
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "1m", "dffff", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_invalid_date(self, mock_print, mock_input, mock_show):
        from main import main
        main()
        self.assertIn("Invalid date format or date. Please use YYYY-MM-DD.", [call.args[0] for call in mock_print.call_args_list])

    @patch("matplotlib.pyplot.show")
    @patch("src.CurrencyManager.CurrencyManager.fetch_data", return_value=[
        ('2024-01-01', 4.00),
        ('2024-01-02', 4.10),
    ])
    @patch("builtins.input", side_effect=["change-histogram", "PLN/USD", "1m", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_pln_in_pair(self, mock_print, mock_input, mock_fetch, mock_show):
        from main import main
        main()
        mock_fetch.assert_called_once()
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    @patch("src.CurrencyManager.CurrencyManager.fetch_data", side_effect=[
        [('2024-01-01', 4.0), ('2024-01-02', 4.2)],
        [('2024-01-01', 2.0), ('2024-01-02', 2.1)],
    ])
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "1m", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_valid_pair(self, mock_print, mock_input, mock_fetch, mock_show):
        from main import main
        main()
        self.assertEqual(mock_fetch.call_count, 2)
        mock_show.assert_called_once()

    @patch("matplotlib.pyplot.show")
    @patch("src.CurrencyManager.CurrencyManager.fetch_data", side_effect=[
        [('2024-01-01', 4.0), ('2024-01-02', 4.2)],
        [('2024-01-01', 2.0)]  # mismatch
    ])
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "1m", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_mismatched_data_length(self, mock_print, mock_input, mock_fetch, mock_show):
        from main import main
        main()
        self.assertIn("Mismatch in data length. Cannot build histogram.", [call.args[0] for call in mock_print.call_args_list])

    @patch("matplotlib.pyplot.show")
    @patch("src.CurrencyManager.CurrencyManager.fetch_data", side_effect=[
        [('2024-01-01', 4.0), ('2024-01-02', 4.1)],
        [('2024-01-01', 2.0), ('2024-01-02', 2.05)],
    ])
    @patch("builtins.input", side_effect=["change-histogram", "USD/EUR", "1m", "2024-01-01", "exit"])
    @patch("builtins.print")
    def test_histogram_full_valid_path(self, mock_print, mock_input, mock_fetch, mock_show):
        from main import main
        main()
        self.assertEqual(mock_fetch.call_count, 2)
        mock_show.assert_called_once()
        self.assertIn("Exiting application.", [call.args[0] for call in mock_print.call_args_list])

class TestMainFlow(unittest.TestCase):
    @patch("builtins.input", side_effect=["list-currencies", "exit"])
    @patch("builtins.print")
    @patch("src.CurrencyManager.CurrencyManager.show_available_currencies")
    def test_main_list_currencies(self, mock_show, mock_print, mock_input):
        from main import main
        main()
        mock_show.assert_called_once()