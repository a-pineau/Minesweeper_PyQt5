# ******************** #
# Minesweeper (no GUI) #
# ******************** #

import random
import re

class Minesweeper():
    def __init__(self, rows, cols, nb_bombs):
        """ Constructor
        Sets the grid
        Plant randomly the bombs on it and initialize the number of neighbouring_bombs
        Parameters:
            board_size: int (size of the grid) [optional, default=10]
            nb_bombs: int (number of bombs on the grid) [optional, default=10]
        """
        self.rows = rows
        self.cols = cols
        self.nb_bombs = nb_bombs
        self.known_location = set()

        self.plant_bombs()
        self.set_neighbouring_bombs()


    def display_board(self, real_board):
        """ Display the current board or its full version
        Parameters:
            real_board: bool (if True then the full version is displayed)
        Returns:
            None
        """
        print(self.known_location)
        visible_board = [[self.board[row][col] if (row, col) in self.known_location else ' ' 
                         for col in range(self.cols)] for row in range(self.rows)]

        str_result = f'{" " * 5 + "   ".join([str(i) for i in range(self.cols)])} \n'
        extra_char = len(str_result)
        str_result += f'{"-" * extra_char}\n'

        actual_board = self.board if real_board else visible_board 
        for i, row in enumerate(actual_board):
            str_result += f'{i}  | {" | ".join(row)} |\n'

        str_result += f'{"-" * extra_char}\n'
        print(str_result)

    def plant_bombs(self):
        """ Plant randomly the bombs on the board
        Parameters: 
            None
        Returns:
            None
        """
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        possible_locations = [(i, j) for i in range(self.rows) for j in range(self.cols)]

        while len(possible_locations) > self.rows * self.cols - self.nb_bombs:
            chosen_location = random.choice(possible_locations)
            possible_locations.remove(chosen_location)
            row, col = chosen_location
            self.board[row][col] = '*'


    def get_neighbouring_bombs(self, r, c):
        """ Get the number of neighbouring bombs of a 'free' cell 
        according to a Moore environment
        Parameters:
            r: int (row's index)
            c: int (column's index)
        return:
            type string (number of neighbouring bombs of a given 'free' cell
        """
        neighbouring_bombs = 0
        for row in range(max(0, r-1), min(r+1, self.rows-1)+1):
            for col in range(max(0, c-1), min(c+1, self.cols-1)+1):
                if row == r and col == c:
                    continue
                if self.board[row][col] == '*':
                    neighbouring_bombs += 1
        return str(neighbouring_bombs)


    def set_neighbouring_bombs(self):
        """ Sets the number of neighbouring bombs for each 'free' cell
        Parameters:
            None
        Returns:
            None
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*':
                    continue
                self.board[row][col] = self.get_neighbouring_bombs(row, col)

    def get_board(self):
        """ Returns the board
        Parameters:
            None
        Returns:
            type list: the board (as a nested list)
        """
        return self.board

    def update_game(self, r, c):
        """ Update the state of the game
        If a bomb is hit or every 'free' cells were found, the game is over
        It continues otherwise
        Parameters:
            r: int (row's index of the player's move)
            c: int (column's index of the player's move)
        Return:
            type bool (game over if True
        """
        self.known_location.add((r, c))
        if self.board[r][c] == '*':
            print('BOOM! Game over :(')
            self.display_board(True)
            return True 
        if len(self.known_location) == self.rows * self.cols - 1:
            print('You won!')
            return True 
        if int(self.board[r][c]) > 0:
            return False 
        
        for row in range(max(0, r-1), min(r+1, self.rows-1)+1):
            for col in range(max(0, c-1), min(c+1, self.cols-1)+1):
                if (row, col) in self.known_location:
                    continue    
                self.update_game(row, col)

        return False 

    def ask_move(self):
        """ Ask the player his current move
        Parameters: 
            None
        Return:
            type tuple of int (player's move)
        """
        while True:
            expr = r'^[0-9]{2}$'
            move = input('Pick a location on the board (row (09) - column (09)): ')
            if re.match(expr, move) is None:
                print('Invalid move!')
                continue
            row, col = move
            if (int(row), int(col)) in self.known_location:
                print('You\'ve already played here!')
                continue
            break

        return int(row), int(col)

    def play_again(self):
        """ Ask the player if he wants to keep playing
        Parameters:
            None
        Returns:
            type bool (if True, game starts over)
        """
        while True:
            play_game = input('Play again (y/n)?: ')
            if re.search(r'^y|n{1}$', play_game, re.IGNORECASE) is None:
                print('Please enter \'y\', \'Y\', \'n\' or \'N\'')
                continue
            if re.search(r'^y{1}$', play_game, re.IGNORECASE):
                return True
            return False

    
if __name__ == "__main__":
    while True:
        M = Minesweeper(10, 10, 10)
        M.display_board(True)
        game_over = False

        while not game_over:
            M.display_board(False)
            r, c = M.ask_move()
            game_over = M.update_game(r, c)
        
        if M.play_again():
            continue
        else:
            print('Bye...')
            break
        
