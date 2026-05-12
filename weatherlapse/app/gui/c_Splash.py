__all__ = ['Splash']

import tkinter as _tk
import tkinter.ttk as _ttk

from .c_SplashImage import SplashImage as _SplashImage
from .c_SplashImages import SplashImages as _SplashImages

class Splash(_ttk.Frame):
    """ Represents a splash visual """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Splash """
        super().__init__(*args, **kwargs)
        # Canvas
        self.__canvas = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            background = 'gray')
        # self.__splash.bind("<Configure>", self.__r_splash_Configure)
        self.__canvas.pack(expand = True, fill = 'both')
        # Images
        self.__images = 
        

    #endregion

    # def __r_splash_Configure(self, event = None):
    #     width = self.__splash.winfo_width()
    #     height = self.__splash.winfo_height()
    #     # Position image
    #     self.__splash.coords(self.__splash_image, width / 2, height / 2)