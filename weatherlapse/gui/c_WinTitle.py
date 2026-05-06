__all__ = ['WinTitle']

import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path

import objtypes as _objtypes

from .c_GUIUtil import GUIUtil as _GUIUtil
from .c_WinConfig import WinConfig as _WinConfig

class WinTitle(_tk.Tk):
    """
    Represents a help window
    """

    #region init

    def __init__(self, appinfo:_objtypes.AppInfo, *args, **kwargs):
        """ Initializer for WinTitle """
        # appinfo
        self.__appinfo = appinfo
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("weatherlapse")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _GUIUtil.win_center(self, 400, 300)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, minsize = 50)
        # splash
        self.__splash = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            background = 'gray')
        self.__splash.bind("<Configure>", self.__r_splash_Configure)
        self.__splash.grid(column = 0, row = 0, columnspan = 2, sticky = 'nsew')
        # splash image
        self.__splash_photo = _tk.PhotoImage(file = f"{self.__appinfo.directory}.png")
        self.__splash_image = self.__splash.create_image(0, 0, image = self.__splash_photo, anchor = 's')
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

    def __r_splash_Configure(self, event = None):
        width = self.__splash.winfo_width()
        height = self.__splash.winfo_height()
        # Position image
        self.__splash.coords(self.__splash_image, width / 2, height)

    def __r_button_start(self):
        return

    def __r_button_config(self):
        win = _WinConfig(self.__appinfo, master = self)
        win.transient(self)
        win.grab_set()
        win.focus_set()
        win.wait_window()

    #endregion