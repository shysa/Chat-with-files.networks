from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver

import datetime


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def connectionLost(self, reason=connectionDone):
        try:
            self.factory.clients.remove(self)
            self.factory.connections.remove(self.login)

            #for user in self.factory.clients:
                #user.send_clients(self)
        except:
            pass

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.login is not None:
            content = f"{datetime.datetime.now().strftime('%H:%M')} <{self.login}>: {content}"

            self.factory.history.append(content)

            for user in self.factory.clients:
                user.sendLine(content.encode())
        else:
            # login:admin -> admin
            if content.startswith("login:"):
                login = content.replace("login:", "")

                for user in self.factory.clients:
                    if user.login == login:
                        self.sendLine("Логин уже занят! Попробуйте придумать другой.".encode())
                        return

                self.login = login
                self.factory.connections.append(login)

                self.factory.clients.append(self)
                self.factory.send_history(self)

                #for user in self.factory.clients:
                self.factory.send_clients(self)
            else:
                self.sendLine("Вы не авторизованы и не можете отправлять сообщения.".encode())


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list
    history: list

    connections: list

    def startFactory(self):
        self.clients = []
        self.history = []
        self.connections = []
        print("Сервер запущен")

    def stopFactory(self):
        print("Сервер выключен")

    def send_history(self, client: ServerProtocol):
        client.sendLine("Дратути!".encode())

        last_messages = self.history[-10:]

        for msg in last_messages:
            client.sendLine(msg.encode())

    def send_clients(self, client: ServerProtocol):
        clients_list = ["#USRCNCT" + usr for usr in self.connections]

        USRCLRmessage = "#USRCLR"
        client.sendLine(USRCLRmessage.encode())

        for usr in clients_list:
            client.sendLine(usr.encode())


if __name__ == '__main__':
    reactor.listenTCP(4000, Server())
    reactor.run()