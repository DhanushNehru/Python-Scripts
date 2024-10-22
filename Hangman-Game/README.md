
# Hangman-Game

This is a Python implementation of the classic Hangman game. In this game, the player tries to guess a randomly selected word by suggesting letters within a certain number of tries. The player wins if they guess the word correctly before running out of attempts.



## How to Play
1)The computer selects a random word from the provided word list.

2)The player guesses letters or the entire word.

3)For each correct guess, the corresponding letters are revealed in the word.

4)If the player makes an incorrect guess, they lose one of their remaining tries.

5)The game ends when the player either guesses the word or runs out of tries.
## Requirements
Python 3.x
## How to Run

1) Clone the repository:

```bash
  git clone https://github.com/your-username/Python-Scripts.git

```
2) Navigate to the Hangman-Game folder:
```bash
  cd Python-Scripts/Hangman-Game
```
3) Run the game:
```bash
  python hangman_game.py
```
## Files
1)hangman_game.py: The main Python script containing the Hangman game logic.

2)words.py: A Python file that contains a list of words (word_list) from which the game selects the word to guess.

3)README.md: This documentation file.
## Future Improvements
1) Introducing an AI against whom the players can play.
2) Addition of hints 
3) Expanding the word list
## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request to add new features, improve the code, or fix bugs.