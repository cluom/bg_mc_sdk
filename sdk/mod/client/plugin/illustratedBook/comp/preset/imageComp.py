
# -*- coding: utf-8 -*-
from mod.client.plugin.illustratedBook.comp.baseComp import BaseComp
from mod.client.plugin.illustratedBook.bookConfig import BookConfig
from typing import List
from typing import Dict
from typing import Tuple

class ImageComp(BaseComp):

    def __init__(self, imageResizeRule = BookConfig.ImageReszieRule.Ninesliced):
        # type: (int) -> ImageComp
        """
            图片组件初始化
        """
        pass

    def SetDataBeforeShow(self, image):
        # type: (str) -> ImageComp
        """
            在显示组件之前，设置组件的数据
        """       
        pass

    def SetAlpha(self, alpha):
        # type: (float) -> ImageComp
        """
            设置图片透明度
        """       
        pass        

