from board import UltimateBoard

class GameState:
    def __init__(self, board, ruleset = "default"):
        self.ruleset = ruleset
        self.board = board
        self.player_turn = 1
        self.last_move = None
        self.valid_boards = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        self.game_over = False
        self.winner = None

    def make_move(self, ult_row, ult_col, row, col):
        if self.game_over:
            raise ValueError("Game is already over.")
        
        if not self.is_legal_move(ult_row, ult_col, row, col):
            raise ValueError(f"Illegal move at ({ult_row}, {ult_col}, {row}, {col})")

        # miniboard = self.board.get_mini_board(ult_row, ult_col)
        # miniboard.make_move(row, col, self.player_turn)

        self.board.make_move(ult_row, ult_col, row, col, self.player_turn)

        self.last_move = (ult_row, ult_col, row, col)

        ult_winner = self.board.check_win()
        if ult_winner is not None:
            self.game_over = True
            self.winner = ult_winner
            return

        if self.ruleset == "majority" and self.board.complete:
            self.winner = self.board.check_majority_win()
            self.game_over = True
            return

        if self.ruleset == "default" and self.board.complete:
            self.winner = 0
            self.game_over = True
            return

        self.update_valid_boards()
        self.switch_player()


    def update_valid_boards(self):
        if self.last_move == None:
            return
        _, _, next_ult_row, next_ult_col = self.last_move

        forced_mini_board = self.board.get_mini_board(next_ult_row, next_ult_col)
        
        if not forced_mini_board.is_complete():
            self.valid_boards = [(next_ult_row, next_ult_col)]
        else:
            self.valid_boards = [
                (row, col) for row in range(3) for col in range(3)
                if not self.board.get_mini_board(row, col).is_complete()
            ]


    def get_valid_actions(self) -> list[tuple[int, int, int, int]]:
        actions = []
        for ult_row, ult_col in self.valid_boards:
            mini = self.board.get_mini_board(ult_row, ult_col)
            for row in range(3):
                for col in range(3):
                    if mini.is_cell_empty(row, col):
                        actions.append((ult_row, ult_col, row, col))
        return actions
    
    def is_legal_move(self, ult_row, ult_col, row, col):
        if (ult_row, ult_col) not in self.valid_boards:
            return False
        mini_board = self.board.get_mini_board(ult_row, ult_col)
        if mini_board.grid[row][col] != 0:
            return False
        return True
    
    def switch_player(self):
        self.player_turn *= -1