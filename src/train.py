from mcts_simple import *
import numpy as np

class ConnectFourGame(Game):
    def __init__(self, n_rows=6, n_cols=7, n_win=4):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_win = n_win
        self.board = np.zeros((n_rows, n_cols), dtype=int)
        self.current_player_idx = 0

    def render(self):
        print(self.board)

    def get_valid_moves(self):
        return np.where(self.board[0,:] == 0)[0]
    
    def get_state(self):
        return self.board.copy()

    def number_of_players(self):
        return 2

    def is_terminal(self):
        return self.has_outcome()
    
    def current_player(self):
        return self.current_player_idx
    
    def possible_actions(self):
        return self.get_valid_moves()
    
    def take_action(self, action: int):
        # Find the lowest empty row in the selected column
        for row in range(self.n_rows-1, -1, -1):
            if self.board[row, action] == 0:
                self.board[row, action] = self.current_player_idx + 1
                break
        
        # Switch to the next player
        self.current_player_idx = (self.current_player_idx + 1) % 2
    
    def _check_win(self, return_winner=False):
        # Check for horizontal wins
        for row in range(self.n_rows):
            for col in range(self.n_cols - self.n_win + 1):
                window = self.board[row, col:col + self.n_win]
                # Check for player 1 win
                if np.all(window == 1):
                    return [0] if return_winner else True
                # Check for player 2 win
                if np.all(window == 2):
                    return [1] if return_winner else True

        # Check for vertical wins
        for row in range(self.n_rows - self.n_win + 1):
            for col in range(self.n_cols):
                window = self.board[row:row + self.n_win, col]
                # Check for player 1 win
                if np.all(window == 1):
                    return [0] if return_winner else True
                # Check for player 2 win
                if np.all(window == 2):
                    return [1] if return_winner else True

        # Check for diagonal wins (positive slope)
        for row in range(self.n_rows - self.n_win + 1):
            for col in range(self.n_cols - self.n_win + 1):
                window = np.array([self.board[row + i, col + i] for i in range(self.n_win)])
                # Check for player 1 win
                if np.all(window == 1):
                    return [0] if return_winner else True
                # Check for player 2 win
                if np.all(window == 2):
                    return [1] if return_winner else True

        # Check for diagonal wins (negative slope)
        for row in range(self.n_win - 1, self.n_rows):
            for col in range(self.n_cols - self.n_win + 1):
                window = np.array([self.board[row - i, col + i] for i in range(self.n_win)])
                # Check for player 1 win
                if np.all(window == 1):
                    return [0] if return_winner else True
                # Check for player 2 win
                if np.all(window == 2):
                    return [1] if return_winner else True

        return [] if return_winner else False
    
    def has_outcome(self):
        # Check for win
        if self._check_win():
            return True

        # Check for draw (board is full)
        if len(self.get_valid_moves()) == 0:
            return True

        return False
    
    def winner(self):
        if not self.has_outcome():
            return []
            
        # Check for draw
        if len(self.get_valid_moves()) == 0:
            return [0, 1]
            
        # Check for win
        return self._check_win(return_winner=True)

def train():
    game = ConnectFourGame()
    mcts = MCTS(game, training = True)
    mcts.self_play(iterations = 50000)
    mcts.save("game.mcts")

def play():
    mcts = MCTS(ConnectFourGame(), training = False)
    mcts.load("game.mcts")
    mcts.self_play()

def main():
    train()
    play()

if __name__ == "__main__":
    main()

