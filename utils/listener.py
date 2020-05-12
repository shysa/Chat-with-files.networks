import datetime
from PyQt5 import QtCore

# ------------------------ PortListener -------------------------------
# ------------------- класс прослушки портов --------------------------
# ---------------------------------------------------------------------
# line               | объекты, передаваемые в главное окно ChatApp
# file               | когда channel.recieve() отдает сообщение/файл
# connected          | content = сообщение / text = название файла
# user_connected     | connected = разрыв связи / связь поддерживается
#                    | user_connected = соединение с другим пользова-
#                    | телем
# transmission_error | transmission_error = ошибка передачи файла
# -------------------|-------------------------------------------------
# line_recieved      | функции-триггеры
# file_recieved      | line = show_message / file = show_file
# connecting         | функции, проверяющие состояние подключения поль-
# user_connecting    | зователей
#                    | 0 - нет подключения, 1 - соединение установлено
# transmission_failed| функция-триггер ошибки передачи
#
# Определен в channels.py и связан с ChatApp
# ---------------------------------------------------------------------


class PortListener(QtCore.QObject):
    line = QtCore.pyqtSignal(str)
    file = QtCore.pyqtSignal(str)
    connected = QtCore.pyqtSignal(bool)
    user_connected = QtCore.pyqtSignal(bool)
    transmission_error = QtCore.pyqtSignal(str)

    def line_recieved(self, text):
        content = f"{datetime.datetime.now().strftime('%H:%M')} <Собеседник>: {text}"
        self.line.emit(content)

    def file_recieved(self, text):
        self.file.emit(text)

    def connecting(self, state):
        if state == 0:
            self.connected.emit(state)

    def user_connecting(self, state):
        self.user_connected.emit(state)

    def transmission_failed(self):
        content = "Произошла ошибка. Сообщение не было доставлено"
        self.transmission_error.emit(content)
