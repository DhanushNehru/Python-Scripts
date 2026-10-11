weight = float(input("Enter your weight in kilograms (kg): "))
height = float(input("Enter your height in meters (m): "))

bmi = weight / (height ** 2)
print(f"\nYour BMI is: {bmi:.2f}")

# Determine BMI category
if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obesity")