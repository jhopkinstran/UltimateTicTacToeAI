def render_board(game_state):
    board = game_state.board
    macro = board.boards
    symbols = {1: 'X', -1: 'O', 0: ' '}

    def render_macro_row(m_row):
        # Collect 3 rows from each MiniBoard and combine them
        lines = [""] * 3
        for mini in m_row:
            for i in range(3):
                row_symbols = [symbols[mini.grid[i][j]] for j in range(3)]
                lines[i] += " " + " | ".join(row_symbols) + "  ||"
        return lines

    print("\nCurrent Board:")
    for macro_row_index, macro_row in enumerate(macro):
        lines = render_macro_row(macro_row)
        for line in lines:
            print(line[:-2])  # Remove last '||'
        if macro_row_index < 2:
            print("=" * 35)  # Divider between macro rows
