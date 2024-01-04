"""
Decimal Conversion
Author: @tonybnya
Filename: base_10.py

A Python script to convert a decimal to binary or to hexadecimal
"""
HEXADECIMALS = {
    0: '0',
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: 'A',
    11: 'B',
    12: 'C',
    13: 'D',
    14: 'E',
    15: 'F'
}


def into_base_2(num: int, visual: bool = False) -> int:
    """
    Decimal to binary

    :param num: decimal number
    :param visual: process visualization
    :return: binary number
    """
    if not isinstance(num, int):
        raise ValueError(
            f"Given value must be an integer, not type {str(type(num))}"
        )

    lst = []
    while num > 0.5:
        if visual:
            print(
                f"{str(num)} / 2 = {str(num / 2)} || \
                {str(num)} % 2 = {str(num % 2)}"
            )

        lst.append(num % 2)
        num = int(num / 2)

    return int(''.join([str(i) for i in lst[::-1]]))


def into_base_16(num: int, visual: bool = False) -> str:
    """
    Decimal to hexadecimal

    :param num: decimal number
    :param visual: process visualization
    :return: hexadecimal number
    """
    if not isinstance(num, int):
        raise ValueError(
            f"Given value must be an integer, not type {str(type(num))}"
        )

    lst = []
    while num != 0:
        if visual:
            print(
                f"{str(num)} % 16 = {str(n % 16)} -> \
                hex = {HEXADECIMALS[num % 16]}"
            )

        lst.append(HEXADECIMALS[num % 16])
        num = int(num / 16)

    if visual:
        print(lst)
        print(f"reversed = {str(lst[::-1])}")

    return ''.join(lst[::-1])
