__all__ = ['WinTitle']

import tkinter as _tk
import tkinter.ttk as _ttk

class WinTitle(_tk.Tk):
    """
    Represents a help window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Window """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("weatherlapse")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.geometry('400x300')
        # splash
        __splash = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            background = 'gray')
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, minsize = 50)
        __splash.grid(column = 0, row = 0, columnspan = 2, sticky = 'nsew')
        # start
        __button_start = _ttk.Button(\
            master = self,\
            text = "Start")
        __button_start.grid(column = 0, row = 1, padx = (0, 2.5), pady = (5, 0), sticky = 'nsew')
        # config
        __button_config = _ttk.Button(\
            master = self,\
            text = "Config")
        __button_config.grid(column = 1, row = 1, padx = (2.5, 0), pady = (5, 0), sticky = 'nsew')

    #endregion