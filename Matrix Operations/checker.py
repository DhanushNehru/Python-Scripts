"""
This program contains functions to validate a matrix, check if two matrices
can be added or multiplied, and check if a matrix is square. It also contains
a function to print a matrix.

Example:
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m4 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(check_matrix_dimension(m1, m2))
    print(check_matrix_multiplication(m1, m2))
    print(check_matrix_square(m3))
    print(check_matrix_square(m4))
    print_matrix(m1)
    print_matrix(m2)
"""

def validate_matrix(m):
    """
    This function validates a matrix.

    It checks if the 2d array is a valid matrix and if the matrix is a list of
    lists.

    Args:
        m (list of lists): The matrix to be validated.

    Returns:
        bool: True if the matrix is valid, False otherwise.
    """
    n = len(m[0])
    for i in range(len(m)):
        if len(m[i]) != n:
            return False
    return True


def check_matrix_dimension(m1, m2):
    """
    This function checks if two matrices can be added.

    It checks if the two matrices have the same dimensions.

    Args:
        m1 (list of lists): The first matrix.
        m2 (list of lists): The second matrix.

    Returns:
        bool: True if the two matrices can be added, False otherwise.
    """
    if (validate_matrix(m1) and validate_matrix(m2)) == False:
        return False
    n = len(m1)
    if (n != len(m2)):
        return False
    for i in range(n):
        if (len(m1[i]) != len(m2[i])):
            return False
    return True


def check_matrix_multiplication(m1, m2):
    """
    This function checks if two matrices can be multiplied.

    It checks if the two matrices have the same number of columns as the first
    matrix has rows.

    Args:
        m1 (list of lists): The first matrix.
        m2 (list of lists): The second matrix.

    Returns:
        bool: True if the two matrices can be multiplied, False otherwise.
    """
    if (validate_matrix(m1) and validate_matrix(m2)) == False:
        return False
    n = len(m1[0])
    if (n != len(m2)):
        return False
    return True


def check_matrix_square(m):
    """
    This function checks if a matrix is square.

    Args:
        m (list of lists): The matrix to be checked.

    Returns:
        bool: True if the matrix is square, False otherwise.
    """
    if validate_matrix(m) == False:
        return False
    n = len(m)
    if (n != len(m[0])):
        return False
    return True


def print_matrix(m):
    """
    This function prints a matrix in the terminal for readability.

    Args:
        m (list of lists): The matrix to be printed.
    """
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(m[i][j], end=" ")
        print()
    print()


def main():
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m4 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(check_matrix_dimension(m1, m2))
    print(check_matrix_multiplication(m1, m2))
    print(check_matrix_square(m3))
    print(check_matrix_square(m4))
    print_matrix(m1)
    print_matrix(m2)


if __name__ == "__main__":
    main()
