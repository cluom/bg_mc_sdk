#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : cluom
# @Email : cluom@outlook.com
# @Time : 2026/6/6 01:20
import os
import re
import shutil
import zipfile
import subprocess

from auto_script.config import DOWNLOAD_DIR, TEST_CACHE_DIR, SDK_DIR
from auto_script.logger import logger

# 匹配 type comment 的返回类型前向引用: -> 'Xxx'  (单引号包裹的类型)
_RETURN_QUOTE_RE = re.compile(r"->\s*'([^']*)'")

# ScreenNode 缺 __init__ 签名,子类 super().__init__ 时 IDE 报参数不匹配,需补一个
_SCREEN_NODE_REL = os.path.join('mod', 'client', 'ui', 'screenNode.py')
_SCREEN_NODE_ANCHOR = 'class ScreenNode(object):\n'
_SCREEN_NODE_INIT = (
    '    def __init__(self, namespace, name, param):\n'
    '        pass\n\n'
)

# sdk/bg 是本仓库自带包(不在 whl 内,overwrite_sdk 不覆盖它),
# 单独把它的 __version__ 同步成本次更新的 SDK 版本号
_BG_INIT_REL = os.path.join('bg', '__init__.py')
_VERSION_RE = re.compile(r"^(__version__\s*=\s*)['\"][^'\"]*['\"]", re.MULTILINE)

# NativeScreenManager 缺 instance() 单例入口,clientApi.GetNativeScreenManagerCls().instance()
# 在 IDE 里无法识别,需补一个静态方法(注意该文件用 Tab 缩进)
_NSM_REL = os.path.join('mod', 'client', 'ui', 'NativeScreenManager.py')
_NSM_ANCHOR = 'class NativeScreenManager(object):\n'
_NSM_INSTANCE = (
    '\t@staticmethod\n'
    '\tdef instance():\n'
    '\t\t# type: () -> NativeScreenManager\n'
    '\t\tpass\n'
)


def find_whl(package, version):
    """在 DOWNLOAD_DIR 中按版本号定位对应的 whl 文件。

    whl 文件名形如 mc_netease_sdk-3.8.0.75808-py2-none-any.whl,
    包名里的 '-' 在 whl 中会被规范成 '_',这里两种写法都匹配。
    """
    norm = package.replace('-', '_')
    if not os.path.isdir(DOWNLOAD_DIR):
        return None
    for name in os.listdir(DOWNLOAD_DIR):
        if not name.endswith('.whl'):
            continue
        if version in name and (norm in name or package in name):
            return os.path.join(DOWNLOAD_DIR, name)
    return None


def extract_whl(whl_path, version):
    """把 whl(本质是 zip)解压到 .cache/.test/<version>/ 临时存放,返回该目录。

    每次解压前先清空同版本目录,保证是干净的解压结果。
    """
    extract_dir = str(os.path.join(TEST_CACHE_DIR, version))
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir)
    with zipfile.ZipFile(whl_path) as z:
        z.extractall(extract_dir)
    # 删除 whl 自带的 *.dist-info 元数据目录(如 mc_netease_sdk-3.8.0.75808.dist-info),
    # 这是 pip 打包的版本/记录信息,不属于 sdk 源码,临时目录里直接清掉
    for name in os.listdir(extract_dir):
        full = os.path.join(extract_dir, name)
        if os.path.isdir(full) and name.endswith('.dist-info'):
            shutil.rmtree(full)
            logger.info('已删除元数据目录 %s', name)
    logger.info('whl 已解压到临时目录 %s', extract_dir)
    return extract_dir


def strip_return_quotes(extract_dir):
    """去掉 type comment 返回类型的引号: -> 'Xxx' => -> Xxx。

    网易 stub 的返回类型写成前向引用字符串(如 # type: () -> 'Type[BaseComponent]'),
    PyCharm 解析这种带引号的返回类型时无法跳转/补全,去掉引号后能正常识别,
    从而让这个 py2 SDK 在 py3 IDE 里能被正常引用。
    遍历临时目录所有 .py(UTF-8,含中文 docstring)逐文件替换。
    """
    total = 0
    files = 0
    for root, _, names in os.walk(extract_dir):
        for n in names:
            if not n.endswith('.py'):
                continue
            path = os.path.join(str(root), str(n))
            with open(path, encoding='utf-8') as f:
                content = f.read()
            new_content, cnt = _RETURN_QUOTE_RE.subn(r'-> \1', content)
            if cnt:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                total += cnt
                files += 1
    logger.info('已去除返回类型引号,涉及 %d 个文件共 %d 处', files, total)
    return total


def patch_screen_node(extract_dir):
    """给 ScreenNode 补一个 __init__(self, namespace, name, param) 空实现。

    官方 stub 的 ScreenNode 没有 __init__,子类写
    ScreenNode.__init__(self, namespace, name, param) 时 PyCharm 报参数不匹配。
    在 class 声明后插入空 __init__,让 IDE 识别构造签名。已有则跳过(幂等)。
    """
    path = os.path.join(extract_dir, _SCREEN_NODE_REL)
    if not os.path.exists(path):
        logger.warning('未找到 %s,跳过 ScreenNode 补丁', _SCREEN_NODE_REL)
        return False
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'def __init__' in content:
        logger.info('ScreenNode 已有 __init__,跳过补丁')
        return False
    if _SCREEN_NODE_ANCHOR not in content:
        logger.warning('未找到 ScreenNode 类声明,跳过补丁')
        return False
    content = content.replace(
        _SCREEN_NODE_ANCHOR, _SCREEN_NODE_ANCHOR + _SCREEN_NODE_INIT, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info('已给 ScreenNode 补 __init__')
    return True


def patch_native_screen_manager(extract_dir):
    """给 NativeScreenManager 补一个 instance() 静态方法。

    官方 stub 缺这个单例入口,clientApi.GetNativeScreenManagerCls().instance()
    在 IDE 里无法识别返回类型。追加到类(文件)末尾,返回类型标注为
    NativeScreenManager,让链式调用可补全。已有则跳过(幂等)。
    该文件只有 NativeScreenManager 一个类且延伸到文件末尾,所以追加到文件末尾
    即追加到类末尾;插入内容用 Tab 缩进与原文件一致。
    """
    path = os.path.join(extract_dir, _NSM_REL)
    if not os.path.exists(path):
        logger.warning('未找到 %s,跳过 NativeScreenManager 补丁', _NSM_REL)
        return False
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'def instance' in content:
        logger.info('NativeScreenManager 已有 instance,跳过补丁')
        return False
    if _NSM_ANCHOR not in content:
        logger.warning('未找到 NativeScreenManager 类声明,跳过补丁')
        return False
    # 追加到类末尾:去掉尾部空行后空一行再接 instance
    content = content.rstrip('\n') + '\n\n' + _NSM_INSTANCE
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info('已给 NativeScreenManager 补 instance')
    return True


def overwrite_sdk(extract_dir):
    """把临时目录里的内容(排除 *.dist-info 元数据)覆盖到 sdk/ 目录。

    按顶层条目逐个替换:目录先删旧再整体拷贝,文件直接覆盖。
    这样旧版本里已删除的文件也会被清掉,而不仅是叠加。
    """
    os.makedirs(SDK_DIR, exist_ok=True)
    # 先清理 sdk 下遗留的 *.dist-info(历史手动解压带进来的元数据),sdk 里不该有
    for name in os.listdir(SDK_DIR):
        full = os.path.join(SDK_DIR, name)
        if os.path.isdir(full) and name.endswith('.dist-info'):
            shutil.rmtree(full)
            logger.info('清理 sdk 遗留元数据目录: %s', name)
    count = 0
    for name in os.listdir(extract_dir):
        if name.endswith('.dist-info'):
            continue
        src = str(os.path.join(extract_dir, name))
        dst = str(os.path.join(SDK_DIR, name))
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        count += 1
        logger.info('覆盖 sdk 条目: %s', name)
    logger.info('已覆盖 sdk 目录 %s,共 %d 个顶层条目', SDK_DIR, count)
    return count


def bump_bg_version(version):
    """把 sdk/bg/__init__.py 的 __version__ 更新成当前 SDK 版本号。

    bg 包不在 whl 内,不会被 overwrite_sdk 覆盖,需要单独同步,
    作为本仓库 stub 当前对应的官方 SDK 版本标识。
    """
    path = os.path.join(SDK_DIR, _BG_INIT_REL)
    if not os.path.exists(path):
        logger.warning('未找到 %s,跳过版本号更新', path)
        return False
    with open(path, encoding='utf-8') as f:
        content = f.read()
    new_content, cnt = _VERSION_RE.subn(
        lambda m: "%s'%s'" % (m.group(1), version), content)
    if not cnt:
        logger.warning('%s 中未找到 __version__,跳过', path)
        return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    logger.info('已更新 bg 版本号为 %s', version)
    return True


def commit_and_push_sdk(version):
    """把 sdk/ 的修改和新增提交为 bg_mc_sdk-<version> 并推送到远程。

    只针对 sdk/ 路径提交,不裹挟 auto_script/ 等其它改动;
    sdk 无改动时跳过(不会产生空提交)。
    """
    repo_root = os.path.dirname(SDK_DIR)
    try:
        subprocess.check_call(['git', 'add', '--', SDK_DIR], cwd=repo_root)
        # diff --cached --quiet: 0 表示无暂存改动,有改动才提交
        if subprocess.call(
                ['git', 'diff', '--cached', '--quiet', '--', SDK_DIR],
                cwd=repo_root) == 0:
            logger.info('sdk 目录无改动,跳过 commit')
            return False
        msg = 'bg_mc_sdk-%s' % version
        subprocess.check_call(['git', 'commit', '-m', msg, '--', SDK_DIR], cwd=repo_root)
        logger.info('已提交 sdk 改动: %s', msg)
        subprocess.check_call(['git', 'push'], cwd=repo_root)
        logger.info('已推送到远程')
        return True
    except subprocess.CalledProcessError as e:
        logger.error('git 操作失败,退出码 %s', e.returncode)
        return False


def update_sdk(package, version):
    """完整流程:把官方 py2 whl 处理成本地可被 py3 IDE 引用的 sdk 库并更新。

    定位 whl -> 解压到临时目录 -> 删元数据 -> 去返回类型引号 -> 覆盖 sdk/。
    """
    whl_path = find_whl(package, version)
    if not whl_path:
        logger.error('未在 %s 找到 %s==%s 的 whl 文件', DOWNLOAD_DIR, package, version)
        return False
    logger.info('找到 whl: %s', whl_path)
    extract_dir = extract_whl(whl_path, version)
    strip_return_quotes(extract_dir)
    patch_screen_node(extract_dir)
    patch_native_screen_manager(extract_dir)
    overwrite_sdk(extract_dir)
    bump_bg_version(version)
    # 覆盖完成后清理临时解压目录,临时文件用完即删
    shutil.rmtree(extract_dir, ignore_errors=True)
    logger.info('已清理临时目录 %s', extract_dir)
    commit_and_push_sdk(version)
    logger.info('sdk 已更新到 %s==%s', package, version)
    return True


if __name__ == '__main__':
    print(update_sdk('mc-netease-sdk', '3.8.0.75808'))
