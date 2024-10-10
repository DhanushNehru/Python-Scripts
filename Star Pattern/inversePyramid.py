def inversePyramid(n):
    for i in range(n, -1, -1):
        for j in range(n-i):
            print(" ", end="")
        for k in range(i+1):
            print("* ", end="")
        print()


if __name__ == "__main__":
    n = int(input("Enter the height : "))
    inversePyramid(n)