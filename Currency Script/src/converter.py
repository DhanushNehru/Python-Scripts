from api_handler import get_exchange_data

class CurrencyConverter:
    def __init__(self):
        data = get_exchange_data()
        self.rates = data["rates"]

    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Invalid currency code.")

        # Convert amount to base (EUR), then to target
        amount_in_base = amount if from_currency == "EUR" else amount / self.rates[from_currency]
        converted_amount = round(amount_in_base * self.rates[to_currency], 2)
        return converted_amount

# --- DEBUG / MANUAL TEST SECTION ---
if __name__ == "__main__":
    print("Running manual test for CurrencyConverter...\n")

    converter = CurrencyConverter()
    from_cur = "USD"
    to_cur = "AUD"
    amt = 100.0

    print(f"Converting {amt} {from_cur} to {to_cur}...")
    try:
        result = converter.convert(from_cur, to_cur, amt)
        print(f"{amt} {from_cur} = {result} {to_cur}")
    except ValueError as e:
        print("Error during conversion:", e)