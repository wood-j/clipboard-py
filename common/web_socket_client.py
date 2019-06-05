from abc import abstractmethod
from websocket import WebSocketApp
from common.decorators.try_except import try_except
from common.log import logger


class SocketClientCallback:
    @abstractmethod
    def on_open(self, ws: WebSocketApp):
        pass

    @abstractmethod
    def on_message(self, ws: WebSocketApp, message):
        pass

    @abstractmethod
    def on_error(self, ws: WebSocketApp, error):
        pass

    @abstractmethod
    def on_close(self, ws: WebSocketApp):
        pass


class SocketClient(object):
    def __init__(self, host: str='127.0.0.1', port: int=10000, callback: SocketClientCallback=None, *args, **kwargs):
        self.host = host
        self.port = port
        self.callback = callback
        self.client = None  # type: WebSocketApp

    def run(self):
        self.client = WebSocketApp(
            f"ws://{self.host}:{self.port}",
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, message: self.on_message(ws, message),
            on_error=lambda ws, error: self.on_error(ws, error),
            on_close=lambda ws: self.on_close(ws)
        )
        self.client.run_forever()

    @try_except('send')
    def send_message(self, message):
        self.client.send(message)

    @try_except('on open')
    def on_open(self, ws: WebSocketApp):
        if not self.callback:
            logger.debug(f'web socket connected')
            return
        self.callback.on_open(ws)

    @try_except('on message')
    def on_message(self, ws: WebSocketApp, message):
        if not self.callback:
            logger.debug(f'got response: {message}')
            return
        self.callback.on_message(ws, message)

    @try_except('on error')
    def on_error(self, ws: WebSocketApp, error):
        if not self.callback:
            logger.error(f'web socket error: {error}')
            return
        self.callback.on_error(ws, error)

    @try_except('on close')
    def on_close(self, ws: WebSocketApp):
        if not self.callback:
            logger.debug(f'web socket closed')
            return
        self.callback.on_close(ws)


if __name__ == '__main__':
    client = SocketClient(host='127.0.0.1', port=10000)
    client.run()
