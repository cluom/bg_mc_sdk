# -*- coding: utf-8 -*-

from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from mod.client.ui.controls.neteaseComboBoxUIControl import NeteaseComboBoxUIControl
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl
from typing import Tuple
from mod.client.ui.controls.selectionWheelUIControl import SelectionWheelUIControl
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from mod.client.ui.controls.sliderUIControl import SliderUIControl

class BaseUIControl():
    def SetPosition(self, pos):
        # type: (Tuple[float,float]) -> None
        """
        设置控件相对父节点的坐标
        """
        pass

    def SetFullSize(self, axis, paramDict):
        # type: (str, dict) -> bool
        """
        设置控件的大小，支持比例形式以及绝对值
        """
        pass

    def GetFullSize(self, axis):
        # type: (str) -> dict
        """
        获取控件的大小，支持百分比以及绝对值
        """
        pass

    def SetFullPosition(self, axis, paramDict):
        # type: (str, dict) -> bool
        """
        设置控件的锚点坐标（全局坐标），支持比例值以及绝对值
        """
        pass

    def GetFullPosition(self, axis):
        # type: (str) -> dict
        """
        获取控件的锚点坐标，支持比例值以及绝对值
        """
        pass

    def SetAnchorFrom(self, anchorFrom):
        # type: (str) -> bool
        """
        设置控件相对于父节点的锚点
        """
        pass

    def GetAnchorFrom(self):
        # type: () -> str
        """
        判断控件相对于父节点的哪个锚点来计算位置与大小
        """
        pass

    def SetAnchorTo(self, anchorTo):
        # type: (str) -> bool
        """
        设置控件自身锚点位置
        """
        pass

    def GetAnchorTo(self):
        # type: () -> str
        """
        获取控件自身锚点位置信息
        """
        pass

    def SetClipOffset(self, clipOffset):
        # type: (Tuple[float,float]) -> bool
        """
        设置控件的裁剪偏移信息
        """
        pass

    def GetClipOffset(self):
        # type: () -> Tuple[float,float]
        """
        获取控件的裁剪偏移信息
        """
        pass

    def SetClipsChildren(self, clipsChildren):
        # type: (bool) -> bool
        """
        设置控件是否开启裁剪内容
        """
        pass

    def GetClipsChildren(self):
        # type: () -> bool
        """
        根据控件路径返回某控件是否开启裁剪内容
        """
        pass

    def SetMaxSize(self, maxSize):
        # type: (Tuple[float,float]) -> bool
        """
        设置控件所允许的最大的大小值
        """
        pass

    def GetMaxSize(self):
        # type: () -> Tuple[float,float]
        """
        获取控件所允许的最大的大小值
        """
        pass

    def SetMinSize(self, minSize):
        # type: (Tuple[float,float]) -> bool
        """
        设置控件所允许的最小的大小值
        """
        pass

    def GetMinSize(self):
        # type: () -> Tuple[float,float]
        """
        获取控件所允许的最小的大小值
        """
        pass

    def GetPosition(self):
        # type: () -> Tuple[float,float]
        """
        获取控件相对父节点的坐标
        """
        pass

    def GetGlobalPosition(self):
        # type: () -> Tuple[float,float]
        """
        获取控件全局坐标
        """
        pass

    def SetSize(self, size, resizeChildren=False):
        # type: (Tuple[float,float], bool) -> None
        """
        设置控件的大小
        """
        pass

    def GetSize(self):
        # type: () -> Tuple[float,float]
        """
        获取控件的大小
        """
        pass

    def SetVisible(self, visible, forceUpdate=True):
        # type: (bool, bool) -> None
        """
        根据控件路径选择是否显示某控件，可以通过传入空字符串（""）的方式来调整整个JSON的显示/隐藏
        """
        pass

    def GetVisible(self):
        # type: () -> bool
        """
        根据控件路径返回某控件是否已显示
        """
        pass

    def SetTouchEnable(self, enable):
        # type: (bool) -> None
        """
        设置控件是否可点击交互
        """
        pass

    def SetAlpha(self, alpha):
        # type: (float) -> None
        """
        设置节点的透明度，仅对image和label控件生效
        """
        pass

    def SetLayer(self, layer, syncRefresh=True, forceUpdate=True):
        # type: (int, bool, bool) -> None
        """
        设置控件节点的层级，可以通过传入空字符串（""）的方式来调整整个JSON的基础层级
        """
        pass

    def GetPath(self):
        # type: () -> str
        """
        返回当前控件的相对路径，路径从画布节点开始算起
        """
        pass

    def GetChildByName(self, childName):
        # type: (str) -> BaseUIControl
        """
        根据子控件的名称获取BaseUIControl实例
        """
        pass

    def GetChildByPath(self, childPath):
        # type: (str) -> BaseUIControl
        """
        根据相对路径获取BaseUIControl实例
        """
        pass

    def resetAnimation(self):
        # type: () -> None
        """
        重置该控件的动画
        """
        pass

    def PauseAnimation(self, propertyName='all'):
        # type: (str) -> bool
        """
        暂停动画，暂停后的动画会停在当前的状态
        """
        pass

    def PlayAnimation(self, propertyName='all'):
        # type: (str) -> bool
        """
        继续播放动画，从动画当前状态开始播放
        """
        pass

    def StopAnimation(self, propertyName='all'):
        # type: (str) -> bool
        """
        停止动画，动画将恢复到第一段动画片段的from状态
        """
        pass

    def SetAnimation(self, propertyName, namespace, animName, autoPlay=False):
        # type: (str, str, str, bool) -> bool
        """
        给单一属性设置动画，已有重复的会设置失败，需要先remove
        """
        pass

    def RemoveAnimation(self, propertyName):
        # type: (str) -> bool
        """
        删除单一属性的动画，删除后的值与当前状态有关，建议删除后重新设置该属性值
        """
        pass

    def SetAnimEndCallback(self, animName, func):
        # type: (str, function) -> bool
        """
        设置动画播放结束后的回调，每次设置都会覆盖上一次的设置
        """
        pass

    def RemoveAnimEndCallback(self, animName):
        # type: (str) -> bool
        """
        移除动画播放结束后的回调
        """
        pass

    def IsAnimEndCallbackRegistered(self, animName):
        # type: (str) -> bool
        """
        控件是否对名称为animName的动画进行了注册回调
        """
        pass

    def asLabel(self):
        # type: () -> LabelUIControl
        """
        将当前BaseUIControl转换为LabelUIControl实例，如当前控件非Label类型则返回None
        """
        pass

    def asButton(self):
        # type: () -> ButtonUIControl
        """
        将当前BaseUIControl转换为ButtonUIControl实例，如当前控件非button类型则返回None
        """
        pass

    def asImage(self):
        # type: () -> ImageUIControl
        """
        将当前BaseUIControl转换为ImageUIControl实例，如当前控件非image类型则返回None
        """
        pass

    def asGrid(self):
        # type: () -> GridUIControl
        """
        将当前BaseUIControl转换为GridUIControl实例，如当前控件非grid类型则返回None
        """
        pass

    def asScrollView(self):
        # type: () -> ScrollViewUIControl
        """
        将当前BaseUIControl转换为ScrollViewUIControl实例，如当前控件非scrollview类型则返回None
        """
        pass

    def asSwitchToggle(self):
        # type: () -> SwitchToggleUIControl
        """
        将当前BaseUIControl转换为SwitchToggleUIControl实例，如当前控件非panel类型或非toggle则返回None
        """
        pass

    def asTextEditBox(self):
        # type: () -> TextEditBoxUIControl
        """
        将当前BaseUIControl转换为TextEditBoxUIControl实例，如当前控件非editbox类型则返回None
        """
        pass

    def asProgressBar(self, fillImagePath='/filled_progress_bar'):
        # type: (str) -> ProgressBarUIControl
        """
        将当前BaseUIControl转换为ProgressBarUIControl实例，如当前控件非panel类型则返回None
        """
        pass

    def asNeteasePaperDoll(self):
        # type: () -> NeteasePaperDollUIControl
        """
        将当前BaseUIControl转换为NeteasePaperDollUIControl实例，如当前控件非custom类型则返回None
        """
        pass

    def asMiniMap(self):
        # type: () -> MiniMapUIControl
        """
        将当前BaseUIControl转换为MiniMapUIControl实例，如当前控件非小地图类型则返回None
        """
        pass

    def asSlider(self):
        # type: () -> SliderUIControl
        """
        将当前BaseUIControl转换为SliderUIControl实例，如当前控件非滑动条类型则返回None
        """
        pass

    def asItemRenderer(self):
        # type: () -> ItemRendererUIControl
        """
        将当前BaseUIControl转换为ItemRenderer实例，如当前控件非custom类型则返回None
        """
        pass

    def asNeteaseComboBox(self):
        # type: () -> NeteaseComboBoxUIControl
        """
        将当前BaseUIControl转换为NeteaseComboBoxUIControl实例，如当前控件非panel类型则返回None
        """
        pass

    def asStackPanel(self):
        # type: () -> StackPanelUIControl
        """
        将当前BaseUIControl转换为StackPanelUIControl实例，如当前控件非stackPanel类型则返回None
        """
        pass

    def asInputPanel(self):
        # type: () -> InputPanelUIControl
        """
        将当前BaseUIControl转换为InputPanelUIControl实例，如当前控件非inputPanel类型则返回None
        """
        pass

    def asSelectionWheel(self):
        # type: () -> SelectionWheelUIControl
        """
        将当前BaseUIControl转换为SelectionWheelUIControl实例，如当前控件非selectionWheel类型则返回None
        """
        pass

