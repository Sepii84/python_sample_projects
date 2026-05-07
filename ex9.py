#Tic-Tac-Toe

def create_board():
    board = [["-", "-", "-"],
             ["-", "-", "-"],
             ["-", "-", "-"]]
    return board

def display_board(board):
    for row in board:
        for column in row:
            print(column, end=" ")
        print()

def make_move(board, row, column, player):
    board[row][column] = player

def switch_player(player):
    return "O" if player == "X" else "X"

def check_winner(board, player):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def is_draw(board):
    for row in board:
        for column in row:
            if column == "-":
                return False
    return True

def main():
    board = create_board()
    player = "X"

    while True:

        display_board(board)

        try:
            row = int(input("Enter the row: ")) - 1
            column = int(input("Enter the column: ")) - 1
        except ValueError:
            print("Invalid move")
            continue
        if row > 2 or row < 0:
            print("Invalid move")
            continue
        if column > 2 or column < 0:
            print("Invalid move")
            continue

        if board[row][column] != "-":
            print("Invalid move")
            continue

        make_move(board, row, column, player)

        if check_winner(board, player):
            display_board(board)
            print(f"Player {player} wins!")
            break
        if is_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        player = switch_player(player)
        print("---------------")


if __name__ == '__main__':
    main()