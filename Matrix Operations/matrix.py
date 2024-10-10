# matrix.py
'''
    The purpose of this program is to give easy access to all the functions of
    the program in the parent directory.
'''

from addition import matrix_addition
from subtraction import matrix_subtraction
from multiplication import matrix_multiplication
from transpose import transpose as transpose_matrix
from rotate import rotate as rotate_matrix
from cofactor import cofactor as calculate_cofactor
from determinant import determinant as calculate_determinant
from adjoint import adjoint as calculate_adjoint
from inverse import inverse as calculate_inverse
from swap import swap_row, swap_column
from sum import matrix_sum, trace, sum_secondary_diagonal

def add_matrices(matrix1, matrix2):
    return matrix_addition(matrix1, matrix2)

def subtract_matrices(matrix1, matrix2):

    return matrix_subtraction(matrix1, matrix2)

def multiply_matrices(matrix1, matrix2):
    return matrix_multiplication(matrix1, matrix2)

def transpose(matrix):
    return transpose_matrix(matrix)

def rotate(matrix, angle):
    return rotate_matrix(matrix, angle)

def cofactor(matrix):
    return calculate_cofactor(matrix)

def determinant(matrix):
    return calculate_determinant(matrix)

def adjoint(matrix):
    return calculate_adjoint(matrix)

def inverse(matrix):
    return calculate_inverse(matrix)

def swap_row(matrix, i, j):
    return swap_row(matrix, i, j)

def swap_column(matrix, i, j):
    return swap_column(matrix, i, j)

def sum_matrix(matrix):
    return matrix_sum(matrix)

def matrix_trace(matrix):
    return trace(matrix)

def secondary_diagonal_sum(matrix):
    return sum_secondary_diagonal(matrix)