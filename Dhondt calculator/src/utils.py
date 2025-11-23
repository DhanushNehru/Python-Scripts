def get_positive_integer(prompt: str) -> int:
    """Prompt the user to enter a positive integer."""
    
    valid_input: bool = False
    while not valid_input:
        print(prompt)
        try:
            value: int = int(input())
            if value <= 0:
                print("Please enter a positive integer.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    