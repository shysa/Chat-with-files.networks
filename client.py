import sys
import datetime
from PyQt5 import QtGui, QtCore, QtWidgets

from gui import window
from gui.utils import info_dialog

import phizical
import channel


# ----------------------- ChatApp ---------------------------
# -- класс главного окна | gui/window.py, gui/ui/window.ui --
# -----------------------------------------------------------
# Функции:
# setupUI           инициализирует элементы интерфейса
# init_handlers     связывает кнопки с обработчиками, какие
#                   функции вызываются при нажатии
# init_toolbar      связывает элементы тулбара с обработчи-
#                   ками (подключение, выход, информация)
# close_connection  закрытие содениния и портов
# init_connection   открытие портов, установка соединения
# create_dialog     вызов окна Информации
# send_message      отправка сообщения, очистка окна
# open_dialog       открытие модального диалогового окна вы-
#                   бора файла для отправки, отправка файла
# save_dialog       открытие модального диалогового окна вы-
#                   бора директории для сохранения скачивае-
#                   мого файла
# show_service      добавление служебного сообщения (об
#                   ошибке) в основное окно
# show_message      добавление нового сообщения в основное
#                   окно
# show_file         добавление строки файла в основное окно
# -----------------------------------------------------------
# Переменные:
# infoDialog        модальное диалоговое окно информации
# bSend             кнопка Отправить (сообщение)
# bSendFile         кнопка Выбрать файл (и отправить)
# textList          основное окно с сообщениями и файлами
# mExit             кнопка тулбара Выход
# mConnect          кнопка тулбара Подключиться
# mInfo             кнопка тулбара Информация
# message           окно набора текстового сообщения
# -----------------------------------------------------------


class ChatApp(QtWidgets.QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()
        self.init_toolbar()
        self.infoDialog = None

    def init_handlers(self):
        self.bSend.clicked.connect(self.send_message)
        self.bSend.setAutoDefault(True)
        self.message.returnPressed.connect(self.bSend.click)
        self.bSendFile.clicked.connect(self.open_dialog)
        self.textList.itemDoubleClicked.connect(self.save_dialog)

    def init_toolbar(self):
        self.mExit.triggered.connect(self.close_connection)
        self.mConnect.triggered.connect(self.init_connection)
        self.mInfo.triggered.connect(self.create_dialog)

    def close_connection(self):
        print("Connection closed")
        QtWidgets.qApp.quit()

    def init_connection(self):
        try:
            phizical.ser_open()
            phizical.ser_read()
            print("Connection open! Start reading")
            self.show_service("Соединение установлено")
        except:
            self.show_service("Невозможно установить соединение")

    def create_dialog(self):
        if not self.infoDialog:
            self.infoDialog = info_dialog.InfoDialog()
        self.infoDialog.show()

    def send_message(self):
        try:
            message = self.message.text()
            if len(message) > 0:
                # TODO: как сделать разные надписи для машины1 и машины2?
                # TODO: как словить приход? :D точнее, как понять когда пинать и вызывать receive, мне же еще надо на
                #  принимаемой стороне вызывать show_message/file
                content = f"{datetime.datetime.now().strftime('%H:%M')} <Вы>: {message}"

                phizical.ser_write(channel.send(content))
                self.show_message(content)

                self.message.clear()
            else:
                self.show_service('Нельзя отправить пустое сообщение')
        except:
            self.show_service('Невозможно отправить сообщение')

    def open_dialog(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить файл", "")[0]
        if filepath:
            try:
                f = QtCore.QFileInfo(filepath)
                print(f.absoluteFilePath())

                phizical.ser_write(channel.send_file(f.absoluteFilePath()))
                self.show_file(f.fileName())
            except:
                self.show_service('Невозможно прикрепить файл')

    def save_dialog(self):
        item = self.textList.currentItem()

        if item.data(QtCore.Qt.UserRole) == 1:
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать папку для сохранения", "")
            if directory:
                print(directory)

            # TODO: указывать полученную директорию
            # channel.receive()

    def show_service(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        item.setForeground(QtGui.QColor(27, 151, 243))
        self.textList.addItem(item)

    def show_message(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        self.textList.addItem(item)

    def show_file(self, content):
        iconfile = QtGui.QIcon('gui/icon/download.png')

        item = QtWidgets.QListWidgetItem()
        item.setIcon(iconfile)
        item.setText(content)
        item.setData(QtCore.Qt.UserRole, 1)

        self.textList.addItem(item)
        self.textList.setIconSize(QtCore.QSize(32, 32))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ChatApp()  # Создаём объект
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение
