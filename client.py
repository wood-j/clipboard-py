import asyncio
import json
import os
import sys
import time
import clipboard
from websocket import WebSocketApp
from common.decorators.thread_function import thread_function
from common.decorators.try_except import try_except
from common.log import logger
from common.web_socket_client import SocketClientCallback, SocketClient
from config import Config

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
            if not txt:
                return
            if self._content == txt:
                return
            logger.debug(f'new clipboard content: {txt}')
            self._content = txt
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
            logger.debug(f'set clipboard: {content}')
            self._content = content

    def on_error(self, ws: WebSocketApp, error):
        logger.error(f'web socket error: {error}')

    def on_close(self, ws: WebSocketApp):
        logger.debug(f'web socket closed')
        self.client = None


def run_linux():
    @thread_function()
    def run_client_thread():
        run_client()

    try:
        from PyQt5 import QtWidgets
    except:
        raise Exception(f'"pyqt5" not installed, which is required in linux system')
    run_client_thread()
    app = QtWidgets.QApplication(sys.argv)
    app.exec()


def run_client():
    client = ClipClient()
    client.run()


if __name__ == '__main__':
    if os.name in ('posix',):
        run_linux()
    else:
        run_client()
