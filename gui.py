import tkinter as tk
from board import UltimateBoard
from game_state import GameState

CELL_SIZE = 50
BOARD_SIZE = 9 * CELL_SIZE
LINE_WIDTH = 2

class UltimateTicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()

        self.board = UltimateBoard()
        self.game = GameState(self.board)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        valid_actions = self.game.get_valid_actions()

        for (ult_r, ult_c, r, c) in valid_actions:
            cell_x = (ult_c * 3 + c) * CELL_SIZE
            cell_y = (ult_r * 3 + r) * CELL_SIZE
            self.canvas.create_rectangle(
                cell_x, cell_y, cell_x + CELL_SIZE, cell_y + CELL_SIZE,
                fill="#e0e0e0", outline="black"
            )

        for i in range(9):
            for j in range(9):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')

        for i in range(1, 3):
            self.canvas.create_line(0, i * 3 * CELL_SIZE, BOARD_SIZE, i * 3 * CELL_SIZE, width=3)
            self.canvas.create_line(i * 3 * CELL_SIZE, 0, i * 3 * CELL_SIZE, BOARD_SIZE, width=3)

        for ult_r in range(3):
            for ult_c in range(3):
                mini = self.board.get_mini_board(ult_r, ult_c)
                for r in range(3):
                    for c in range(3):
                        val = mini.grid[r][c]
                        if val != 0:
                            symbol = 'X' if val == 1 else 'O'
                            x = (ult_c * 3 + c) * CELL_SIZE + CELL_SIZE // 2
                            y = (ult_r * 3 + r) * CELL_SIZE + CELL_SIZE // 2
                            self.canvas.create_text(x, y, text=symbol, font=("Arial", 24))

    def handle_click(self, event):
        if self.game.game_over:
            return

        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        ult_r, r = divmod(row, 3)
        ult_c, c = divmod(col, 3)

        try:
            self.game.make_move(ult_r, ult_c, r, c)
            self.draw_board()
            if self.game.game_over:
                self.show_winner()
        except Exception as e:
            print(f"Invalid move: {e}")

    def show_winner(self):
        winner = self.game.winner
        text = "It's a draw!"
        if winner == 1:
            text = "Player X wins!"
        elif winner == -1:
            text = "Player O wins!"

        self.canvas.create_text(BOARD_SIZE // 2, BOARD_SIZE // 2, text=text,
                                font=("Arial", 32), fill="green")

def main():
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
