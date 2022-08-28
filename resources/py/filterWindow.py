from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import uic


class FilterWindow(QWidget):

    def __init__(self, mainWindow, regular_library, data):
        super().__init__()
        self.ui = uic.loadUi("resources/ui/filter.ui")
