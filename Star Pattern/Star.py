def Star(n):
    # Upper part of the star
    for i in range(1, n + 1):
        for j in range(n):
            print("  ", end="")
        for j in range(1, n - i + 1):
            print("  ", end="")
        for j in range(1, 2 *  i):
            print("* ", end="")
        print()

    # Upper middle part of the star
    for i in range(1, n + 1):
        for j in range(n - 1, n - i, -1):
            print("  ", end="")
        for j in range(1, n - i + 2):
            print("* ", end="")
        for j in range(1, 2 *  n):
            print("* ", end="")
        for j in range(1, n - i + 2):
            print("* ", end="")
        print()

    # Lower middle part of the star
    for i in range(1, n + 1):
        for j in range(1, n - i + 1):
            print("  ", end="")
        for j in range(1, i + 1):
            print("* ", end="")
        for j in range(1, 2 *  n):
            print("* ", end="")
        for j in range(1, i + 1):
            print("* ", end="")
        print()

    # Lower part of the star
    for i in range(n, 0, -1):
        for j in range(n):
            print("  ", end="")
        for j in range(1, n - i + 1):
            print("  ", end="")
        for j in range(1, 2 *  i):
            print("* ", end="")
        print()

if __name__ == "__main__":
    n = int(input("Enter the size of the star: "))
    Star(n)