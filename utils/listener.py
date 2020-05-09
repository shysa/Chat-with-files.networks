import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class PortListener(QtCore.QObject):
    running = False
    line = QtCore.pyqtSignal(str)
    file = QtCore.pyqtSignal(str)

    def line_recieved(self, text):
        self.line.emit(text)

    def file_recieved(self, text):
        self.file.emit(text)
