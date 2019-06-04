# -*- coding:utf-8 -*-
import logging
import logging.config
import os
import re
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from common.paths import get_data_root


def new_logger(name):
    root = get_data_root()
    log_root = os.path.join(root, 'logs')
    if not os.path.exists(log_root):
        os.makedirs(log_root)
    result = logging.getLogger(name)
    result.setLevel(logging.DEBUG)
    # format
    basic_format = '%(asctime)s %(levelname)s File "%(pathname)s", line %(lineno)s： %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(basic_format, date_format)
    # console stream
    steam_handler = logging.StreamHandler()
    steam_handler.setFormatter(formatter)
    result.addHandler(steam_handler)
    # file stream
    file_name = os.path.join(log_root, f'{name}.log')
    file_handler = TimedRotatingFileHandler(filename=file_name, when="D", interval=1, backupCount=30, encoding='UTF-8')
    # file_handler = TimedRotatingFileHandler(file_name, "M", 1, 10)
    # file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    result.addHandler(file_handler)
    return result


logger = new_logger('clipboard')


if __name__ == '__main__':
    for i in range(120):
        logger.debug('hello world!')
        time.sleep(1)
