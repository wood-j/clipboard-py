import functools
import time
from concurrent.futures import ThreadPoolExecutor


class PoolManager:
    pool = ThreadPoolExecutor(4)

    def set_pool(self, thread_count: int):
        self.pool = ThreadPoolExecutor(thread_count)


def thread_function():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            pool = PoolManager.pool
            pool.submit(func, *args, **kw)
        return wrapper
    return decorator


if __name__ == '__main__':
    @thread_function()
    def func(key):
        print(f'start: {key}')
        time.sleep(1)
        print(f'end: {key}')

    func('1')
    func('2')
    func('3')
    func('4')
    func('5')
