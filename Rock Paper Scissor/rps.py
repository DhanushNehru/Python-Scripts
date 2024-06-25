import random

# Print multiline instruction
# perform string concatenation of string
print("Winning Rules of the Rock Paper Scissor game as follows: \n"
      + "Rock vs Paper -> Paper wins \n"
      + "Rock vs Scissor -> Rock wins \n"
      + "Paper vs Scissor -> Scissor wins \n"
      + "Similar selections result in a draw. \n")

while True:
    print("Enter choice by entering the appropriate number \n 1. Rock \n 2. Paper \n 3. Scissor \n")

    # Take the input from user
    try:
        choice = int(input("It is your turn, please choose: "))  # Updated here to handle input within try-except block
        while choice > 3 or choice < 1:
            choice = int(input("Please enter a number between 1 and 3: "))  # Moved input validation inside try block
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")  # Added error message for invalid input
        continue

    # Initialize value of choice_name variable corresponding to the choice value
    if choice == 1:
        choice_name = 'Rock'
    elif choice == 2:
        choice_name = 'Paper'
    else:
        choice_name = 'Scissor'

    # Print user choice
    print("You chose: " + choice_name)
    print("\nNow it's my turn.......")

    # Computer chooses randomly any number among 1, 2, and 3 using randint method of random module
    comp_choice = random.randint(1, 3)
    comp_choice_name = {1: 'Rock', 2: 'Paper', 3: 'Scissor'}[comp_choice]

    print(f"I chose: {comp_choice_name}")
    print(f"{choice_name} vs {comp_choice_name}")

    # Determine the result
    if choice == comp_choice:
        print(f"We both chose {choice_name}. It's a draw!")
    else:
        if (choice == 1 and comp_choice == 3) or (choice == 2 and comp_choice == 1) or (choice == 3 and comp_choice == 2):
            print(f"{choice_name} wins! <== User wins ==>")
        else:
            print(f"{comp_choice_name} wins! <== Computer wins ==>")

    # Ask to play again
    print("Do you want to play again? (Y/N)")
    ans = input().lower()
    if ans == 'n':
        break
    elif ans != 'y':
        print("Invalid input. Exiting the game.")
        break

# After coming out of the while loop
# we print thanks for playing
print("\nThanks for playing")
