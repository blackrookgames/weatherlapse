__all__ = ['PercentBar']

import tkinter as _tk
import tkinter.ttk as _ttk

class PercentBar(_tk.Frame):
    """ Represents a percentage bar """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for PercentBar """
        super().__init__(*args, **kwargs)
        # bar
        self.__bar = _ttk.Progressbar(self)
        self.__bar.pack(side = 'left', fill = 'both', expand = True)
        # label
        self.__label = _ttk.Label(self, width = 5)
        self.__label.pack(side = 'left', fill = 'y', padx = (5, 0))
        # percentage
        self.__percentage = -1.0

    #endregion

    #region properties

    @property
    def percentage(self):
        """ Percentage value """
        return self.__percentage
    @percentage.setter
    def percentage(self, value:float):
        if self.__percentage == value: return
        self.__percentage = value
        self.__bar.configure(value = max(0, min(100.0, self.__percentage)))
        self.__label.configure(text = "" if (self.__percentage < 0.0) else f"{round(self.__percentage)}%")

    #endregion