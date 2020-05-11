import sys
import datetime
import os
from PyQt5 import QtGui, QtCore, QtWidgets

from gui import window
from utils import info_dialog

import phizical
import channel


# ----------------------- ChatApp ---------------------------
# -- класс главного окна | gui/window.py, gui/ui/window.ui --
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
# port_listener     определен в channel.py - сигнализирует
#                   о пришедшем сообщении/файле в гл. окно
# -----------------------------------------------------------


class ChatApp(QtWidgets.QMainWindow, window.Ui_MainWindow):
    # setupUI           инициализирует графические элементы интерфейса
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()
        self.init_toolbar()
        self.infoDialog = None
        self.statusBar.showMessage("Чтобы установить соединение и начать работу, нажмите Подключиться")

    # init_handlers     связывает кнопки с обработчиками, какие функции вызываются при нажатии
    def init_handlers(self):
        self.bSend.clicked.connect(self.send_message)
        self.bSend.setAutoDefault(True)
        self.message.returnPressed.connect(self.bSend.click)
        self.bSendFile.clicked.connect(self.open_dialog)
        self.textList.itemDoubleClicked.connect(self.save_dialog)

    # init_toolbar      связывает элементы тулбара с обработчиками (подключение, выход, информация)
    def init_toolbar(self):
        self.mExit.triggered.connect(self.close_connection)
        self.mConnect.triggered.connect(self.init_connection)
        self.mInfo.triggered.connect(self.create_dialog)

    # closeEvent        переопределение события close (X)
    def closeEvent(self, event: QtGui.QCloseEvent):
        self.close_connection()
        event.accept()

    # close_connection  закрытие содениния и портов
    def close_connection(self):
        self.statusBar.showMessage("Отключение...")
        phizical.ser_close()
        print("Connection closed")
        QtWidgets.qApp.quit()

    # init_connection   открытие портов, установка соединения, запуск прослушки портов
    def init_connection(self):
        try:
            phizical.portinit()
            phizical.ser_open()
            phizical.ser_read()
            print("Connection open! Start reading")
            self.show_service("Соединение установлено")
            self.statusBar.showMessage("Соединено")
            self.listen()
        except:
            self.show_service("Невозможно установить соединение")

    # create_dialog     показ окна Информации
    def create_dialog(self):
        if not self.infoDialog:
            self.infoDialog = info_dialog.InfoDialog()
        self.infoDialog.show()

    # send_message      отправка сообщения, очистка окна
    def send_message(self):
        try:
            message = self.message.text()
            if len(message) > 0:
                content = f"{datetime.datetime.now().strftime('%H:%M')} <Вы>: {message}"

                phizical.ser_write(channel.send(message))
                self.show_message(content)

                self.message.clear()
            else:
                self.show_service('Нельзя отправить пустое сообщение')
        except:
            self.show_service('Невозможно отправить сообщение')

    # open_dialog       открытие модального диалогового окна выбора файла для отправки, отправка файла
    def open_dialog(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить файл", "")[0]
        if filepath:
            try:
                f = QtCore.QFileInfo(filepath)
                print(f.absolutePath())

                phizical.ser_write(channel.send_file(f.absoluteFilePath()))
                self.show_file(f.fileName())
            except:
                self.show_service('Невозможно прикрепить файл')

    # save_dialog       открытие модального диалогового окна выбора директории для сохранения скачиваемого файла
    def save_dialog(self):
        item = self.textList.currentItem()
        file_name = item.text()

        if item.data(QtCore.Qt.UserRole) == 1:
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать папку для сохранения", "")
            if directory:
                new_dir = directory + '/' + file_name
                if not os.path.isfile(new_dir):
                    os.replace("../downloads/"+file_name, new_dir)
                else:
                    i = 1
                    new_file_name = file_name[:file_name.rfind('.')] +\
                                    '(' + str(i) + ')' + file_name[file_name.rfind('.'):]
                    new_dir = directory + '/' + new_file_name
                    while os.path.isfile(new_dir):
                        new_file_name = file_name[:file_name.rfind('.')] +\
                                        '(' + str(i) + ')' + file_name[file_name.rfind('.'):]
                        new_dir = directory + '/' + new_file_name
                        i = i + 1
                    else:
                        os.replace("../downloads/" + file_name, new_dir)

                print(directory, file_name)

    # show_service      добавление служебного сообщения (об ошибке) в основное окно
    def show_service(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        item.setForeground(QtGui.QColor(27, 151, 243))
        self.textList.addItem(item)
        self.textList.scrollToBottom()

    # show_message      добавление нового сообщения в основное окно
    @QtCore.pyqtSlot(str)
    def show_message(self, content):
        item = QtWidgets.QListWidgetItem()
        item.setText(content)
        self.textList.addItem(item)
        self.textList.scrollToBottom()

    # show_file         добавление строки файла в основное окно
    @QtCore.pyqtSlot(str)
    def show_file(self, content):
        iconfile = QtGui.QIcon('../gui/icon/download.png')

        item = QtWidgets.QListWidgetItem()
        item.setIcon(iconfile)
        item.setText(content)
        item.setData(QtCore.Qt.UserRole, 1)

        self.textList.addItem(item)
        self.textList.setIconSize(QtCore.QSize(32, 32))
        self.textList.scrollToBottom()

    # listen            создает объект port_listener в главном окне (связующее звено с канальным уров-
    #                   нем), и связывает сигналы [line - получено сообщение, file - получен файл] с
    #                   show_message и show_file
    def listen(self):
        self.port_listener = channel.plistener
        self.port_listener.line.connect(self.show_message)
        self.port_listener.file.connect(self.show_file)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)      # Новый экземпляр QApplication
    window = ChatApp()                          # Создает объект
    window.show()                               # Показывает окно
    sys.exit(app.exec_())                       # и запускает приложение
