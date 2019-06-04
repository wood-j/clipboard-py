from abc import abstractmethod
from threading import Thread
from websocket_server import WebsocketServer, WebSocketHandler
from common.decorators.try_except import try_except
from common.log import logger


class SocketServerCallback:
    @abstractmethod
    def new_client(self, client, server):
        pass

    @abstractmethod
    def client_left(self, client, server):
        pass

    @abstractmethod
    def message_received(self, client, server, message):
        pass


class SocketServer(object):
    def __init__(self, port: int=10000, callback: SocketServerCallback=None):
        self.port = port
        self.callback = callback
        self.server = None  # type: WebsocketServer

    def run(self):
        self.server = WebsocketServer(self.port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()

    @try_except('new client')
    def new_client(self, client, server):
        if not self.callback:
            logger.debug(f'new client: {client}')
            return
        self.callback.new_client(client, server)

    @try_except('new left')
    def client_left(self, client, server):
        if not self.callback:
            logger.debug(f'client left: {client}')
            return
        self.callback.client_left(client, server)

    @try_except('message received')
    def message_received(self, client, server, message):
        if not self.callback:
            b_data = message.encode(encoding='raw_unicode_escape')
            message = b_data.decode()
            logger.debug(f'client id: {client["id"]} request: {message}')
            handler = client['handler']     # type: WebSocketHandler
            handler.send_message(message)
            logger.debug(f'client id: {client["id"]} response: {message}')
            return
        self.callback.message_received(client, server, message)


if __name__ == '__main__':
    server = SocketServer(port=10000, callback=None)
    server.run()
