import random

board = [["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6]


def gamePlayTwoPlayers(p1, p2):
    win = ""
    while win == "":
        column = int(input("{}'s turn. Enter which column you would like to drop your piece into: ".format(p1)))
        connectFourBoard(column, "X")

        if check_vertical_win(p1, p2, column):
            print()
            print(check_vertical_win(p1, p2, column))
            break
        if check_horizontal_win(p1, p2):
            print()
            print(check_horizontal_win(p1, p2))
            break
        if check_positive_diagonal_win(p1, p2):
            print()
            print(check_positive_diagonal_win(p1, p2))
            break
        if check_negative_diagonal_win(p1, p2):
            print()
            print(check_negative_diagonal_win(p1, p2))
            break

        column = int(input("{}'s turn. Enter which column you would like to drop your piece into: ".format(p2)))
        connectFourBoard(column, "O")

        if check_vertical_win(p1, p2, column):
            print() 
            print(check_vertical_win(p1, p2, column))
            break
        if check_horizontal_win(p1, p2):
            print()
            print(check_horizontal_win("x", "O"))
            break
        if check_positive_diagonal_win(p1, p2):
            print()
            print(check_positive_diagonal_win(p1, p2))
            break
        if check_negative_diagonal_win(p1, p2):
            print()
            print(check_negative_diagonal_win(p1, p2))
            break


def gamePlayOnePlayer(p1, p2):
    win = ""
    while win == "":
        column = int(input("{}'s turn. Enter which column you would like to drop your piece into: ".format(p1)))
        connectFourBoard(column, "X")

        if check_vertical_win(p1, p2, column):
            print()
            print(check_vertical_win(p1, p2, column))
            break
        if check_horizontal_win(p1, p2):
            print()
            print(check_horizontal_win(p1, p2))
            break
        if check_positive_diagonal_win(p1, p2):
            print()
            print(check_positive_diagonal_win(p1, p2))
            break
        if check_negative_diagonal_win(p1, p2):
            print()
            print(check_negative_diagonal_win(p1, p2))
            break

        print()

        column = random.randint(1, 7)
        connectFourBoard(column, "O")

        if check_vertical_win(p1, p2, column):
            print()
            print(check_vertical_win(p1, p2, column))
            break
        if check_horizontal_win(p1, p2):
            print()
            print(check_horizontal_win(p1, p2))
            break
        if check_positive_diagonal_win(p1, p2):
            print()
            print(check_positive_diagonal_win(p1, p2))
            break
        if check_negative_diagonal_win(p1, p2):
            print()
            print(check_negative_diagonal_win(p1, p2))
            break


def connectFourBoard(col, playerIcon):
    col -= 1
    coordinate = []

    for row in range(len(board[col])-1, -1, -1):
        if board[col][row] == "-":
            board[col][row] = playerIcon
            coordinate.append([row, col])
            break
    for row in range(len(board)):
        for col in range(len(board[row])):
            print("|", board[row][col], "|", board[row+1][col], "|", board[row+2][col], "|", board[row+3][col], "|",
                  board[row+4][col], "|", board[row+5][col], "|", board[row+6][col], "|")
        break


def check_vertical_win(p1, p2, col):
    playerCount1 = 0
    playerCount2 = 0
    col -= 1

    for row in range(len(board[col])-1, -1, -1):
        if board[col][row] == "X":
            playerCount1 += 1
            playerCount2 = 0
        elif board[col][row] == "O":
            playerCount2 += 1
            playerCount1 = 0

        if playerCount1 == 4:
            return "{} Wins".format(p1)
        elif playerCount2 == 4:
            return "{} Wins".format(p2)


def check_horizontal_win(p1, p2):
    for row in range(len(board[0])-1, -1, -1):
        playerCount1 = 0
        playerCount2 = 0
        for col in range(len(board)):
            if board[col][row] == "X":
                playerCount1 += 1
                playerCount2 = 0
            elif board[col][row] == "O":
                playerCount2 += 1
                playerCount1 = 0
            elif board[col][row] == "-":
                playerCount1 = 0
                playerCount2 = 0

            if playerCount1 == 4:
                return "{} Wins".format(p1)
            elif playerCount2 == 4:
                return "{} Wins".format(p2)


def check_positive_diagonal_win(p1, p2):
    playerCount1 = 0
    playerCount2 = 0

    for row in range(len(board[0])-1, -1, -1):
        for col in range(len(board)-3):
            if board[col][row] == "X":
                playerCount1 += 1
                while playerCount1 < 4:
                    col += 1
                    row -= 1
                    if board[col][row] == "X":
                        playerCount1 += 1
                    else:
                        playerCount1 = 0
                        break
            elif board[col][row] == "O":
                playerCount1 += 1
                while playerCount1 < 4:
                    col += 1
                    row -= 1
                    if board[col][row] == "O":
                        playerCount1 += 1
                    else:
                        playerCount1 = 0
                        break

            if playerCount1 == 4:
                return "{} Wins".format(p1)
            elif playerCount2 == 4:
                return "{} Wins".format(p2)
            else:
                playerCount1 = 0
                playerCount2 = 0


def check_negative_diagonal_win(p1, p2):
    playerCount1 = 0
    playerCount2 = 0

    for row in range(len(board[0])-3):
        for col in range(len(board)-3):
            if board[col][row] == "X":
                playerCount1 += 1
                while playerCount1 < 4:
                    col += 1
                    row -= 1
                    if board[col][row] == "X":
                        playerCount1 += 1
                    else:
                        playerCount1 = 0
                        break
            elif board[col][row] == "O":
                playerCount1 += 1
                while playerCount1 < 4:
                    col += 1
                    row += 1
                    if board[col][row] == "O":
                        playerCount1 += 1
                    else:
                        playerCount1 = 0
                        break

            if playerCount1 == 4:
                return "{} Wins".format(p1)
            elif playerCount2 == 4:
                return "{} Wins".format(p2)
            else:
                playerCount1 = 0
                playerCount2 = 0


def main():
    print("Welcome to Connect Four! Connect 4 of your pieces in either horizontal, vertical, or diagonal to win.")

    numPlayers = int(input("Choose how many players: "))

    while numPlayers not in [1,2]:
        numPlayers = int(input("Sorry for the value you entered was invalid. Are you playing with 1 or 2 players: "))

    if numPlayers == 1:
        player1 = input("Player 1, please enter your name: ")
        player2 = "CPU"
        gamePlayTwoPlayers(player1, player2)
    elif numPlayers == 2:
        player1 = input("Player 1, please enter your name: ")
        player2 = input("Player 2, please enter your name: ")
        gamePlayTwoPlayers(player1, player2)


main()