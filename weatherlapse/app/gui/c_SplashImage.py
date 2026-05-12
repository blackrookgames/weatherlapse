__all__ = ['SplashImage']

import math as _math
import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path
from PIL import\
    Image as _Image

from .c_Anchor import\
    Anchor as _Anchor

class SplashImage:
    """ Represents an image in a splash visual """

    #region init

    def __init__(self, path:_Path, anchor:_Anchor = _Anchor.CENTER, letterbox:bool = False):
        """
        Initializer for SplashImage
        
        :param path:
            Path to input image
        :param anchor:
            Anchor setting
        :param letterbox:
            Whether or not to use letterbox alignment
        """
        self.__img = _Image.open(path)
        self.__img.load()
        self.__img.close()
        self.__width, self.__height = self.__img.size
        self.__aspect = self.__width / self.__height
        self.__anchor = anchor
        self.__letterbox = letterbox

    #endregion

    #region properties

    @property
    def width(self):
        """ Image width """
        return self.__width
    
    @property
    def height(self):
        """ Image height """
        return self.__height
    
    @property
    def aspect(self):
        """ Image aspect ratio """
        return self.__aspect

    @property
    def anchor(self):
        """ Anchor setting """
        return self.__anchor

    @property
    def letterbox(self):
        """ Whether or not to use letterbox alignment """
        return self.__letterbox

    #endregion

    #region internal methods

    def _render(self, target_width:int, target_height:int):
        """
        Assume:
        - target_width > 0
        - target_height > 0
        \n
        \nAlso accessed by Splash 
        """
        target_aspect = target_width / target_height
        usewidth = (self.__aspect > target_aspect) if self.__letterbox else (self.__aspect < target_aspect)
        if usewidth: return self.__img.resize((target_width, _math.ceil(target_width * self.__aspect)))
        return self.__img.resize((_math.ceil(target_height / self.__aspect)), target_height)
        
            

            

    #endregion