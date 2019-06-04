import json
import sys
import time
import clipboard
from websocket import WebSocketApp
from common.decorators.thread_function import thread_function
from common.decorators.try_except import try_except
from common.log import logger
from common.web_socket_client import SocketClientCallback, SocketClient
from config import Config
from PyQt5 import QtWidgets

MSG_SHARE = 0


class ClipClient(SocketClientCallback):
    def __init__(self):
        self.client = None  # type: SocketClient
        self._content = ''

    def run(self):
        self.check_clipboard_async()
        conf = Config.load()
        setting = conf.server_setting
        while True:
            self.client = SocketClient(host=setting.host, port=setting.port, callback=self)
            self.client.run()

    @thread_function()
    def check_clipboard_async(self):
        @try_except('do check')
        def do_check():
            txt = clipboard.paste()
            if self._content == txt:
                return
            self._content = txt
            logger.debug(f'new clipboard content: {self._content}')
            if not self._content:
                return
            if not self.client:
                return
            dic = {
                'method': MSG_SHARE,
                'content': self._content,
            }
            js = json.dumps(dic, ensure_ascii=False, indent=4)
            logger.debug(f'send: {js}')
            self.client.send_message(js)

        while True:
            do_check()
            time.sleep(1)

    # =================================================================== SocketClientCallback

    def on_open(self, ws: WebSocketApp):
        logger.debug(f'web socket connected')

    def on_message(self, ws: WebSocketApp, message):
        logger.debug(f'got response: {message}')
        if not message:
            return
        dic = json.loads(message)
        code = dic.get('method', -1)
        if code == MSG_SHARE:
            content = dic.get('content', None)
            if not content:
                logger.warning(f'get empty share content')
                return
            if self._content == content:
                return
            clipboard.copy(content)
            self._content = content

    def on_error(self, ws: WebSocketApp, error):
        logger.error(f'web socket error: {error}')

    def on_close(self, ws: WebSocketApp):
        logger.debug(f'web socket closed')
        self.client = None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # @thread_function()
    # def check():
    #     while True:
    #         txt = clipboard.paste()
    #         logger.debug(txt)
    #         time.sleep(1)
    # check()
    # check()
    client = ClipClient()
    client.run()
