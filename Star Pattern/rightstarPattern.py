def rightstarPattern(n):
    for i in range(1, n+1):
        for j in range(1, n-i+1):
            print("  ", end="")
        for j in range(1, i+1):
            print("* ", end="")
        print()


if __name__ == "__main__":
    n = int(input("Enter the height : "))
    rightstarPattern(n)