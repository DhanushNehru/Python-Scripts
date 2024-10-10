"""
This module contains functions to transpose a matrix.

The module contains the following functions:

- `transpose(matrix)`: This function takes a matrix as input and returns its
  transpose.

The module also contains a main function which tests the transpose function.

Example:
    m = [[2, 4, 6, 14], [8, 10, 12, 17], [14, 16, 18, 45]]
    transpose(m)
    # Output:
    # [[2, 8, 14], [4, 10, 16], [6, 12, 18], [14, 17, 45]]
"""

from checker import validate_matrix, print_matrix
import sys


def transpose(m):
    """
    Transpose a matrix.

    Parameters
    ----------
    m : list of lists
        The matrix to be transposed.

    Returns
    -------
    list of lists
        The transposed matrix.

    Raises
    ------
    sys.exit
        If the matrix is not square.
    """
    if validate_matrix(m) == False:
        sys.exit("Matrix is not valid")
    a = len(m)
    b = len(m[0])
    answer = [[0 for i in range(a)] for j in range(b)]
    for i in range(b):
        for j in range(a):
            answer[i][j] = m[j][i]
    return answer


def main():
    """
    This function reads a matrix from the user and prints its transpose.
    """
    m = [[2, 4, 6, 14], [8, 10, 12, 17], [14, 16, 18, 45]]
    print_matrix(transpose(m))


if __name__ == "__main__":
    main()

