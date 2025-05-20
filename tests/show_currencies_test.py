import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.CurrencyManager import CurrencyManager
from unittest.mock import patch
from io import StringIO

def test_show_available_currencies_output():
    cm = CurrencyManager()
    expected_output = "Available currencies:\n- USD\n- EUR\n- CHF\n- GBP\n- JPY\n- NOK\n- SEK\n"

    with patch('sys.stdout', new=StringIO()) as fake_out:
        cm.show_available_currencies()
        assert fake_out.getvalue() == expected_output

