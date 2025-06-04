import tkinter as tk
from board import UltimateBoard
from game_state import GameState
from agents.random_agent import RandomAgent

CELL_SIZE = 50
BOARD_SIZE = 9 * CELL_SIZE
LINE_WIDTH = 2

class UltimateTicTacToeGUI:
    def __init__(self, root, player_one="human", player_two="human"):
        self.root = root
        self.root.title("Ultimate Tic-Tac-Toe")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()

        self.players = {
            1: player_one,
            -1: player_two
        }

        self.board = UltimateBoard()
        self.game = GameState(self.board, ruleset="majority")
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        valid_actions = self.game.get_valid_actions()
        current_player = self.game.player_turn
        highlight_color = "#ffe6e6" if current_player == 1 else "#e6f0ff"

        for ult_r in range(3):
            for ult_c in range(3):
                mini = self.board.get_mini_board(ult_r, ult_c)
                if mini.winner:
                    fill = "#cc0000" if mini.winner == 1 else "#003399"
                    x1 = ult_c * 3 * CELL_SIZE
                    y1 = ult_r * 3 * CELL_SIZE
                    x2 = x1 + 3 * CELL_SIZE
                    y2 = y1 + 3 * CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='')

        for (ult_r, ult_c, r, c) in valid_actions:
            x1 = (ult_c * 3 + c) * CELL_SIZE
            y1 = (ult_r * 3 + r) * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=highlight_color, outline="black")

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
                            color = "#ff4d4d" if val == 1 else "#4d94ff"
                            x = (ult_c * 3 + c) * CELL_SIZE + CELL_SIZE // 2
                            y = (ult_r * 3 + r) * CELL_SIZE + CELL_SIZE // 2
                            self.canvas.create_text(x, y, text=symbol, font=("Arial", 24), fill=color)


    def handle_click(self, event):
        if self.game.game_over:
            return
        
        if self.players[self.game.player_turn] != "human":
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
            self.update()
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
        
    def update(self):
        if self.game.game_over:
            return

        player = self.players[self.game.player_turn]

        if player == "human":
            return
        else:
            self.root.after(300, self.agent_move)

    def agent_move(self):
        player = self.players[self.game.player_turn]
        if player != "human":
            move = player.get_action(self.game)
            self.game.make_move(*move)
            self.draw_board()
            if self.game.game_over:
                self.show_winner()
            self.update()

def main():
    root = tk.Tk()
    app = UltimateTicTacToeGUI(root, player_one="human", player_two=RandomAgent())
    root.mainloop()

if __name__ == "__main__":
    main()
