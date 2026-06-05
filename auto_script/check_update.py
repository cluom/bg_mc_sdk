#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/5 18:28
import os
import json
import feedparser

from windows_toasts import Toast, WindowsToaster

from auto_script.config import VERSION_DICT
from auto_script.auto_download_whl import pip_download
from auto_script.update_sdk import update_sdk
from auto_script.logger import logger

PACKAGE = 'mc-netease-sdk'  # 换成你要监控的库名
FEED = f'https://pypi.org/rss/project/{PACKAGE}/releases.xml'


def get_latest_version():
    d = feedparser.parse(FEED)
    if not d.entries:
        return None
    # RSS 里 entries[0] 就是最新一条发布,title 通常是版本号
    return d.entries[0].title.strip()


def load_last():
    if os.path.exists(VERSION_DICT):
        with open(VERSION_DICT, encoding='utf-8') as f:
            return json.load(f).get(PACKAGE)
    return None


def save_last(ver):
    data = {}
    if os.path.exists(VERSION_DICT):
        with open(VERSION_DICT, encoding='utf-8') as f:
            data = json.load(f)
    data[PACKAGE] = ver
    with open(VERSION_DICT, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def check_update():
    latest = get_latest_version()
    last = load_last()
    logger.info('当前记录版本: %s, PyPI 最新版本: %s', last, latest)

    if latest and latest != last:
        logger.info('发现新版本 %s -> %s,开始下载并安装', last, latest)
        toaster = WindowsToaster('检查更新')  # 这个名字会显示为通知来源
        toast = Toast()
        toast.text_fields = ['网易SDK有新版本!', f'{last} -> {latest}']
        toaster.show_toast(toast)
        pip_download(PACKAGE, latest)
        update_sdk(PACKAGE, latest)
        save_last(latest)
        logger.info('版本记录已更新为 %s', latest)
    else:
        logger.info('无新版本,跳过')


if __name__ == '__main__':
    check_update()
