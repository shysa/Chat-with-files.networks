from PyQt5 import QtCore, QtWidgets
from gui import info


class InfoDialog(QtWidgets.QDialog, info.Ui_dialog):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Dialog)
        self.setupUi(self)
        self.init_handlers()
        self.setFixedSize(self.size())

    def init_handlers(self):
        self.bOK.clicked.connect(self.close)
