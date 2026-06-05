#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/6 00:47
import os
import sys
import json
import subprocess

from auto_script.config import VERSION_DICT, DOWNLOAD_DIR
from auto_script.logger import logger


def load_versions():
    """读取 check_update 记录的 {包名: 版本号}"""
    if not os.path.exists(VERSION_DICT):
        return {}
    with open(VERSION_DICT, encoding='utf-8') as f:
        return json.load(f)


def pip_download(package, version):
    """用当前环境的 pip 下载指定包的 whl 到 DOWNLOAD_DIR"""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    spec = f'{package}=={version}' if version else package
    cmd = [
        sys.executable, '-m', 'pip', 'download', spec,
        '-d', DOWNLOAD_DIR,
        '--only-binary=:all:',  # 只下 whl
        '--no-deps',            # 只下这个包本身,不连带依赖
        # mc-netease-sdk 的 whl 是 py2-none-any(给网易 Py2.7 环境用),
        # 而本脚本跑在 Python3,不指定目标环境的话 pip 会判为不兼容
        # → "from versions: none"。下面四项让 pip 按 py2 目标环境去下,
        # 绕过当前解释器的兼容性检查。
        '--python-version', '2',
        '--implementation', 'py',
        '--abi', 'none',
        '--platform', 'any',
    ]
    logger.info('开始下载 %s 到 %s', spec, DOWNLOAD_DIR)
    logger.info('执行命令: %s', ' '.join(cmd))
    # check_call:非零退出码会抛 CalledProcessError,交给 main 统一处理
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        logger.error('下载失败 %s,退出码 %s', spec, e.returncode)
        raise
    logger.info('下载完成 %s', spec)
    return True


if __name__ == '__main__':
    print(pip_download('mc-netease-sdk', '3.8.0.75808'))
