import sys
import os
import unittest
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

if __name__ == '__main__':
    unittest.main()
