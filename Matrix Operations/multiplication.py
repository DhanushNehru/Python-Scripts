"""
This module contains two functions to multiply matrices.

The first function, `matrix_multiplication`, multiplies two matrices. The
function takes two matrices as arguments and returns the product of the two
matrices. The function first checks if the dimensions of the two matrices match.
If the dimensions do not match, the function raises a SystemExit exception.

The function then creates a new matrix filled with zeros and calculates the
product of the two matrices by iterating over the elements of the matrices and
multiplying the corresponding elements together. The function then returns the
product of the two matrices.

The second function, `scalar_matrix_multiplication`, multiplies a matrix by a
scalar. The function takes a scalar and a matrix as arguments and returns the
product of the scalar and the matrix. The function first checks if the matrix is
valid. If the matrix is not valid, the function raises a SystemExit exception.

The function then multiplies each element of the matrix by the scalar and
returns the product of the scalar and the matrix.

The module also contains a main function which tests the matrix multiplication
functions.

Example:
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_multiplication(m1, m2)
    [[30, 36, 42], [66, 81, 96], [102, 126, 150]]

    scalar_matrix_multiplication(5, m1)
    [[5, 10, 15], [20, 25, 30], [35, 40, 45]]

"""

from checker import check_matrix_multiplication, validate_matrix, print_matrix
import sys


def matrix_multiplication(m1, m2):
    """
    This function multiplies two matrices.

    Args:
        m1 (list of lists): The first matrix.
        m2 (list of lists): The second matrix.

    Returns:
        list of lists: The product of the two matrices.

    Raises:
        sys.exit: If the dimensions of the two matrices do not match.
    """
    if check_matrix_multiplication(m1, m2) == False:
        sys.exit("Matrix dimensions do not match")

    n = len(m1)
    m = len(m1[0])
    l = len(m2[0])
    answer = [[0 for i in range(l)] for j in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                answer[i][j] += m1[i][k] * m2[k][j]
    
    return answer



def scalar_matrix_multiplication(s, m):
    """
    This function multiplies a matrix by a scalar.

    Args:
        s (int): The scalar.
        m (list of lists): The matrix.

    Returns:
        list of lists: The product of the scalar and the matrix.

    Raises:
        sys.exit: If the matrix is not valid.
    """
    if validate_matrix(m) == False:
        sys.exit("The 2D array is not a valid matrix")
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] = s * m[i][j]
    return m



def main():
    """
    This function tests the matrix multiplication functions.

    """
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print_matrix(matrix_multiplication(m1, m2))
    print_matrix(scalar_matrix_multiplication(5, m1))


if __name__ == "__main__":
    main()

