"""
 AUTHORS:
    Bishoy George        20217021   S12
    Omar Ahmed Mohamed   20216067   S12
    Zaynab El Agamy      20215016   S11
    Farah Mohamad        20216128   S11
    Toka Abd El Ghafar   20218003   S11

"""


import tkinter as tk


class OthelloGUI:
    def __init__(self, master):
        # Initialize the Othello GUI
        self.master = master
        self.master.title("Othello")  # Set the title of the window
        self.master.configure(bg='darkgreen')  # Set the background color of the window
        self.game = OthelloLogic()  # Initialize the game logic
        self.create_widgets()  # Create GUI widgets
        self.update_board()  # Update the game board

    def create_widgets(self):
        # Create GUI widgets
        self.buttons = [[None] * 8 for _ in range(8)]  # Initialize a grid of buttons for the game board

        # Create buttons for each cell of the game board
        for i in range(8):
            for j in range(8):
                self.buttons[i][j] = tk.Button(
                    self.master, width=9, height=3, bg="green", font=('Arial', 14),
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=1, pady=1)

        # Create labels for displaying score and possible moves
        self.score_label = tk.Label(self.master, text="Black: 2 / White: 2", bg="darkgreen", fg="white",
                                    font=('Helvetica', 19, 'bold'))
        self.score_label.grid(row=8, columnspan=8, pady=10)

        self.possible_moves_label = tk.Label(self.master, text="", bg="darkgreen", fg="white", font=('Helvetica', 12))
        self.possible_moves_label.grid(row=9, columnspan=8)

        # Create radio buttons for selecting difficulty level
        difficulty_label = tk.Label(self.master, text="Difficulty:", bg="darkgreen", fg="white", font=('Helvetica', 12))
        difficulty_label.grid(row=10, column=0, pady=0)

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Medium")
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        for i, option in enumerate(self.difficulty_options):
            tk.Radiobutton(
                self.master, text=option, variable=self.difficulty_var, value=option,
                bg="darkgreen", fg="white", selectcolor="black", font=('Helvetica', 12)
            ).grid(row=10, column=i + 1)

        # Create a button to start the game
        start_button = tk.Button(self.master, text="Start", command=self.start_game, bg="lightgrey",
                                 font=('Helvetica', 12, 'bold'))
        start_button.grid(row=10, column=4, padx=20)

    def start_game(self):
        # Start the game with selected difficulty level
        difficulty = self.difficulty_var.get().lower()
        depth = {"easy": 1, "medium": 3, "hard": 5}.get(difficulty, 3)
        self.game.play_ai_move(depth)  # AI makes a move
        self.update_board()
        self.update_score()

    def make_move(self, row, col):
        # Make player move and update GUI
        if self.game.update_board(row, col):
            self.update_board()
            difficulty = self.difficulty_var.get().lower()
            depth = {"easy": 1, "medium": 3, "hard": 5}.get(difficulty, 3)
            self.game.play_ai_move(depth)  # AI makes a move
            self.update_board()
            self.update_score()
            if self.game.end_of_game():  # Check for game end
                self.display_winner()

    def update_board_widgets(self):
        # Update button states based on the game board
        possible_moves = self.game.possible_moves()
        for i in range(8):
            for j in range(8):
                if self.game.board[i][j] == 'B':
                    self.buttons[i][j].config(text='●', bg='green', fg='black')
                elif self.game.board[i][j] == 'W':
                    self.buttons[i][j].config(text='●', bg='green', fg='white')
                elif (i, j) in possible_moves:
                    self.buttons[i][j].config(text='●', bg='#8BC34A', fg='#8BC34A')  # Highlight possible move
                else:
                    self.buttons[i][j].config(text='', bg='green', fg='#8BC34A')  # Empty cell

    def update_board(self):
        # Refresh the game board and display possible moves
        self.update_board_widgets()
        current_moves = self.game.possible_moves()
        self.possible_moves_label.config(text=f"Possible moves: {current_moves}")

    def update_score(self):
        # Update score display
        scores = self.game.calculate_score()
        self.score_label.config(text=f"Black: {scores['B']} / White: {scores['W']}")

    def display_winner(self):
        # Display the game winner
        scores = self.game.calculate_score()
        if scores['B'] > scores['W']:
            winner = "Black"
        elif scores['B'] < scores['W']:
            winner = "White"
        else:
            winner = "It's a tie!"

        winner_label = tk.Label(
            self.master, text=f"Winner: {winner}", font=('Helvetica', 16, 'bold'),
            bg="lightgrey", padx=2, pady=2
        )
        winner_label.grid(row=11, columnspan=8)


class OthelloLogic:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'
        self.opponent = 'W'

    def play_ai_move(self, depth):
        _, best_move = self.alpha_beta_search(self.board, depth)
        if best_move is not None:
            self.update_board(best_move[0], best_move[1])

    def valid_move(self, row, col):
        if self.board[row][col] != ' ':
            return False
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.opponent:
                r, c = r + delta_r, c + delta_c
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False

    def update_board(self, row, col):
        # Check if the move is valid
        if not self.valid_move(row, col):
            return False

        # Place the current player's piece on the board
        self.board[row][col] = self.current_player

        # Flip the opponent's pieces in all 4 directions
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            to_flip = []
            # Collect opponent's pieces to flip
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.opponent:
                to_flip.append((r, c))
                r, c = r + delta_r, c + delta_c
                # Flip the pieces if the current player's piece is found after opponent's pieces
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    for r_flip, c_flip in to_flip:
                        self.board[r_flip][c_flip] = self.current_player
                    break

        # Switch the current player and opponent
        self.current_player, self.opponent = self.opponent, self.current_player
        return True

    def calculate_score(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return {'B': black_count, 'W': white_count}

    def end_of_game(self):
        total_disks = sum(row.count('B') + row.count('W') for row in self.board)
        if total_disks >= 60:
            return True

        for i in range(8):
            for j in range(8):
                if self.valid_move(i, j):
                    return False
        return True

    def possible_moves(self):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.valid_move(i, j):
                    valid_moves.append((i, j))
        return valid_moves

    def alpha_beta_search(self, board, depth):
        _, move = self.alphabeta(board, float('-inf'), float('inf'), depth, True)
        return _, move

    def alphabeta(self, board, alpha, beta, depth, maximizing_player):
        if depth == 0 or self.end_of_game():
            return self.Utility(board), None

        if maximizing_player:
            max_val = float('-inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if self.valid_move(i, j):
                        new_board = [row[:] for row in board]
                        self.test_move_on_board(i, j, new_board)
                        val, _ = self.alphabeta(new_board, alpha, beta, depth - 1, False)
                        if val > max_val:
                            max_val = val
                            best_move = (i, j)
                        alpha = max(alpha, val)
                        if beta <= alpha:
                            break
            return max_val, best_move
        else:
            min_val = float('inf')
            best_move = None
            for i in range(8):
                for j in range(8):
                    if self.valid_move(i, j):
                        new_board = [row[:] for row in board]
                        self.test_move_on_board(i, j, new_board)
                        val, _ = self.alphabeta(new_board, alpha, beta, depth - 1, True)
                        if val < min_val:
                            min_val = val
                            best_move = (i, j)
                        beta = min(beta, val)
                        if beta <= alpha:
                            break
            return min_val, best_move

    def Utility(self, board):
        scores = self.calculate_score()
        return scores[self.current_player] - scores[self.opponent]

    def test_move_on_board(self, row, col, board):
        board[row][col] = self.current_player
        for delta_r, delta_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = row + delta_r, col + delta_c
            to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.opponent:
                to_flip.append((r, c))
                r, c = r + delta_r, c + delta_c
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.current_player:
                    for r_flip, c_flip in to_flip:
                        board[r_flip][c_flip] = self.current_player
                    break


root = tk.Tk()
app = OthelloGUI(root)
root.mainloop()
