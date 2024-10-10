"""
This module contains a function to calculate the minor matrix of a given matrix.

The function takes a matrix and two indices as arguments and returns the minor
matrix of the given matrix at the given indices.

The minor matrix is a matrix that is formed by removing the row and column at the
given indices from the given matrix.

The module also contains a main function which tests the minor function.

Example:
    matrix = [[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12], [13, 14, 15, 16]]
    i = 1
    j = 1
    minor(matrix, i-1, j-1)
    # Output:
    # [[1, 3, 10], [7, 9, 12], [13, 15, 16]]
"""

from checker import print_matrix


def minor(matrix, i, j):
    """
    This function calculates the minor matrix of a given matrix at the given
    indices.

    Parameters
    ----------
    matrix : list of lists
        The input matrix.
    i : int
        The row index.
    j : int
        The column index.

    Returns
    -------
    list of lists
        The minor matrix of the given matrix at the given indices.
    """
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]


def main():
    matrix = [[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12], [13, 14, 15, 16]]
    i = 1
    j = 1
    print_matrix(minor(matrix, i-1, j-1))


if __name__ == "__main__":
    main()
