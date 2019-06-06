import functools
import time
from concurrent.futures import ThreadPoolExecutor


class PoolManager:
    pool = ThreadPoolExecutor(10)


def thread_pool():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pool = PoolManager.pool
            pool.submit(func, *args, **kwargs)
        return wrapper
    return decorator


if __name__ == '__main__':
    @thread_pool()
    def func(key):
        print(f'start: {key}')
        time.sleep(1)
        print(f'end: {key}')

    for i in range(20):
        func(i)
