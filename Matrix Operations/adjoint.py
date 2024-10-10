"""
This module contains a function to calculate the adjoint matrix of a given matrix.

The adjoint matrix of a matrix is the transpose of its cofactor matrix.

The module contains the following functions:

- `adjoint(matrix)`: This function takes a matrix as input and returns its
  adjoint matrix.

The module also contains a main function which tests the adjoint function.

Example:
    matrix = [[1, -1, 2], [2, 3, 5], [1, 0, 3]]
    adjoint(matrix)
    # Output:
    # [[9, 3, -11], [-1, 1, -1], [-3, -1, 5]]
"""

from checker import print_matrix
from cofactor import cofactor
from transpose import transpose


def adjoint(matrix):
    """
    This function takes a matrix as input and returns its adjoint matrix.

    Args:
        matrix (list of lists): The input matrix.

    Returns:
        list of lists: The adjoint matrix of the input matrix.

    Raises:
        sys.exit: If the input matrix is not a square matrix.
    """
    matrix = transpose(cofactor(matrix))
    return matrix


def main():
    m = [[1, -1, 2], [2, 3, 5], [1, 0, 3]]
    result = adjoint(m)
    print_matrix(result)


if __name__ == "__main__":
    main()
