from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic


class GameDataWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("resources/ui/gameData.ui")