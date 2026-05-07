#minesweeper game LOL

import random

def create_board(rows, columns):
    return [[0] * columns for _ in range(rows)]

def create_empty_board(rows, columns):
    return [["#"] * columns for _ in range(rows)]

def display_board(board):
    for row in board:
        for column in row:
            print(column, end=" ")
        print()

def already_hit(game_board, hit_row, hit_column):
    return game_board[hit_row][hit_column] != "#"

def already_flagged(game_board, flag_row, flag_column):
    return game_board[flag_row][flag_column] == "f"

def check_mine(board, row, column):
    return board[row][column] == "*"

def build_board(board, row_position, column_position):
    board[row_position][column_position] = "*"
    for row in range(row_position - 1, row_position + 2):
        for column in range(column_position - 1, column_position + 2):
            if row < 0 or column < 0:
                continue
            if row >= len(board) or column >= len(board[0]):
                continue
            if check_mine(board, row, column):
                continue
            board[row][column] += 1

def click(board, game_board, hit_row, hit_column):
    game_board[hit_row][hit_column] = board[hit_row][hit_column]
    if game_board[hit_row][hit_column] == 0:
        expansion(board, game_board, hit_row, hit_column)

def flag(game_board, flag_row, flag_column):
    game_board[flag_row][flag_column] = "f"

def expansion(board, game_board, hit_row, hit_column):
    if hit_row + 1 < len(board):
        if ((not check_mine(board, hit_row+1, hit_column)) and
                game_board[hit_row+1][hit_column] == "#" ):
            click(board, game_board, hit_row+1, hit_column)
    if hit_column + 1 < len(board[0]):
        if ((not check_mine(board, hit_row, hit_column+1)) and
                game_board[hit_row][hit_column+1] == "#" ):
            click(board, game_board, hit_row, hit_column+1)
    if hit_row - 1 >= 0 :
        if ((not check_mine(board, hit_row-1, hit_column)) and
                game_board[hit_row-1][hit_column] == "#" ):
            click(board, game_board, hit_row-1, hit_column)
    if hit_column - 1 >= 0:
        if ((not check_mine(board, hit_row, hit_column-1)) and
                game_board[hit_row][hit_column-1] == "#" ):
            click(board, game_board, hit_row, hit_column-1)

    if hit_row + 1 < len(board) and hit_column + 1 < len(board[0]):
        if ((not check_mine(board, hit_row+1, hit_column+1)) and
                game_board[hit_row+1][hit_column+1] == "#" ):
            click(board, game_board, hit_row+1, hit_column+1)
    if hit_row + 1 < len(board) and hit_column - 1 >= 0:
        if ((not check_mine(board, hit_row+1, hit_column-1)) and
                game_board[hit_row+1][hit_column-1] == "#" ):
            click(board, game_board, hit_row+1, hit_column-1)
    if hit_row - 1 >= 0 and hit_column + 1 < len(board[0]):
        if (not check_mine(board, hit_row-1, hit_column+1) and
                game_board[hit_row-1][hit_column+1] == "#" ):
            click(board, game_board, hit_row-1, hit_column+1)
    if hit_row - 1 >= 0 and hit_column - 1 >= 0:
        if ((not check_mine(board, hit_row-1, hit_column-1)) and
                game_board[hit_row-1][hit_column-1] == "#" ):
            click(board, game_board, hit_row-1, hit_column-1)

def win_check(board, game_board):
    for row in range(len(board)):
        for column in range(len(board[0])):
            if not check_mine(board, row, column):
                if board[row][column] != game_board[row][column]:
                    return False
    return True

def main():

    try:
        rows = int(input("Enter the number of rows: "))
        columns = int(input("Enter the number of columns: "))
    except ValueError:
        print("Invalid board size")
        return
    if rows <= 0 or columns <= 0:
        print("Invalid board size")
        return
    board = create_board(rows, columns)
    game_board = create_empty_board(rows, columns)
    while True:
        try:
            mine_count = int(input("Enter the number of mines: "))
        except ValueError:
            print("Invalid mine count")
            continue
        if mine_count > rows * columns or mine_count < 0:
            print("Invalid mine count")
            continue
        break

    i = 0
    while i < mine_count:
        position = random.randint(1, (rows * columns))
        row_position = (position - 1) // columns
        column_position = (position - 1) % columns
        if check_mine(board, row_position, column_position):
            continue
        build_board(board, row_position, column_position)
        i += 1
    flag_counter = mine_count

    while True:
        display_board(game_board)
        try:
            if flag_counter != 0:
                choice = int(input(f"1) Hit\n2) Flag (remaining: {flag_counter})\n"))
            else:
                print("No flags left so you have to hit")
                choice = 1
        except ValueError:
            print("Please choose 1 or 2")
            continue
        match choice:
            case 1:
                try:
                    hit_row = int(input("Enter the row to hit: "))
                    hit_column = int(input("Enter the column to hit: "))
                except ValueError:
                    print("Invalid hit")
                    continue
                if hit_row <= 0 or hit_column <= 0 \
                        or hit_row > rows or hit_column > columns:
                    print("Invalid hit")
                    continue
                hit_row -= 1
                hit_column -= 1
                if game_board[hit_row][hit_column] == "f":
                    print("Cell is flagged")
                    continue
                if already_hit(game_board, hit_row, hit_column):
                    print("Already revealed")
                    continue
                if check_mine(board, hit_row, hit_column):
                    display_board(board)
                    print("You lose!")
                    break
                click(board, game_board, hit_row, hit_column)
                if win_check(board, game_board):
                    display_board(board)
                    print("You win!")
                    break
            case 2:
                try:
                    flag_row = int(input("Enter the row to flag: "))
                    flag_column = int(input("Enter the column to flag: "))
                except ValueError:
                    print("Invalid flag")
                    continue
                if flag_row <= 0 or flag_column <= 0 \
                        or flag_row > rows or flag_column > columns:
                    print("Invalid flag")
                    continue
                flag_row -= 1
                flag_column -= 1
                if already_flagged(game_board, flag_row, flag_column):
                    print("Already flagged")
                    continue
                if already_hit(game_board, flag_row, flag_column):
                    print("Already revealed")
                    continue
                flag(game_board, flag_row, flag_column)
                flag_counter -= 1
                continue
            case _:
                print("Please choose 1 or 2")
                continue
        print("-" * (rows + 3))

if __name__ == '__main__':
    main()