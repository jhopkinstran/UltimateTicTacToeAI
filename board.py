class MiniBoard:
    def __init__(self):
        self.grid = [[0]*3 for _ in range(3)]
        self.winner = None
        self.complete = False

    def make_move(self, row, col, player):
        if not self.is_cell_empty(row, col):
            raise ValueError("Cell already taken")
        self.grid[row][col] = player
        self.winner = self.check_win()
        self.complete = self.is_complete()

    def check_win(self):
        for i in range(3):
            if abs(sum(self.grid[i])) == 3:
                return self.grid[i][0]
            if abs(sum([self.grid[j][i] for j in range(3)])) == 3:
                return self.grid[0][i]

        if abs(sum(self.grid[i][i] for i in range(3))) == 3:
            return self.grid[0][0]
        if abs(sum(self.grid[i][2-i] for i in range(3))) == 3:
            return self.grid[0][2]
        return None
        
    def is_cell_empty(self, row, col):
        return self.grid[row][col] == 0

    def is_draw(self):
        return all(cell != 0 for row in self.grid for cell in row)
    
    def is_complete(self):
        return self.winner is not None or self.is_draw()


class UltimateBoard:
    def __init__(self):
        self.boards = [[MiniBoard() for _ in range(3)] for _ in range(3)]
        self.winner = None
        self.complete = False

    def make_move(self, ult_row, ult_col, row, col, player):
        
        self.get_mini_board(ult_row, ult_col).make_move(row, col, player)
        self.winner = self.check_win()
        self.complete = self.winner is not None or self.is_full()

    def get_mini_board(self, row, col):
        return self.boards[row][col]

    def get_ult_grid(self):
        return [[self.boards[r][c].winner or 0 for c in range(3)] for r in range(3)]

    def check_win(self):
        ult = self.get_ult_grid()

        for i in range(3):
            if abs(sum(ult[i])) == 3:
                return ult[i][0]
            if abs(sum(ult[j][i] for j in range(3))) == 3:
                return ult[0][i]

        if abs(ult[0][0] + ult[1][1] + ult[2][2]) == 3:
            return ult[0][0]
        if abs(ult[0][2] + ult[1][1] + ult[2][0]) == 3:
            return ult[0][2]

        return None

    def is_full(self):
        return all(self.boards[r][c].is_complete() for r in range(3) for c in range(3))
    
    def check_majority_win(self):
        ult = self.get_ult_grid()
        total = sum(cell for row in ult for cell in row)
        if sum > 0:
            return 1
        elif sum < 0:
            return -1
        else:
            return 0

 