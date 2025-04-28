from train import ConnectFourGame
from mcts_simple import MCTS
import numpy as np
import random

def print_board(board):
    # Print column numbers
    print("  ", end="")
    for col in range(board.shape[1]):
        print(f"{col} ", end="")
    print()
    
    # Print board with row numbers
    for row in range(board.shape[0]):
        print(f"{row} ", end="")
        for col in range(board.shape[1]):
            cell = board[row, col]
            if cell == 0:
                print(". ", end="")
            elif cell == 1:
                print("X ", end="")
            else:
                print("O ", end="")
        print()

def get_user_move(game):
    while True:
        try:
            col = int(input("Enter column number (0-6): "))
            if col in game.get_valid_moves():
                return col
            print("Invalid move! Column is full or out of range.")
        except ValueError:
            print("Please enter a valid number!")

def main():
    # Initialize game and load trained MCTS
    game = ConnectFourGame()
    tree = MCTS(game, training=False)
    tree.load("game.mcts")
    
    print("Welcome to Connect Four!")
    print("You are X, the AI is O")
    print("Enter column numbers (0-6) to make your moves")
    print()
    
    node = tree.root
    while not game.is_terminal():
        # Print current board state
        print("\nCurrent board:")
        print_board(game.get_state())
        
        actions = game.possible_actions()
        if game.current_player() == 0:  # User's turn
            move = get_user_move(game)
            if node is not None:
                node = node.children[move] if move in node.children else None
        else:  # AI's turn
            print("\nAI is thinking...")
            if node is not None and len(node.children) > 0:
                move = node.choose_best_action(tree.training)
                node = node.children[move]
            else:
                move = random.choice(actions)
                node = None
            print(f"AI placed in column {move}")
        
        game.take_action(move)
    # Game over
    print("\nFinal board:")
    print_board(game.get_state())
    
    winners = game.winner()
    if len(winners) == 2:
        print("\nIt's a draw!")
        print_board(game.get_state())
    elif winners[0] == 0:
        print("\nYou won!")
        print_board(game.get_state())
    else:
        print("\nAI won!")
        print_board(game.get_state())
if __name__ == "__main__":
    main()
