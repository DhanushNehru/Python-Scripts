# Get data
from typing import Optional


results = []

def get_positive_integer(prompt: str) -> Optional[int]:
    value: Optional[int] = None
    valid_input = False
 
    while not valid_input:
        print(prompt)
        try:
            value = int(input())
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                valid_input = True
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return value
