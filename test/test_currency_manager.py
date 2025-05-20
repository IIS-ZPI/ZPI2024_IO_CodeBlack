import sys
import os
import unittest
from unittest.mock import mock_open, patch
from io import StringIO
from unittest.mock import patch
from contextlib import redirect_stdout
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.CurrencyManager import CurrencyManager

class TestCurrencyManager(unittest.TestCase):
    def test_show_help_output(self):
        cm = CurrencyManager()
        buffer = StringIO()

        with redirect_stdout(buffer):
            cm.show_help()

        output = buffer.getvalue()

        self.assertIn("Available commands:", output)
        self.assertIn("fetch-data", output)
        self.assertIn("list-currencies", output)
        self.assertIn("help", output)
        self.assertIn("export csv", output)

    def test_show_available_currencies_output(self):
        cm = CurrencyManager()
        expected_output = "Available currencies:\n- USD\n- EUR\n- CHF\n- GBP\n- JPY\n- NOK\n- SEK\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cm.show_available_currencies()
            assert fake_out.getvalue() == expected_output

    def test_export_to_csv(self):
        exporter = CurrencyManager()
        data = [["2023-01-01", 4.5], ["2023-01-02", 4.6]]
        mock_file = mock_open()

        with patch("builtins.open", mock_file), \
             patch("csv.writer") as mock_writer_class, \
             patch("builtins.print") as mock_print:

            mock_writer = mock_writer_class.return_value
            exporter.export_to_csv(data, "test.csv")

            mock_file.assert_called_once_with("test.csv", mode='w', newline='')

            mock_writer.writerow.assert_called_once_with(["Date", "Exchange Rate"])
            mock_writer.writerows.assert_called_once_with(data)

            mock_print.assert_called_once_with("Data exported to test.csv")

if __name__ == '__main__':
    unittest.main()
