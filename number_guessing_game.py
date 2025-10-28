# Program that implements a number guessing game.

import random

def get_level():
    while True:
        try:
            n = int(input("Level: ").strip())
            if n > 0:
                return n
        except ValueError:
            pass

def get_guess():
    while True:
        try:
            guess = int(input("Guess: ").strip())
            if guess > 0:
                return guess
        except ValueError:
            pass

def guessing_game():
    print("Welcome to the Guessing Game!")
    n = get_level()
    number_to_guess = random.randint(1, n)
    while True:
        user_guess = get_guess()
        if user_guess > number_to_guess:
            print("Too large!")
        elif user_guess < number_to_guess:
            print("Too small!")
        else:
            print("Just right!")
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    guessing_game()
