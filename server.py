import json
import time

from websocket_server import WebSocketHandler

from client import MSG_HEAR_BEAT
from common.decorators.try_except import try_except
from common.log import logger
from common.web_socket_server import SocketServerCallback, SocketServer
from config import Config


class ClipServer(SocketServerCallback):
    def __init__(self):
        self.server = None      # type: SocketServer
        self.dic_clients = {}   # type: dict[str, WebSocketHandler]

    @try_except('server run')
    def run(self):
        conf = Config.load()
        setting = conf.server_setting
        self.server = SocketServer(host=setting.host, port=setting.port, callback=self)
        self.server.run()

    # ===================================================================== SocketServerCallback

    def new_client(self, client, server):
        logger.debug(f'new client: {client}')
        id = client['id']
        handler = client['handler']
        self.dic_clients[id] = handler

    def client_left(self, client, server):
        logger.debug(f'client left: {client}')
        id = client['id']
        del self.dic_clients[id]

    def message_received(self, client, server, message):
        b_data = message.encode(encoding='raw_unicode_escape')
        message = b_data.decode()
        logger.debug(f'client id: {client["id"]} request: {message}')
        client_id = client['id']
        dic = json.loads(message)
        msg_type = dic['method']
        if msg_type == MSG_HEAR_BEAT:
            return
        for id, handler in self.dic_clients.items():
            if id == client_id:
                continue
            handler.send_message(message)


if __name__ == '__main__':
    while 1:
        svc = ClipServer()
        svc.run()
        time.sleep(1)
