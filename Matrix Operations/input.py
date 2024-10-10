"""
This program asks the user to input a matrix and prints it back to the user.

It asks the user how many rows they want in their matrix and then asks the user
to input the elements of the matrix one row at a time. If the user inputs a
matrix that is not valid, the program will raise a SystemExit exception with
the message "Matrix is not valid".

The program will then print out the matrix that the user input with the message
"Here's your matrix: \n".

Example:
    $ python input.py
    How many rows in your matrix? 3
    1 2 3
    4 5 6
    7 8 9
    Here's your matrix:
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

"""

from checker import print_matrix, validate_matrix
import sys


def input_matrix():
    """
    Ask the user to input a matrix.

    The function asks the user how many rows they want in their matrix and then
    asks the user to input the elements of the matrix one row at a time. If the
    user inputs a matrix that is not valid, the function will raise a SystemExit
    exception with the message "Matrix is not valid".

    Returns:
        list of lists: The matrix that the user input.
    """
    m = [list(map(int, input().split())) for _ in range(int(input("How many rows in your matrix?")))]
    if validate_matrix(m) == False:
        sys.exit("Matrix is not valid")
    return m


def main():
    """
    The main function of the program.

    The function asks the user to input a matrix and then prints out the matrix
    that the user input with the message "Here's your matrix: \n".
    """
    m = input_matrix()
    print("Here's your matrix: \n")
    print_matrix(m)


if __name__ == "__main__":
    main()

