# Matrix Operations Library
=====================================

A collection of Python functions for performing various matrix operations.

## Functions
-------------

### 1. Checker
---------------

*   **File:** `checker.py`
*   **Description:** This program contains functions to validate a matrix, check if two matrices can be added or multiplied, and check if a matrix is square. It also contains a function to print a matrix.

### 2. Input
-------------

*   **File:** `input.py`
*   **Description:** This program asks the user to input a matrix and prints it back to the user.

### 3. Matrix
-------------

*   **File:** `matrix.py`
*   **Description:** This module contains functions to perform various matrix operations, including addition, subtraction, multiplication, transpose, rotate, cofactor, determinant, adjoint, inverse, swap, and sum.

### 4. Addition
--------------

*   **File:** `addition.py`
*   **Description:** This program implements matrix addition.

### 5. Subtraction
----------------

*   **File:** `subtraction.py`
*   **Description:** This program implements matrix subtraction.

### 6. Multiplication
------------------

*   **File:** `multiplication.py`
*   **Description:** This module contains two functions to multiply matrices.

### 7. Transpose
--------------

*   **File:** `transpose.py`
*   **Description:** This module contains functions to transpose a matrix.

### 8. Rotate
------------

*   **File:** `rotate.py`
*   **Description:** This program rotates a matrix by 90, 180 or 270 degrees.

### 9. Cofactor
-------------

*   **File:** `cofactor.py`
*   **Description:** This module contains functions to calculate the cofactor matrix of a given matrix.

### 10. Determinant
----------------

*   **File:** `determinant.py`
*   **Description:** This module contains a function to calculate the determinant of a matrix.

### 11. Adjoint
-------------

*   **File:** `adjoint.py`
*   **Description:** This module contains a function to calculate the adjoint matrix of a given matrix.

### 12. Inverse
-------------

*   **File:** `inverse.py`
*   **Description:** The inverse of a matrix is a matrix that when multiplied with the original matrix gives the identity matrix.

### 13. Swap
------------

*   **File:** `swap.py`
*   **Description:** This module contains functions to swap rows and columns of a matrix.

### 14. Sum
------------

*   **File:** `sum.py`
*   **Description:** This module contains functions to calculate the sum of all elements in a matrix, the trace of a matrix and the sum of the elements in the secondary diagonal of a matrix.



## Usage
-----

To use the functions in this library, simply import the corresponding module and call the desired function. For example, to add two matrices, you would import the `matrix` module and call the `add_matrices` function.

```python
import matrix

matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]

result = matrix.add_matrices(matrix1, matrix2)
print(result)
```

## Contributed By
--------------

SammyUrfen
