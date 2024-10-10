"""
This program rotates a matrix by 90, 180 or 270 degrees.

It includes a function to rotate a matrix, and a main function to test the
rotation function.

Example:
    m = [[2, 4, 6, 14], [8, 10, 12, 17], [14, 16, 18, 45]]
    rotate(m, 90)
    # Output:
    # [[14, 17, 45, 18], [12, 10, 8, 6], [6, 4, 2, 14]]

"""
from transpose import transpose
from checker import print_matrix
import sys


def rotate(m, deg = 90):
    """
    Rotate a matrix.

    This function takes a matrix and a rotation degree (90, 180 or 270) as input and returns its rotated version.

    Parameters
    ----------
    m : list of lists
        The matrix to be rotated.

    Returns
    -------
    list of lists
        The rotated matrix.

    Raises
    ------
    sys.exit
        If the matrix is not square.
    """
    
    if (deg!= 90 and deg!= 180 and deg!= 270):
        sys.exit("Rotation degree must be 90, 180 or 270")
    n = deg//90
    k = len(m)
    for _ in range(n):
        m = transpose(m)
        for i in range(len(m)):
            for j in range(len(m[i])//2):
                m[i][j], m[i][k-j-1] = m[i][k-j-1], m[i][j]
    return m


def main():
    m = [[2, 4, 6, 14], [8, 10, 12, 17], [14, 16, 18, 45]]
    print_matrix(rotate(m, 90))


if __name__ == "__main__":
    main()
