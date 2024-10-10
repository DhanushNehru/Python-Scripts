"""
The inverse of a matrix is a matrix that when multiplied with the original
matrix gives the identity matrix. The inverse of a matrix is calculated using
the adjoint matrix and the determinant of the matrix. The adjoint matrix is the
transpose of the cofactor matrix and the determinant is the sum of the products
of the elements of the matrix and their corresponding cofactors.

The function first calculates the determinant of the matrix. If the determinant
is zero, the function raises a ValueError because the inverse of a matrix with
zero determinant does not exist. The function then calculates the adjoint matrix
and divides each element of the adjoint matrix by the determinant to get the
inverse matrix.
"""
from checker import print_matrix
from adjoint import adjoint
from determinant import determinant
import sys

def inverse(matrix):
    """
    Calculate the inverse of a matrix.

    Args:
        matrix (list of lists): The matrix whose inverse is to be calculated.

    Returns:
        list of lists: The inverse of the input matrix.

    Raises:
        sys.exit: If the matrix is not square or has zero determinant.
    """
    det = determinant(matrix)
    if det == 0:
        sys.exit("Determinant of the matrix is zero and hence inverse matrix does not exist")
    matrix = adjoint(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] / det
    return matrix


def main():
    matrix = [[2, 7, 9], [3, 10, 2], [14, 6, 15]]
    print_matrix(inverse(matrix))


if __name__ == "__main__":
    main()