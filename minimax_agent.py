

class UltimateMiniMax:
    def __init__(self, depth = 10):
        self.depth = depth

    def make_move(self):
        action_list = self.board.get_valid_actions()
