"""
This module contains functions to calculate the sum of all elements in a matrix,
the trace of a matrix and the sum of the elements in the secondary diagonal of a
matrix.

The module contains the following functions:

- `matrix_sum(m)`: This function takes a matrix as input and returns the sum of
  all its elements.
- `trace(m)`: This function takes a matrix as input and returns the sum of the
  elements in its main diagonal.
- `sum_secondary_diagonal(m)`: This function takes a matrix as input and
  returns the sum of the elements in its secondary diagonal.

The module also contains a main function which tests the above functions.

Example:
    m1 = [[1, 2, 10], [4, 5, 11], [7, 8, 12]]
    matrix_sum(m1)
    # Output: 45
    trace(m1)
    # Output: 36
    sum_secondary_diagonal(m1)
    # Output: 39

"""
from checker import validate_matrix, check_matrix_square
import sys


def matrix_sum(m):
    """
    This function calculates the sum of all elements in a matrix.

    Args:
        m (list of lists): The matrix whose sum is to be calculated.

    Returns:
        int: The sum of all elements in the matrix.

    Raises:
        sys.exit: If the 2D array is not a valid matrix.
    """
    if not validate_matrix(m):
        sys.exit("The 2D array is not a valid matrix")
    sum = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            sum += m[i][j]
    return sum


def trace(m):
    """
    This function calculates the trace of a matrix.

    Args:
        m (list of lists): The matrix whose trace is to be calculated.

    Returns:
        int: The trace of the matrix.

    Raises:
        sys.exit: If the matrix is not square.
    """
    if not check_matrix_square(m):
        sys.exit("The matrix is not square")
    sum = 0
    for i in range(len(m)):
        sum += m[i][i]
    return sum


def sum_secondary_diagonal(m):
    """
    This function calculates the sum of the elements in the secondary diagonal of
    a matrix.

    Args:
        m (list of lists): The matrix whose secondary diagonal sum is to be
            calculated.

    Returns:
        int: The sum of the elements in the secondary diagonal of the matrix.

    Raises:
        sys.exit: If the matrix is not square.
    """
    if not check_matrix_square(m):
        sys.exit("The matrix is not square")
    sum = 0
    for i in range(len(m)):
        sum += m[i][len(m)-i-1]
    return sum


def main():
    m1 = [[1, 2, 10], [4, 5, 11], [7, 8, 12]]
    print(matrix_sum(m1))
    print(trace(m1))
    print(sum_secondary_diagonal(m1))


if __name__ == "__main__":
    main()
