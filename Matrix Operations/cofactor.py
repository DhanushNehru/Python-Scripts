"""
This module contains functions to calculate the cofactor matrix of a given
matrix.

A cofactor matrix is a matrix where each element is the cofactor of the
corresponding element in the original matrix. The cofactor of an element is
defined as the minor of the element multiplied by (-1) to the power of the sum
of the row and column indices.

The module contains the following functions:

- `cofactor(matrix)`: This function takes a matrix as input
  and returns its cofactor matrix.

The module also contains a main function which tests the
`calculate_cofactor_matrix` function.

Example usage:
    matrix = [
        [1, 2, 3],
        [0, 4, 5],
        [1, 0, 6]
    ]

    result = calculate_cofactor_matrix(matrix)
    print_matrix(result)
"""

from checker import print_matrix
from minor import minor
from determinant import determinant


def cofactor(matrix):
    """
    This function takes a matrix as input and returns its cofactor matrix.

    Args:
        matrix (list of lists): The input matrix.

    Returns:
        list of lists: The cofactor matrix of the input matrix.

    Raises:
        sys.exit: If the input matrix is not a square matrix.
    """

    n = len(matrix)
    cofactor_matrix = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            minor_matrix = minor(matrix, i, j)
            cofactor_value = ((-1) ** (i + j)) * determinant(minor_matrix)
            cofactor_row.append(cofactor_value)
        cofactor_matrix.append(cofactor_row)

    return cofactor_matrix


def main():
    # Example usage:
    matrix = [
        [1, 2, 3],
        [0, 4, 5],
        [1, 0, 6]
    ]

    result = cofactor(matrix)
    print_matrix(result)


if __name__ == "__main__":
    main()
