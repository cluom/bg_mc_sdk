# -*- coding: utf-8 -*-

from mod.common.component.baseComponent import BaseComponent
from typing import Tuple

class ChestContainerCompServer(BaseComponent):
    def GetChestBoxSize(self, playerId, pos, dimensionId=-1):
        # type: (None, Tuple[int,int,int], int) -> int
        """
        获取箱子容量大小
        """
        pass

    def SetChestBoxItemNum(self, playerId, pos, slotPos, num, dimensionId=-1):
        # type: (None, Tuple[int,int,int], int, int, int) -> bool
        """
        设置箱子槽位物品数目
        """
        pass

    def SetChestBoxItemExchange(self, playerId, pos, slotPos1, slotPos2):
        # type: (str, Tuple[int,int,int], int, int) -> bool
        """
        交换箱子里物品的槽位
        """
        pass

