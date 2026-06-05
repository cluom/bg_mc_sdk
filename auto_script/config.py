#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/6 00:54
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_DICT = os.path.normpath(os.path.join(BASE_DIR, '../.cache/last_version.json'))
DOWNLOAD_DIR = os.path.normpath(os.path.join(BASE_DIR, '../downloads'))
LOG_DIR = os.path.normpath(os.path.join(BASE_DIR, '../logs'))
LOG_FILE = os.path.normpath(os.path.join(LOG_DIR, 'auto_script.log'))
# whl 解压临时存放目录(按版本分子目录),以及最终覆盖的 sdk 目录
TEST_CACHE_DIR = os.path.normpath(os.path.join(BASE_DIR, '../.cache/.test'))
SDK_DIR = os.path.normpath(os.path.join(BASE_DIR, '../sdk'))