import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

class _Calendar(_tk.LabelFrame):

    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, text = "Calendar")
        self.__ignore = False
        # value
        self.__value:_dt.date = _dt.date(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Calendar] = None

    #endregion

    #region properties

    @property
    def value(self):
        """ Calendar/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.date):
        if self.__value == value: return
        self.__set_value(value)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Calendar]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:_dt.date):
        self.__value = value
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)

    #endregion