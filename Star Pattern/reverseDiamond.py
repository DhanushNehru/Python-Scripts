def reverseDiamond(n):
    for i in range(1, n + 1):
        for j in range(1, 2 * n):
            if n - i + 1 < j < n + i - 1:
                print(" ", end="")
            else:
                print("*", end="")
        print()

    for i in range(n-1, 0, -1):
        for j in range(1, 2 * n):
            if n - i + 1 < j < n + i - 1:
                print(" ", end="")
            else:
                print("*", end="")
        print()
    


if __name__ == "__main__":
    n = int(input("Enter the height of half the diamond : "))
    reverseDiamond(n)