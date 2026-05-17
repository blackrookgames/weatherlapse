__all__ = ['Test']

import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui

from app.gui.c_DateTimeField_Calendar import _Calendar

from .c_WinUtil import WinUtil as _WinUtil

class Test(_tk.Tk):

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Test """
        super().__init__(*args, **kwargs)
        _WinUtil.win_center(self, 300, 300)
        # calendar
        self.__calendar = _Calendar(master = self)
        self.__calendar.pack(fill = 'x')
        # button
        self.__button = _ttk.Button(master = self)
        self.__button.pack()

    #endregion

    #region receivers


    #endregion