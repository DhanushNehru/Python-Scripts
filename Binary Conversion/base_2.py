"""
Binary Conversion
Author: @tonybnya
Filename: base_2.py

A Python script to convert a string representation of a binary number
into its ASCII code, or into its decimal
"""
from typing import List, Union


def into_ascii(binary: Union[str, List[str]], visual: bool = False) -> str:
    """
    Binary to ASCII

    :param binary: binary number or an array
    :param visual: process visualization
    :return: ASCII code as a string
    """

    if not isinstance(binary, str) or not isinstance(binary, list):
        raise ValueError(
            f"Given value must be a string or an array of strings, \
            not type {str(type(binary))}"
        )
    if isinstance(binary, str):
        digits = binary.split()
    elif isinstance(binary, list):
        digits = binary

    code = ""

    for digit in digits:
        if visual:
            print(
                f"{digit} -> {into_base_10(int(digit))} -> \
                {chr(into_base_10(int(digit)))}"
            )

        value = into_base_10(int(digit))
        code += chr(value)

    return code


def into_base_10(binary: int, visual: bool = False) -> int:
    """
    Binary to decimal

    :param binary: binary number
    :param visual: process visualization
    :return: a decimal number
    """
    if not isinstance(binary, int):
        raise ValueError(
            f"Given value must be an integer, not type {str(type(binary))}"
        )

    num = 0
    lst = [int(i) for i in str(binary)]

    for digit in lst:
        if visual:
            print(f"{str(num)} x 2 + {str(digit)} = {str(num * 2 + digit)}")

        num = num * 2 + digit

    return num
