"""
This program implements matrix addition.

It includes a function to check if the dimensions of two matrices match,
a function to add two matrices, and a main function to test the matrix
addition function.

Example:
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_addition(m1, m2)
    [[2, 4, 6], [8, 10, 12], [14, 16, 18]]
"""

from checker import check_matrix_dimension, print_matrix
import sys


def matrix_addition(m1, m2):
    """
    This function adds two matrices.

    Args:
        m1 (list of lists): The first matrix.
        m2 (list of lists): The second matrix.

    Returns:
        list of lists: The sum of the two matrices.

    Raises:
        sys.exit: If the dimensions of the two matrices do not match.
    """
    if check_matrix_dimension(m1, m2) == False:
        sys.exit("Matrix dimensions do not match")

    n = len(m1)
    m = len(m1[0])    
    answer = [[0 for i in range(m)] for j in range(n)]
    for i in range(len(m1)):
        for j in range(len(m1[i])):
            answer[i][j] = m1[i][j] + m2[i][j]
    return answer


def main():
    """
    This function tests the matrix addition function.

    """
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print_matrix(matrix_addition(m1, m2))


if __name__ == "__main__":
    main()
