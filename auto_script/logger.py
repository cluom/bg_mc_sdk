#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/6 01:10
import os
import logging
from logging.handlers import RotatingFileHandler

from auto_script.config import LOG_DIR, LOG_FILE

_LOGGER_NAME = 'auto_script'
_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'


def get_logger(name=_LOGGER_NAME):
    """统一 logger：控制台 + 文件双输出。

    文件落盘到 logs/auto_script.log（UTF-8、轮转），随时可直接上传/分享。
    单文件上限 1MB，保留 5 份历史。
    """
    my_logger = logging.getLogger(name)
    if my_logger.handlers:
        return my_logger
    my_logger.setLevel(logging.INFO)

    os.makedirs(LOG_DIR, exist_ok=True)
    formatter = logging.Formatter(_FORMAT)

    # 文件 handler：UTF-8 落盘，便于留档 / 上传排查
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    # 控制台 handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(stream_handler)

    my_logger.propagate = False
    return my_logger


logger = get_logger()
