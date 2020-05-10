import datetime
from PyQt5 import QtCore

# ---------------------- PortListener -------------------------------
# ----------------- класс прослушки портов --------------------------
# -------------------------------------------------------------------
# line               | объекты, передаваемые в главное окно ChatApp
# file               | когда channel.recieve() отдает сообщение/файл
# ___________________| content = сообщение / text = название файла
# line_recieved      | функции-триггеры
# file_recieved      | line = show_message / file = show_file
# Определен в channels.py и связан с ChatApp
# -------------------------------------------------------------------


class PortListener(QtCore.QObject):
    line = QtCore.pyqtSignal(str)
    file = QtCore.pyqtSignal(str)

    def line_recieved(self, text):
        content = f"{datetime.datetime.now().strftime('%H:%M')} <Собеседник>: {text}"
        self.line.emit(content)

    def file_recieved(self, text):
        self.file.emit(text)
