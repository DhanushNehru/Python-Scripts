import random


def get_user_choice():
    choices = ["rock", "paper", "scissors", "lizard", "spock"]
    user_choice = input("Enter your choice (rock, paper, scissors, lizard, spock): ").lower()
    while user_choice not in choices:
        user_choice = input("Invalid choice. Please enter rock, paper, scissors, lizard, or spock: ").lower()
    return user_choice


def get_computer_choice():
    choices = ["rock", "paper", "scissors", "lizard", "spock"]
    return random.choice(choices)


def determine_winner(user_choice, computer_choice):
    win_conditions = {
        "scissors": ["paper", "lizard"],
        "paper": ["rock", "spock"],
        "rock": ["lizard", "scissors"],
        "lizard": ["spock", "paper"],
        "spock": ["scissors", "rock"]
    }

    if user_choice == computer_choice:
        return "tie"
    elif computer_choice in win_conditions[user_choice]:
        return "user"
    else:
        return "computer"


def play_game():
    print("Welcome to Rock, Paper, Scissors, Lizard, Spock!")

    while True:
        while True:
            try:
                num_rounds = int(input("Enter the number of rounds you want to play: "))
                if num_rounds <= 0:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        user_score = 0
        computer_score = 0
        ties = 0

        for round_number in range(1, num_rounds + 1):
            print(f"\nRound {round_number}/{num_rounds}")

            user_choice = get_user_choice()
            computer_choice = get_computer_choice()

            print(f"\nYou chose: {user_choice}")
            print(f"Computer chose: {computer_choice}")

            winner = determine_winner(user_choice, computer_choice)

            if winner == "tie":
                print("It's a tie!")
                ties += 1
            elif winner == "user":
                print("You win!")
                user_score += 1
            else:
                print("Computer wins!")
                computer_score += 1

            print(f"\nScores:\nUser: {user_score}\nComputer: {computer_score}\nTies: {ties}")

        print("\nFinal Scores:")
        print(f"User: {user_score}")
        print(f"Computer: {computer_score}")
        print(f"Ties: {ties}")

        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    play_game()
