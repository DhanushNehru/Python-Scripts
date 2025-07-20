import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
from src.api_handler import get_exchange_data

class TestAPIHandler(unittest.TestCase):
    """
    Unit tests for the get_exchange_data function in api_handler.py.
    """
    @patch("api_handler.requests.get")
    def test_get_exchange_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "base": "EUR",
            "date": "2025-06-02",
            "rates": {"USD": 1.14, "GBP": 0.84}
        }

        data = get_exchange_data()
        self.assertEqual(data["base"], "EUR")
        self.assertIn("USD", data["rates"])

    @patch("api_handler.requests.get")
    def test_get_exchange_data_failure(self, mock_get):
        """
        Test that get_exchange_data raises an exception when API response fails.
        """
        mock_get.return_value.status_code = 404
        with self.assertRaises(Exception):
            get_exchange_data()

if __name__ == "__main__":
    unittest.main()

