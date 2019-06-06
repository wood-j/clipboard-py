import functools
import time
from threading import Thread


def thread_new(key: str= '', daemon=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t = Thread(
                target=lambda: func(*args, **kwargs),
                daemon=daemon
            )
            t.start()
        return wrapper
    return decorator


if __name__ == '__main__':
    @thread_new()
    def func(key):
        print(f'start: {key}')
        time.sleep(1)
        print(f'end: {key}')

    for i in range(10):
        func(i)

    while 1:
        time.sleep(1)
