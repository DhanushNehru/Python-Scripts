"""
This module contains functions to calculate the determinant of a matrix.

The determinant of a matrix is a scalar value that can be used to describe the
matrix's linear transformation. It can be used to determine the solvability of a
system of linear equations, invertibility of a matrix, and the volume scaling
factor of the linear transformation.

The module contains the following functions:

- `determinant(matrix)`: This function takes a matrix as input and returns its
  determinant.

The module also contains a main function which tests the determinant function.

Example:
    matrix = [[1, 2], [2, 9]]
    determinant(matrix)
    # Output: 7

"""
from checker import check_matrix_square
import sys
from minor import minor

def determinant(matrix):
    """
    Calculate the determinant of a matrix.

    Parameters
    ----------
    matrix : list of lists
        The matrix whose determinant is to be calculated.

    Returns
    -------
    int
        The determinant of the matrix.

    Raises
    ------
    sys.exit
        If the matrix is not square.
    """
    if not check_matrix_square(matrix):
        sys.exit("Matrix is not square")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return sum(((-1) ** j) * matrix[0][j] * determinant(minor(matrix, 0, j)) for j in range(len(matrix)))



def main():
    matrix = [[1, 2], [2, 9]]
    print(determinant(matrix))


if __name__ == "__main__":
    main()
