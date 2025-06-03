from board import UltimateBoard
from game_state import GameState
from visualizer import render_board

def main():
    board = UltimateBoard()
    game = GameState(board)

    print("Welcome to Ultimate Tic-Tac-Toe!")
    render_board(game)

    while not game.game_over:
        print(f"\nPlayer {'X' if game.player_turn == 1 else 'O'}'s turn")
        print(f"Valid boards to play in: {game.valid_boards}")
        
        try:
            move = input("Enter move as ult_row ult_col row col (e.g. 0 1 2 2): ")
            ult_r, ult_c, r, c = map(int, move.strip().split())
            game.make_move(ult_r, ult_c, r, c)
            render_board(game)
        except ValueError as ve:
            print(f"Invalid move: {ve}")
        except Exception as e:
            print(f"Error: {e}")

    print("\nGame over!")
    if game.winner == 1:
        print("Player X wins!")
    elif game.winner == -1:
        print("Player O wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()