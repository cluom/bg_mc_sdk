#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/6 01:10
import os
import logging
from logging.handlers import RotatingFileHandler

from auto_script.config import LOG_DIR, LOG_FILE, RUN_LOG_FILE

_LOGGER_NAME = 'auto_script'
_RUN_LOGGER_NAME = 'auto_script.daily_run'
_FORMAT = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'


def _build_logger(name, log_file):
    """构造一个控制台 + 文件双输出的 logger（UTF-8、轮转）。

    单文件上限 1MB，保留 5 份历史。已构造过则直接返回（幂等，避免重复加 handler）。
    """
    my_logger = logging.getLogger(name)
    if my_logger.handlers:
        return my_logger
    my_logger.setLevel(logging.INFO)

    os.makedirs(LOG_DIR, exist_ok=True)
    formatter = logging.Formatter(_FORMAT)

    # 文件 handler：UTF-8 落盘，便于留档 / 上传排查
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)

    # 控制台 handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(stream_handler)

    my_logger.propagate = False
    return my_logger


def get_logger(name=_LOGGER_NAME):
    """业务 logger：更新检查/下载/覆盖等过程落盘到 logs/auto_script.log。"""
    return _build_logger(name, LOG_FILE)


def get_run_logger():
    """定时任务"运行心跳"logger：独立落盘到 logs/daily_run.log。

    与业务日志分开——即使本次"无新版本"业务无输出，这里也会记录每次启停，
    方便一眼确认计划任务在正常运行。
    """
    return _build_logger(_RUN_LOGGER_NAME, RUN_LOG_FILE)


logger = get_logger()
