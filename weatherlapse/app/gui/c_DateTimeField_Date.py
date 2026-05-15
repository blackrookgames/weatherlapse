import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

class _Date(_tk.LabelFrame):

    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, text = "Date")
        # value
        self.__value:_dt.datetime = _dt.datetime(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Date] = None
        # label
        self.__label = _tk.Label(master = self, anchor = 'w', justify = 'left', text = str(self.__value))
        self.__label.pack(expand = True, side = 'left', fill = 'x')
        # button
        self.__button = _ttk.Button(master = self, text = "Choose")
        self.__button.pack(side = 'left')

    #endregion

    #region properties

    @property
    def value(self):
        """ Date/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.datetime):
        if self.__value == value: return
        self.__set_value(value)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Date]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:_dt.datetime):
        self.__value = value
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)
        # Update widgets
        self.__label.configure(text = str(self.__value))

    #endregion