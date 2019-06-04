from websocket_server import WebSocketHandler
from common.log import logger
from common.web_socket_server import SocketServerCallback, SocketServer
from config import Config


class ClipServer(SocketServerCallback):
    def __init__(self):
        self.server = None      # type: SocketServer
        self.dic_clients = {}   # type: dict[str, WebSocketHandler]

    def run(self):
        conf = Config.load()
        setting = conf.server_setting
        while True:
            self.server = SocketServer(port=setting.port, callback=self)
            self.server.run()

    # ===================================================================== SocketServerCallback

    def new_client(self, client, server):
        logger.debug('new client: {client}')
        id = client['id']
        handler = client['handler']
        self.dic_clients[id] = handler

    def client_left(self, client, server):
        logger.debug(f'client left: {client}')
        id = client['id']
        del self.dic_clients[id]

    def message_received(self, client, server, message):
        logger.debug(f'client id: {client["id"]} request: {message}')
        client_id = client['id']
        for id, handler in self.dic_clients.items():
            if id == client_id:
                continue
            handler.send_message(message)


if __name__ == '__main__':
    svc = ClipServer()
    svc.run()
