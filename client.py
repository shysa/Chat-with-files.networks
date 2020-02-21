import sys
from PyQt5 import QtWidgets
from gui import guimain

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.text_list.addItem('Connection is created...')
        self.factory.window.text_list.addItem('Send the message like \'login:your_name\'')

    def lineReceived(self, line: bytes):
        message = line.decode()
        self.factory.window.text_list.addItem(message)


class Connector(ClientFactory):
    window: 'ChatWindow'
    protocol = ConnectorProtocol

    def __init__(self, app_window):
        self.window = app_window

    def clientConnectionFailed(self, connector, reason):
        self.window.text_list.addItem('Connection failed... Try again later...')

    def clientConnectionLost(self, connector, reason):
        self.window.text_list.addItem('Connection lost... wait or try later...')


class ChatWindow(QtWidgets.QMainWindow, guimain.Ui_MainWindow):
    protocol: ConnectorProtocol
    reactor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.send_button.clicked.connect(self.send_message)

    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        try:
            message = self.message_text.toPlainText()
            if len(message) > 0:
                self.protocol.sendLine(message.encode())
                self.message_text.setText('')
            else:
                self.text_list.addItem('Can\'t send the message: a message is empty')
        except:
            self.text_list.addItem('Can\'t send the message')


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