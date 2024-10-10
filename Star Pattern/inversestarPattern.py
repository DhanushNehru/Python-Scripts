def inversestarPattern(n):
    for i in range(n+1, 0, -1):
        for j in range(1, i+1):
            print("* ", end="")
        print()


if __name__ == "__main__":
    n = int(input("Enter the height : "))
    inversestarPattern(n)