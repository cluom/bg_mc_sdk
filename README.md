# bg_mc_sdk

> 网易我的世界 ModSDK（`mc-netease-sdk`）的 **Python 3 补全库**——让你在 PyCharm 等现代 IDE 里写网易 Mod 时，拥有完整的类型提示、跳转和自动补全。

## 这是什么 / 为什么需要它

网易官方的 `mc-netease-sdk` 是为 **Python 2.7** 运行环境打包的，它的存根（stub）有几个问题，导致在 Python 3 的 IDE 里开发体验很差：

- **返回类型写成带引号的前向引用**（`# type: () -> 'Type[BaseComponent]'`），PyCharm 无法解析，点不动、补不全；
- **部分类缺少关键方法签名**（如 `ScreenNode.__init__`、`NativeScreenManager.instance()`），调用时 IDE 报参数不匹配或识别不出返回类型；
- 直接 `pip install mc-netease-sdk` 在 Python 3 环境会因 `py2-none-any` 标记被判为不兼容。

`bg_mc_sdk` 把官方 SDK 自动加工成 **Python 3 友好的纯补全库**：去掉返回类型引号、补齐缺失签名、剔除打包元数据，让你在 IDE 里获得和官方 API 一致、且能正常跳转/补全的开发体验。

> ⚠️ 本库**仅用于开发期的代码补全与类型提示**，不包含任何引擎实现，不能在运行时替代游戏内的真实 SDK。真正的逻辑仍由网易客户端在 Mod 运行时提供。

## 安装

```shell
pip install bg_mc_sdk
```

## 在 IDE 中使用

安装后，照常按官方写法 import 即可，IDE 会自动识别类型：

```python
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.minecraftEnum import AttrType

# 此时 PyCharm 能正确补全 / 跳转 / 显示返回类型
comp = serverApi.GetEngineCompFactory().CreateAttr(player_id)
comp.GetAttrValue(AttrType.HEALTH)
```

## 相比官方 SDK 做了哪些处理

| 处理 | 说明 |
|------|------|
| **去返回类型引号** | `-> 'Xxx'` → `-> Xxx`，PyCharm 才能解析返回类型、支持链式补全 |
| **补缺失签名** | 给 `ScreenNode` 补 `__init__(self, namespace, name, param)`、给 `NativeScreenManager` 补 `instance()` 等官方 stub 遗漏的方法 |
| **剔除打包元数据** | 移除 whl 自带的 `*.dist-info`，只保留纯源码 stub |
| **版本号同步** | `sdk/bg/__init__.py` 的 `__version__` 跟随官方 SDK 版本 |

## 自动更新机制

`auto_script/` 下是一套自动维护脚本，定期把官方新版 SDK 同步过来：

```
检测 PyPI 新版 → 下载官方 whl → 解压 → 去 dist-info → 去返回类型引号
  → 补缺失签名(ScreenNode / NativeScreenManager ...) → 覆盖 sdk/
  → 同步 bg 版本号 → 自动 commit & push
```

发现新的缺失签名时，只需把对应补丁加进 `update_sdk.py` 的处理链（幂等），下次更新会自动应用、不会被官方内容覆盖冲掉。

## 版本号

版本号直接跟随网易官方 SDK，形如 `3.8.0.75809`，方便对照官方版本。

## 致谢与许可

- 本库的 stub 内容来源于网易官方 [`mc-netease-sdk`](https://pypi.org/project/mc-netease-sdk/)，其以 **MIT 协议**开源；`bg_mc_sdk` 在此基础上做 Python 3 适配加工，同样以 **MIT 协议**发布，并保留原作者版权声明。
- 项目地址：<https://github.com/cluom/bg_mc_sdk>
