import math
import random

class Player:
    def _init_(self, letter):
        #letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass

    class RandomComputerPlayer(Player):
        def _init_(self, letter):
            super()._init_(letter)
        
        def get_move(self, game):
            # get a random valid spot for our next move
            square = random.choice[game.available_moves()]
            return square

class HumanPlayer(Player):
    def _init_(self, letter):
        super()._init_(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (8-9):')
            # we're going to check that this is a correct value by trying to cast
            # it to an integer, and id it's not, then we say its invalid
            # if that spot is not available on the board, we also say its invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True # if these are successful, then yay!
            except ValueError:
                print('Invalid square. Try again.')

        return val 
    
class GeniusComputerPlayer(Player):
    def _init_(self, letter):
        super()._init_(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)
        return square
    
    def minimax(self, state, player):
        max_player = self.letter # yourself!
        other_player = 'O' if player == 'X' else 'X' # the other player...

        # first, we want to check if the previous move is a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of the score
            # for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_square() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)
                    } 
        
        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': -math.inf} # each score should minimize


        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # noe, we alternate players

            # step 2: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messed up from the recursion


            # step 4: update the dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best ['score']:
                    best = sim_score # replace best
                else:
                    if sim_score['score'] < best ['score']:
                        best = sim_score # replace best
            return best