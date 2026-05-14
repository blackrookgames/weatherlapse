__all__ = ['WinTitle']

import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path

import app.gui as _gui

from app.c_AppInfo import AppInfo as _AppInfo
from .c_WinUtil import WinUtil as _WinUtil

class WinTitle(_tk.Tk):
    """
    Represents a help window
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for WinTitle """
        # appinfo
        self.__appinfo = appinfo
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("weatherlapse")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _WinUtil.win_center(self, 400, 250)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, minsize = 50)
        # icon
        if self.__appinfo.iswindows:
            self.__icon = None
            self.iconbitmap(self.__appinfo.iconpath)
        else:
            self.__icon = _tk.PhotoImage(file = self.__appinfo.iconpath)
            self.iconphoto(True, self.__icon)
        # splash
        self.__splash = _gui.Splash(master = self)
        self.__splash.grid(column = 0, row = 0, columnspan = 2, sticky = 'nsew')
        self.__splash.images.add(_gui.SplashImage(\
            _Path(f"{self.__appinfo.directory}.splash.png"),\
            anchor = _gui.Anchor.CENTER,\
            letterbox = False))
        self.__splash.images.add(_gui.SplashImage(\
            _Path(f"{self.__appinfo.directory}.logo.png"),\
            anchor = _gui.Anchor.N,\
            letterbox = True))
        # start
        self.__button_start = _ttk.Button(\
            master = self,\
            command = self.__r_button_start,\
            text = "Start")
        self.__button_start.grid(column = 0, row = 1, padx = (0, 2.5), pady = (5, 0), sticky = 'nsew')
        # config
        self.__button_config = _ttk.Button(\
            master = self,\
            command = self.__r_button_config,\
            text = "Config")
        self.__button_config.grid(column = 1, row = 1, padx = (2.5, 0), pady = (5, 0), sticky = 'nsew')
        # Post init
        self.__refresh()

    #endregion

    #region helper methods

    def __refresh(self):
        # Refresh Start button
        if self.__appinfo.configpath.is_file():
            if self.__button_start.cget('state') == 'disabled':
                self.__button_start.config(state = 'normal')
        else:
            if self.__button_start.cget('state') != 'disabled':
                self.__button_start.config(state = 'disabled')

    #endregion

    #region receivers

    def __r_button_start(self):
        return

    def __r_button_config(self):
        return

    #endregion