# Write your code here :-)
import math

# Initialize a 3x3 Tic-Tac-Toe board with empty spaces.
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
nodes_visited = 0  # Counter for the number of nodes visited

def print_board():
    """Prints the current state of the board."""
    for row in board:
        print('|'.join(row))
    print("\n")

def is_winner(player):
    """Checks if the given player has won."""
    #checking each row
    for row in board:   
        if all(s == player for s in row):
            return True
    #checking each column
    for col in range(3): 
        if all(board[row][col] == player for row in range(3)):
            return True
    #checking both diagnols
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)): 
        return True
    return False

def is_full():
    """Returns True if the board is full."""
    return all(cell != ' ' for row in board for cell in row)

def count_winning_lines(player):
    """Counts the total possible winning lines for a player."""
    lines = 0
    #checking winning lines in rows
    for row in board:
        if all(s == player or s == ' ' for s in row):
            lines += 1
    #checking winning lines in columns
    for col in range(3):
        if all(board[row][col] == player or board[row][col] == ' ' for row in range(3)):
            lines += 1
    #checking winning lines in diagnols
    if all(board[i][i] == player or board[i][i] == ' ' for i in range(3)):
        lines += 1
    if all(board[i][2-i] == player or board[i][2-i] == ' ' for i in range(3)):
        lines += 1
    return lines

def heuristic():
    """Evaluates the board state using E(n) = M(n) - O(n)."""
    return count_winning_lines('O') - count_winning_lines('X')

def minimax(is_maximizing):
    """Minimax algorithm with heuristic evaluation and node counting."""
    global nodes_visited
    nodes_visited += 1  # Increment the counter at each node visit

    if is_winner('X'):  # if player wins
        return -10
    if is_winner('O'):  # if AI wins
        return 10
    if is_full():
        return 0

    best_score = -math.inf if is_maximizing else math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O' if is_maximizing else 'X'
                score = minimax(not is_maximizing) + heuristic()
                board[i][j] = ' '
                best_score = max(best_score, score) if is_maximizing else min(best_score, score)
    return best_score

def best_move():
    """Finds and executes the best move for AI."""
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    board[move[0]][move[1]] = 'O'

def main():
    """Main game loop with single number input."""
    global nodes_visited
    while True:
        print_board()
        pos = int(input("Enter position (0-8): "))
        row, col = divmod(pos, 3)
        if board[row][col] != ' ':
            print("Invalid move! Try again.")
            continue
        board[row][col] = 'X'
        if is_winner('X'):
            print_board()
            print("You win!")
            break
        if is_full():
            print_board()
            print("It's a tie!")
            break
        best_move()
        if is_winner('O'):
            print_board()
            print("AI wins!")
            break
        if is_full():
            print_board()
            print("It's a tie!")
            break
    print(f"Total nodes visited: {nodes_visited}")

if __name__ == "__main__":
    main()
