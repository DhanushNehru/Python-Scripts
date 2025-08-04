def convert_from_celsius(temp: float, to_unit: str) -> float:
    if to_unit == 'a':
        return (temp * 9 / 5) + 32  # Celsius to Fahrenheit
    elif to_unit == 'b':
        return temp + 273.15        # Celsius to Kelvin


def convert_from_fahrenheit(temp: float, to_unit: str) -> float:
    if to_unit == 'a':
        return (temp - 32) * 5 / 9  # Fahrenheit to Celsius
    elif to_unit == 'b':
        return (temp - 32) * 5 / 9 + 273.15  # Fahrenheit to Kelvin


def convert_from_kelvin(temp: float, to_unit: str) -> float:
    if to_unit == 'a':
        return temp - 273.15        # Kelvin to Celsius
    elif to_unit == 'b':
        return (temp - 273.15) * 9 / 5 + 32  # Kelvin to Fahrenheit


def get_conversion():
    print("Choose the input temperature scale:")
    print("1. Celsius")
    print("2. Fahrenheit")
    print("3. Kelvin")
    from_unit = input("Enter option (1/2/3): ")

    try:
        temp = float(input("Enter the temperature: "))
    except ValueError:
        print("Invalid temperature input.")
        return

    if from_unit == "1":
        to_unit = input("Convert to:\n(a) Fahrenheit\n(b) Kelvin\nEnter a/b: ")
        result = convert_from_celsius(temp, to_unit)
        suffix = "°F" if to_unit == 'a' else "K"

    elif from_unit == "2":
        to_unit = input("Convert to:\n(a) Celsius\n(b) Kelvin\nEnter a/b: ")
        result = convert_from_fahrenheit(temp, to_unit)
        suffix = "°C" if to_unit == 'a' else "K"

    elif from_unit == "3":
        to_unit = input("Convert to:\n(a) Celsius\n(b) Fahrenheit\nEnter a/b: ")
        result = convert_from_kelvin(temp, to_unit)
        suffix = "°C" if to_unit == 'a' else "°F"

    else:
        print("Invalid choice. Please choose 1, 2, or 3.")
        return

    print(f"Converted temperature: {result:.2f} {suffix}")


if __name__ == "__main__":
    get_conversion()
