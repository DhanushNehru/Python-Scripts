"""
This module contains functions to swap rows and columns of a matrix.

The module contains the following functions:

- `swap_row(matrix, i, j)`: This function swaps the i-th and j-th rows of the
  given matrix.
- `swap_column(matrix, i, j)`: This function swaps the i-th and j-th columns of
  the given matrix.
- `main()`: This function is the main function of the program. It swaps rows and
  columns of a matrix and prints the result.

Example:
    $ python swap.py
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    [[4, 5, 6], [1, 2, 3], [7, 8, 9]]
    [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
"""

from checker import validate_matrix, print_matrix
import sys


def swap_row(m, i, j):
    """
    This function swaps the i-th and j-th rows of the given matrix.

    Args:
        m (list of lists): The matrix to be modified.
        i (int): The index of the first row to be swapped.
        j (int): The index of the second row to be swapped.
    """
    temp = m[i]
    m[i] = m[j]
    m[j] = temp
    return


def swap_column(m, i, j):
    """
    This function swaps the i-th and j-th columns of the given matrix.

    Args:
        m (list of lists): The matrix to be modified.
        i (int): The index of the first column to be swapped.
        j (int): The index of the second column to be swapped.
    """
    for lis in m:
        lis[i], lis[j] = lis[j], lis[i]
    return


def main():
    """
    This function is the main function of the program. It swaps rows and columns
    of a matrix and prints the result.
    """
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print_matrix(m)
    swap_row(m, 0, 1)
    print_matrix(m)
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    swap_column(m, 0, 2)
    print_matrix(m)


if __name__ == "__main__":
    main()
