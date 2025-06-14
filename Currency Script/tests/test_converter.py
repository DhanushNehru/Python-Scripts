import unittest
from converter import CurrencyConverter

class TestCurrencyConverter(unittest.TestCase):
    """Unit tests for CurrencyConverter class."""

    @classmethod
    def setUpClass(cls):
        """Initialize converter once for all tests."""
        cls.converter = CurrencyConverter()

    def test_valid_conversion(self):
        """Test converting from USD to EUR returns a float value."""
        result = self.converter.convert("USD", "EUR", 100)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_same_currency(self):
        """Test converting a currency to itself returns the same amount."""
        amount = 50
        result = self.converter.convert("USD", "USD", amount)
        self.assertAlmostEqual(result, amount, places=2)

    def test_invalid_currency(self):
        """Test invalid currency codes raise ValueError."""
        with self.assertRaises(ValueError):
            self.converter.convert("XXX", "EUR", 100)

        with self.assertRaises(ValueError):
            self.converter.convert("USD", "YYY", 100)

if __name__ == "__main__":
    unittest.main()
