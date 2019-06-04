#  -*- coding: utf-8 -*-
import functools
import inspect

from common.log import logger


def try_except(text: str):
    """ Decorator to wrap code into try except with log.

    Based on try except
    Based on Logging

    :param text: the exception title to show in log file
    :return: return the expected result if no exception, else return None.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                result = func(*args, **kw)
                return result
            except:
                sig = inspect.signature(func)
                arg_str = str(sig.parameters)
                logger.debug(f'function:  {func.__name__}')
                logger.debug(f'signature: {arg_str}')
                logger.debug(f'args:      {str(args)}')
                logger.debug(f'kwargs:    {str(kw)}')
                logger.exception(f'{text}')
                return None
        return wrapper
    return decorator
