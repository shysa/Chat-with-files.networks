import sys
from PyQt5 import QtWidgets, QtCore
from gui import guimain, guireg

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.text_list.addItem('Соединение установлено...')
        self.factory.window.text_list.addItem('Отправьте сообщение вида \'login:your_name\'')

    def lineReceived(self, line: bytes):
        message = line.decode()

        if message.startswith("#USRCNCT"):
            message = message.replace("#USRCNCT", "")
            self.factory.window.user_list.addItem(message)

        elif message.startswith("#USRCLR"):
            self.factory.window.user_list.clear()

        else:
            self.factory.window.text_list.addItem(message)


class Connector(ClientFactory):
    window: 'ChatWindow'
    protocol = ConnectorProtocol

    def __init__(self, app_window):
        self.window = app_window

    def clientConnectionFailed(self, connector, reason):
        self.window.text_list.addItem('Соединение не установлено. Попробуйте позже')

    def clientConnectionLost(self, connector, reason):
        self.window.text_list.addItem('Соединение с сервером потеряно. Попробуйте позже')


class ChatWindow(QtWidgets.QMainWindow, guimain.Ui_MainWindow):
    protocol: ConnectorProtocol
    reactor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.send_button.clicked.connect(self.send_message)
        self.exit_button.clicked.connect(self.close)
        self.file_button.clicked.connect(self.open_dialog)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        try:
            message = self.message_text.toPlainText()
            if len(message) > 0:
                self.protocol.sendLine(message.encode())
                self.message_text.setText('')
            else:
                self.text_list.addItem('Нельзя отправить пустое сообщение')
        except:
            self.text_list.addItem('Невозможно отправить сообщение')

    def open_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        result = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить файл", "",
                                                       "All Files (*);;(*.jpg);;(*.png);;(*.txt)",
                                                       options=options)
        if result:
            print(result)


class RegWindow(QtWidgets.QMainWindow, guireg.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    import qt5reactor
    qt5reactor.install()

    window = ChatWindow()
    window.show()

    from twisted.internet import reactor

    reactor.connectTCP(
        "localhost",
        4000,
        Connector(window)
    )

    window.reactor = reactor
    reactor.run()