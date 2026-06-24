#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
r"""定时任务入口：供 Windows 计划任务直接调用。

为什么单独有这个文件，而不是让计划任务直接跑 check_update.py：

1. 修正 sys.path。计划任务用 `pythonw.exe auto_script\run_daily.py` 这种
   "脚本路径直接启动"的方式时，Python 会把 auto_script\ 目录（而非仓库根）
   放进 sys.path[0]，导致 `from auto_script.config import ...` 直接
   ModuleNotFoundError 崩溃——崩在 import 阶段，连日志都来不及打。
   这里在 import 任何 auto_script 包之前，先把仓库根插到 sys.path 最前，
   无论从哪个 cwd / 怎么启动都能正常 import。

2. 独立的"运行心跳"日志。check_update 的业务日志（logs/auto_script.log）
   只在"有新版本"时才有大量输出；这里用 logs/daily_run.log 单独记录
   每次启停 / 耗时 / 退出码 / 异常，即使本次无新版本也留痕，方便确认
   定时任务到底有没有在跑。

3. 兜底捕获异常。check_update 抛任何异常都写进心跳日志，绝不静默崩溃。
"""
import os
import sys
import time
import traceback

# 仓库根 = 本文件的上上级目录（auto_script/run_daily.py -> 仓库根）。
# 必须在 import auto_script 包之前插入，否则脚本路径启动时根本 import 不到。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from auto_script.logger import get_run_logger
from auto_script.check_update import check_update

run_logger = get_run_logger()


def main():
    start = time.time()
    run_logger.info('===== 定时任务启动 (pid=%s) =====', os.getpid())
    try:
        check_update()
    except Exception:
        run_logger.error('定时任务异常退出：\n%s', traceback.format_exc())
        run_logger.info('===== 定时任务结束（失败）耗时 %.2fs =====', time.time() - start)
        return 1
    run_logger.info('===== 定时任务结束（成功）耗时 %.2fs =====', time.time() - start)
    return 0


if __name__ == '__main__':
    sys.exit(main())
