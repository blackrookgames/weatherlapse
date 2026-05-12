__all__ = ['SplashImages']

import math as _math
import tkinter as _tk
import tkinter.ttk as _ttk

from typing import\
    TYPE_CHECKING as _TYPE_CHECKING
from pathlib import\
    Path as _Path
from PIL import\
    Image as _Image

from .c_SplashImage import\
    SplashImage as _SplashImage

if (_TYPE_CHECKING):
    from .c_Splash import Splash as _Splash

class SplashImages:
    """ Represents the displayed images in a splash visual """

    #region init

    def __init__(self, splash:'_Splash'):
        """
        WARNING: This is only to be called by Splash
        """
        self.__splash = splash

    #endregion

    #region properties

    @property
    def splash(self):
        """ Splash object """
        return self.__splash

    #endregion