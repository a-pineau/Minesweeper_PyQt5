import sys
import Minesweeper as MS
import time
import os
import platform

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout)

BASE_FOLDER = os.path.dirname(__file__)
IMG_BOMB_PATH = os.path.join(BASE_FOLDER, f"images{os.sep}bomb.png")
IMG_FLAG_PATH = os.path.join(BASE_FOLDER, f"images{os.sep}flag.png")
IMG_RESTART_PATH = os.path.join(BASE_FOLDER, f"images{os.sep}restart.png")
IMG_GIVEUP_PATH = os.path.join(BASE_FOLDER, f"images{os.sep}lock2.png")
COLORS = ['#0042FF', # 1 neighbours: blue
          '#248B00', # 2 neighbours: green
          '#FF0000', # 3 neighbours: red
          '#640000', # 4 neighbours: ...
          '#340064', # 5 neighbours: purple  
          '#D500FF', # 6 neighbours: pink
          '#249274', # 7 neighbours: green 2
          '#000000'  # 8 neighbours: black
         ] 

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, row=10, col=10, bombs=10, button_size=35, parent=None):
        """ Constructor
        Parameters:
            row: int (number of rows) [optionnal, default=10]
            col: int (number of columns) [optionnal, default=10]
            bomb: int (number of bombs) [optionnal, default=10]
            button_size: int (grid's button size) [optionnal, default=35]
        """
        super().__init__(parent)
        self.setWindowTitle("Minesweeper")

        """ Game data """
        # Num. of rows, cols and bombs planted
        self.row, self.col, self.button_size, self.bombs = row, col, button_size, bombs
        # Board (Minesweeper)
        self.game = MS.Minesweeper(self.row, self.col, self.bombs)
        # Locations already revealed
        self.known_location = set()
        # Bombs location
        self.bombs_location = set()

        """ GUI data (from top to bottom) """
        # Central widget
        self.central_widget = QtWidgets.QWidget(self)
        # Vertical layout to hold the top frame and the grid
        self.V_layout = QtWidgets.QVBoxLayout(self.central_widget)
        # Create menu bar
        self._create_menu_bar()
        # Connect actions (of menu bar)
        self._connect_menu_bar_actions()
        # Create top frame
        self._create_top_frame()
        # Create grid grid
        self._create_grid()
        # Buttons grid
        self._create_buttons_grid()
        # Timer
        self._init_timer = int(time.time())

        self.setCentralWidget(self.central_widget)
        self.V_layout.addLayout(self.h_layout)
        self.V_layout.addLayout(self.grid_layout)
        self.V_layout.setSizeConstraint(QLayout.SetFixedSize)

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_timer)
        self._timer.start(1000) 

    def _create_menu_bar(self):
        """ Create the menu bar (Difficulty)
        Parameters:
            None
        Returns:
            None
        """
        # Main 
        self.menubar_main = QtWidgets.QMenuBar(self)
        # Game size 
        self.menu_game_size = QtWidgets.QMenu("Difficulty", self)
        # Actions of game size
        self.action_easy = QtWidgets.QAction('Easy (10x10, 10 bombs)', self)
        self.action_medium = QtWidgets.QAction('Medium (20x20, 20 bombs)', self)
        self.action_hard = QtWidgets.QAction('Hard (20x35, 99 bombs)', self)

        self.menu_game_size.addAction(self.action_easy)
        self.menu_game_size.addAction(self.action_medium)
        self.menu_game_size.addAction(self.action_hard)

        self.menubar_main.addMenu(self.menu_game_size)
        self.setMenuBar(self.menubar_main)

    def _connect_menu_bar_actions(self):
        """ Connect the menu bar to the difficulty actions
        Parameters:
            None
        Returns:
            None
        """
        # Game size
        self.action_easy.triggered.connect(lambda: self._change_game_size(10, 10, 10, 35))
        self.action_medium.triggered.connect(lambda: self._change_game_size(20, 20, 40, 25))
        self.action_hard.triggered.connect(lambda: self._change_game_size(25, 35, 99, 20))

    def _create_top_frame(self):
        """ Create the top frame
        From left to right: Number of bombs, give up button,
        restart button and timer
        Parameters:
            None
        Returns:
            None
        """
        # Horizontal layout
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.setContentsMargins(5,5,5,5)

        """ From left to right """
        # Label num. bombs
        self.label_num_bombs = QtWidgets.QLabel()
        self.label_num_bombs.setText(str(self.bombs))
        self.label_num_bombs.setFont(QtGui.QFont("Calibri", 22, QFont.Bold))
        self.label_num_bombs.setAlignment(QtCore.Qt.AlignCenter)
        self.label_num_bombs.setStyleSheet("border: 0px")
        self.h_layout.addWidget(self.label_num_bombs)
        # Give up button
        self.give_up_button = QtWidgets.QPushButton()
        self.give_up_button.clicked.connect(self._reveal_bombs)
        self.give_up_button.setFixedSize(50, 50)
        self.give_up_button.setIcon(QtGui.QIcon(IMG_GIVEUP_PATH))
        self.give_up_button.setToolTip("Restart game")
        self.give_up_button.setIconSize(QSize(45, 45))
        self.h_layout.addWidget(self.give_up_button)
        # Reset button
        self.reset_button = QtWidgets.QPushButton()
        self.reset_button.clicked.connect(self._restart_game)
        self.reset_button.setFixedSize(50, 50)
        self.reset_button.setIcon(QtGui.QIcon(IMG_RESTART_PATH))
        self.reset_button.setToolTip("Restart game")
        self.reset_button.setIconSize(QSize(50, 50))
        self.h_layout.addWidget(self.reset_button)
        # Time elapsed
        self.label_time = QtWidgets.QLabel()
        self.label_time.setText("000")
        self.label_time.setFont(QtGui.QFont("Calibri", 22, QFont.Bold))
        self.label_time.setStyleSheet("border: 0px")
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.h_layout.addWidget(self.label_time)

    def _update_timer(self):
        """ Update the timer and set the corresponding label text
        Parameters:
            None
        Returns:
            None
        """
        secs = int(time.time()) - self._init_timer
        self.label_time.setText("%03d" % secs)

    def _create_grid(self):
        """ Create the main grid containing the buttons
        Parameters:
            None
        Returns:
            None
        """
        # Grid
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setContentsMargins(5,5,5,5)

    def _create_buttons_grid(self):
        """ Create the buttons 
        Parameters:
            None
        Returns:
            None
        """
        board = self.game.get_board()
        self.buttons = [[None for _ in range(self.col)] for _ in range(self.row)]
        for r in range(self.row):
            for c in range(self.col):
                if board[r][c] == '*': self.bombs_location.add((r, c))
                button = QtWidgets.QPushButton()
                button.setProperty("row", r)
                button.setProperty("col", c)
                button.installEventFilter(self)
                button.setFixedSize(self.button_size, self.button_size)
                self.grid_layout.addWidget(button, r, c)
                self.buttons[r][c] = button

    def _display_message_box(self, text):
        """ Display the message box when the game is over
        Parameters:
            text: string (text to display)
        Returns:
            None
        """
        msg = QMessageBox(QMessageBox.Information, "Game over", text)
        restart_button = msg.addButton("Restart", QMessageBox.ActionRole)
        quit_button = msg.addButton("Quit", QMessageBox.ActionRole)
        msg.exec_()

        if msg.clickedButton() == restart_button:
            self._restart_game()
        elif msg.clickedButton() == quit_button:
            self.close()

    def _reveal_bombs(self):
        """ Reveal the bombs locations
        Parameters:
            None
        Returns:
            None
        """
        w = self.buttons[0][0].size().width()
        for loc in self.bombs_location:
            r, c = loc
            self.buttons[r][c].setIcon(QtGui.QIcon(IMG_BOMB_PATH))
            self.buttons[r][c].setIconSize(QSize(w-5, w-5))

    def _check_button(self, r, c):
        """ Check the grids buttons when clicked
        Parameters:
            r: int (row's indice of button)
            c: int (column's indice of button)
        Returns:
            None
        """         
        self.known_location.add((r, c))
        board = self.game.get_board()
        result = board[r][c]

        # Bomb found :(
        if result == '*':
            self.buttons[r][c].setIcon(QtGui.QIcon(IMG_BOMB_PATH))
            self._reveal_bombs()
            self._display_message_box("BOOM! You lost :(")
            return
        # Cell with neighbouring bombs
        if int(result) > 0:
            self.buttons[r][c].setText(str(result))
            self.buttons[r][c].setFont(QtGui.QFont("Calibri", 13, QFont.Bold))
        else:
        # No neighbours - recursive search
            for row in range(max(0, r-1), min(r+1, self.row-1)+1):
                for col in range(max(0, c-1), min(c+1, self.col-1)+1):
                    if (row, col) in self.known_location:
                        continue
                    self.buttons[r][c].setText('')
                    self._check_button(row, col)

        self.buttons[r][c].setEnabled(False)
        self.buttons[r][c].setIcon(QtGui.QIcon())
        self.buttons[r][c].setStyleSheet(f"color: {COLORS[int(result) -1]}; \
                                         border-style: dotted")    
        if len(self.known_location) == self.row * self.col - self.bombs:
            self._display_message_box("You won!")

    def _add_flag_marker(self, r, c):
        """ Add a flag marker on mouse right click
        Parameters:
            r: int (row's indice of button)
            c: int (column's indice of button)
        Returns:
            None
        """
        w = self.buttons[0][0].size().width()
        if self.buttons[r][c].isEnabled():
            self.buttons[r][c].setIcon(QtGui.QIcon(IMG_FLAG_PATH))
            self.buttons[r][c].setIconSize(QSize(w-5, w-5))

    def eventFilter(self, obj, event):
        """ Set a filter to handle the left/right clicks actions
        Parameters:
            obj: Grid's button clicked
            event: Event type (left or right click)
        Returns:
            a event type
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            r, c = obj.property("row"), obj.property("col")
            if event.button() == QtCore.Qt.LeftButton:
                self._check_button(r, c)
            elif event.button() == QtCore.Qt.RightButton:
                self._add_flag_marker(r, c)
        return QtCore.QObject.event(obj, event)

    def _change_game_size(self, r, c, b, b_size):
        """ Change the game's size
        Parameters:
            row: int (number of rows) [optionnal, default=10]
            col: int (number of columns) [optionnal, default=10]
            b: int (number of bombs) [optionnal, default=10]
            b_size: int (grid's button size) [optionnal, default=35]
        """
        self.game = MS.Minesweeper(r, c, b)
        self.row, self.col, self.bombs, self.button_size = r, c, b, b_size
        self.label_num_bombs.setText(str(self.bombs))
        self._create_grid
        self._restart_game()

    def _restart_game(self):
        """ Restart the game
        Parameters:
            None
        Returns:
            None
        """
        self._init_timer = int(time.time())
        self.known_location.clear()
        self.bombs_location.clear()
        self.game.plant_bombs()
        self.game.set_neighbouring_bombs()

        # First, get rid of all the layout's widgets
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        # And add new one
        self._create_buttons_grid()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
