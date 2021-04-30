import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Minesweeper")
        self.resize(400, 400)

        # Buttons list
        self.row, self.col, self.bombs = 20, 20, 20
        self.buttons = [[None for _ in range(self.row)] for _ in range(self.col)]

        # Create menu
        self._createMenuBar()

        # Buttons grid
        self._createButtonsGrid()

    def _createMenuBar(self):
        # Main 
        self.menubar_main = QtWidgets.QMenuBar(self)
        # Game size 
        self.menu_game_size = QtWidgets.QMenu("Game size", self)
        # Actions of game size
        self.action_easy = QtWidgets.QAction('Easy (10x10, 10 bombs)', self)
        self.action_medium = QtWidgets.QAction('Medium (20x20, 20 bombs)', self)
        self.action_hard = QtWidgets.QAction('Hard (20x35, 99 bombs)', self)

        self.menu_game_size.addAction(self.action_easy)
        self.menu_game_size.addAction(self.action_medium)
        self.menu_game_size.addAction(self.action_hard)

        self.menubar_main.addMenu(self.menu_game_size)

        # Help
        self.menu_help = QtWidgets.QMenu("Help", self)
        # Actions of help menu
        self.action_restart_game = QtWidgets.QAction("Restart game", self)
        self.action_give_up = QtWidgets.QAction("Give up", self)

        self.menu_help.addAction(self.action_restart_game)
        self.menu_help.addAction(self.action_give_up)

        self.menubar_main.addMenu(self.menu_help)

        self.setMenuBar(self.menubar_main)

    def _createButtonsGrid(self):
        widget_grid = QWidget()
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSizeConstraint(QLayout.SetFixedSize)

        for r in range(self.row):
            for c in range(self.col):
                button = QtWidgets.QPushButton()
                button.setFixedSize(30, 30)
                self.buttons[r][c] = button
                grid_layout.addWidget(button, r, c)

        grid_layout.setHorizontalSpacing(0)
        grid_layout.setVerticalSpacing(0)

        widget_grid.setLayout(grid_layout)
        self.setCentralWidget(widget_grid)

    def _check_button(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
