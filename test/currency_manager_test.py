import unittest
from io import StringIO
from contextlib import redirect_stdout
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

if __name__ == '__main__':
    unittest.main()
