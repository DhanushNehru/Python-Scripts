import random

# Basic settings
rows = 5
cols = 5
mines = 3

# Create hidden board
board = [[" " for _ in range(cols)] for _ in range(rows)]
visible = [["?" for _ in range(cols)] for _ in range(rows)]

# Place mines
placed_mines = 0
while placed_mines < mines:
    r = random.randint(0, rows - 1)
    c = random.randint(0, cols - 1)
    if board[r][c] != "X":
        board[r][c] = "X"
        placed_mines += 1

# Count mines around a cell
def count_mines(r, c):
    count = 0
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            if 0 <= i < rows and 0 <= j < cols:
                if board[i][j] == "X":
                    count += 1
    return count

# Fill board with numbers
for r in range(rows):
    for c in range(cols):
        if board[r][c] != "X":
            board[r][c] = str(count_mines(r, c))

# Show the visible board
def show():
    for row in visible:
        print(" ".join(row))
    print()

# Game loop
safe_cells = rows * cols - mines
while True:
    show()
    r = int(input("Row (0-4): "))
    c = int(input("Col (0-4): "))
    
    if board[r][c] == "X":
        print("💥 You hit a mine. Game Over!")
        break
    else:
        visible[r][c] = board[r][c]
        safe_cells -= 1
        if safe_cells == 0:
            print("🏆 You won! No safe cells left.")
            break

# Reveal the real board at the end
print("\nReal board:")
for row in board:
    print(" ".join(row))
