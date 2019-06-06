import json
import time
import clipboard
from websocket import WebSocketApp
from common.decorators.thread_new import thread_new
from common.decorators.try_except import try_except
from common.log import logger
from common.web_socket_client import SocketClientCallback, SocketClient
from config import Config

MSG_SHARE = 0


class ClipClient(SocketClientCallback):
    def __init__(self):
        self.client = None  # type: SocketClient
        self.connected = False
        self.end = False
        self._content = ''

    @try_except('client run')
    def run(self):
        self.check_clipboard_thread()
        conf = Config.load()
        setting = conf.server_setting
        self.client = SocketClient(host=setting.host, port=setting.port, callback=self)
        self.client.run()
        self.end = True

    @thread_new('check_clipboard_thread')
    def check_clipboard_thread(self):
        @try_except('do_check')
        def do_check():
            txt = clipboard.paste()
            if not txt:
                return
            if self._content == txt:
                return
            logger.debug(f'new clipboard content: {txt}')
            self._content = txt
            if not (self.client and self.connected):
                return
            dic = {
                'method': MSG_SHARE,
                'content': self._content,
            }
            js = json.dumps(dic, ensure_ascii=False, indent=4)
            logger.debug(f'send: {js}')
            self.client.send_message(js)

        while 1:
            if self.end:
                return
            time.sleep(1)
            do_check()

    # =================================================================== SocketClientCallback

    def on_open(self, ws: WebSocketApp):
        logger.debug(f'web socket connected')
        self.connected = True

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
        self.connected = False


def run_client():
    while 1:
        time.sleep(1)
        client = ClipClient()
        client.run()
        logger.debug('end')


if __name__ == '__main__':
    run_client()
