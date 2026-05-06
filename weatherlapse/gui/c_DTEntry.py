__all__ = ['DTEntry']

import tkinter as _tk
import tkinter.ttk as _ttk

from datetime import datetime as _datetime

class DTEntry(_ttk.Frame):
    """
    Represents a date/time entry field
    """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for WinConfig """
        # value
        self.__value = _datetime.now()
        # Initialize
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1)
        # label
        __label = _ttk.Label(\
            master = self,\
            justify = 'left',\
            text = str(self.__value))
        __label.grid(\
            column = 0, row = 0,\
            padx = (0, 5),\
            sticky = 'we')
        # button
        __button = _ttk.Button(\
            master = self,\
            width = 5,\
            text = "...")
        __button.grid(\
            column = 1, row = 0)

    #endregion