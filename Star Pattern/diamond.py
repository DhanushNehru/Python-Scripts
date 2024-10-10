def diamond(n):
    for i in range(n):
        for j in range(n-i):
            print(" ", end="")
        for k in range(i+1):
            print("* ", end="")
        print()
    for i in range(n-2, -1, -1):
        for j in range(n-i):
            print(" ", end="")
        for k in range(i+1):
            print("* ", end="")
        print()


if __name__ == "__main__":
    n = int(input("Enter the height of half the diamond : "))
    diamond(n)