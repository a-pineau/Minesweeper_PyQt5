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

