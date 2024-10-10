"""
This program implements matrix subtraction.

It includes a function to check if the dimensions of two matrices match,
a function to subtract the second matrix from the first, and a main function
to test the matrix subtraction function.

Example:
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    matrix_subtraction(m1, m2)
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
"""

from checker import check_matrix_dimension, print_matrix
import sys


def matrix_subtraction(m1, m2):
    """
    This function subtracts the second matrix from the first.

    Args:
        m1 (list of lists): The first matrix.
        m2 (list of lists): The second matrix.

    Returns:
        list of lists: The difference of the two matrices.

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
            answer[i][j] = m1[i][j] - m2[i][j]
    return answer


def main():
    """
    This function tests the matrix subtraction function.

    """
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print_matrix(matrix_subtraction(m1, m2))


if __name__ == "__main__":
    main()

