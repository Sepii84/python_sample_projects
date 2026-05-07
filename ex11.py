#minesweeper board generator:

def create_board(rows, columns):
    return [[0] * columns for _ in range(rows)]

def display_board(board):
    for row in board:
        for column in row:
            print(column, end=" ")
        print()

def check_mine(board, row, column):
    return board[row][column] == "*"

def place_mine(board, row_position, column_position):
    board[row_position][column_position] = "*"
    update_adjacent_counts(board, row_position, column_position)

def update_adjacent_counts(board, row_position, column_position):
    for row in range(row_position - 1, row_position + 2):
        for column in range(column_position - 1, column_position + 2):
            if row < 0 or column < 0:
                continue
            if row >= len(board) or column >= len(board[0]):
                continue
            if check_mine(board, row, column):
                continue
            board[row][column] += 1

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
        try:
            row_position = int(input(f"Enter the row position of mine number {i + 1}: "))
            column_position = int(input(f"Enter the column position of mine number {i + 1}: "))
        except ValueError:
            print("Invalid mine position")
            continue
        if (row_position > rows or column_position > columns or
                row_position <= 0 or column_position <= 0):
            print("Invalid mine position")
            continue
        if check_mine(board, row_position-1, column_position-1):
            print("Invalid mine position")
            continue
        i += 1
        row_position -= 1
        column_position -= 1
        place_mine(board, row_position, column_position)
    display_board(board)

if __name__ == '__main__':
    main()