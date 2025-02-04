import random
import copy

class TicTacToeMC:
    def __init__(self):
        self.board = [" "]*9
        self.current_player = 'X'

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def make_move(self, index, player):
        if self.board[index] == " ":
            self.board[index] = player
            return True
        return False

    def switch_player(self, player):
        return 'O' if player == 'X' else 'X'

    def check_winner(self):
        """
        Checks for a winner or a tie on self.board.
        Returns 'X', 'O', 'Tie', or None.
        """
        win_positions = [
            (0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # columns
            (0,4,8), (2,4,6)            # diagonals
        ]
        for a,b,c in win_positions:
            if (self.board[a] != " " 
                and self.board[a] == self.board[b] == self.board[c]):
                return self.board[a]

        if " " not in self.board:
            return "Tie"
        return None

    def play_random_game(self, board_state, start_player):
        """
        Simulate a random game (both players pick random moves),
        starting from the given board_state (list of 9 cells)
        and player.
        Returns the result: 'X', 'O', or 'Tie'.
        """
        sim_board = copy.deepcopy(board_state)
        player = start_player

        while True:
            winner = self.get_winner_for_state(sim_board)
            if winner is not None:
                return winner
            moves = [i for i, spot in enumerate(sim_board) if spot == " "]
            random_move = random.choice(moves)
            sim_board[random_move] = player
            player = self.switch_player(player)

    def get_winner_for_state(self, board_state):
        """
        Same logic as check_winner but operates on a given board_state 
        (so we don't mutate self.board).
        """
        win_positions = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b,c in win_positions:
            if (board_state[a] != " " 
                and board_state[a] == board_state[b] == board_state[c]):
                return board_state[a]

        if " " not in board_state:
            return "Tie"
        return None

    def monte_carlo_move(self, simulations=5000):
        """
        Returns the index of the best move for self.current_player,
        determined by Monte Carlo simulations.
        """
        best_move = None
        best_score = -1.0
        moves = self.available_moves()

        for move in moves:
            # Try this move
            self.board[move] = self.current_player

            # Next turn would be the other player
            next_player = self.switch_player(self.current_player)

            # Run simulations
            wins = 0
            for _ in range(simulations):
                result = self.play_random_game(self.board, next_player)
                if result == self.current_player:
                    wins += 1

            # Undo the move
            self.board[move] = " "
            win_rate = wins / simulations

            # Track if this is the best so far
            if win_rate > best_score:
                best_score = win_rate
                best_move = move

        return best_move

def get_first_two_moves_for_X(simulations=1000):
    """
    This function:
    1. Lets X find its best first move using Monte Carlo.
    2. Lets O respond (also Monte Carlo).
    3. Lets X find its second-best move (again Monte Carlo).

    Returns (first_move_for_X, second_move_for_X).
    """
    game = TicTacToeMC()

    # --- X's first move ---
    # best first move for X
    x_first_move = game.monte_carlo_move(simulations=simulations)
    game.make_move(x_first_move, 'X')

    # Switch to O
    game.current_player = 'O'

    # --- O's first move ---
    # We do not care which one it is, but we let O move
    o_first_move = game.monte_carlo_move(simulations=simulations)
    game.make_move(o_first_move, 'O')

    # Switch back to X
    game.current_player = 'X'

    # --- X's second move ---
    x_second_move = game.monte_carlo_move(simulations=simulations)
    # (We could apply it or just return it. Let's do both.)
    game.make_move(x_second_move, 'X')

    return x_first_move, x_second_move

if __name__ == "__main__":
    # Example usage: 
    first_move, second_move = get_first_two_moves_for_X(simulations=500)
    print(f"X's best first move (index): {first_move}")
    print(f"X's best second move (index): {second_move}")
