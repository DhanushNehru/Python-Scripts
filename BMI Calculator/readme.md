# Simple BMI Calculator (Python)

A straightforward command-line tool to calculate **Body Mass Index (BMI)** and determine your weight category based on standard classifications.

## What it does

- Asks for your weight (in pounds)
- Asks for your height (in inches)
- Calculates BMI using the imperial formula
- Displays your BMI rounded to 1 decimal place + weight category

## BMI Categories (imperial units)

| BMI Range       | Category        |
|-----------------|-----------------|
| < 18.5          | Underweight     |
| 18.5 – 24.9     | Normal weight   |
| 25.0 – 29.9     | Overweight      |
| 30.0 and above  | Obese           |

## Requirements

- Python 3.x
- [pyinputplus](https://pypi.org/project/PyInputPlus/) library

```bash
pip install pyinputplus

##Usage

python bmicalc.py
# or
python3 bmicalc.py

## Example Run

How much do you weigh in Lbs?  165
How tall are you in inches?  68
your BMI is 25.1, you are overweight.