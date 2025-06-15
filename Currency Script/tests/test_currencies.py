import unittest
from currencies import get_supported_currencies, is_valid_currency

class TestCurrencies(unittest.TestCase):
    """Unit tests for currency helper functions."""

    def setUp(self):
        """Set up sample rates dictionary for use in tests."""
        self.sample_rates = {
            "USD": 1.1,
            "EUR": 1.0,
            "GBP": 0.85,
            "JPY": 150.0
        }

    def test_get_supported_currencies(self):
        """Test that all currency codes are returned correctly."""
        expected = ["USD", "EUR", "GBP", "JPY"]
        result = get_supported_currencies(self.sample_rates)
        self.assertListEqual(sorted(result), sorted(expected))

    def test_is_valid_currency_true(self):
        """Test that valid currency codes return True."""
        self.assertTrue(is_valid_currency("usd", self.sample_rates))
        self.assertTrue(is_valid_currency("EUR", self.sample_rates))

    def test_is_valid_currency_false(self):
        """Test that unsupported currency codes return False."""
        self.assertFalse(is_valid_currency("ABC", self.sample_rates))
        self.assertFalse(is_valid_currency("xyz", self.sample_rates))

if __name__ == "__main__":
    unittest.main()
