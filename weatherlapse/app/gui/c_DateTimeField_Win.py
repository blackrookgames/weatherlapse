import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.objtypes as _objtypes

from .c_DateTimeField_Date import _Date
from .c_DateTimeField_Time import _Time

class _Win(_tk.Toplevel):

    #region init

    def __init__(self,\
            initvalue:_dt.datetime = _dt.datetime(2000, 1, 1),\
            title:str = "",\
            format:_objtypes.DTFormat = _objtypes.DTFormat(False, _objtypes.DTFormatDate.YEAR_MONTH_DAY),\
            *args, **kwargs):
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Pick Date/Time")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.title(title)
        # Size
        WIN_WIDTH = 300
        WIN_HEIGHT = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_x = round(screen_width / 2 - WIN_WIDTH / 2)
        win_y = round(screen_height / 2 - WIN_HEIGHT / 2)
        self.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}+{win_x}+{win_y}')
        # value
        self.__value = initvalue
        self.__temp = self.__value
        # Widgets
        def _widgets():
            nonlocal self
            def __form():
                nonlocal self, format
                # f
                self.__f = _tk.Frame(master = self)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
                # f_date
                self.__f_date = _Date(master = self.__f, format = format.date, padx = 2.5, pady = 2.5)
                self.__f_date.pack(anchor = 'n', fill = 'x')
                # f_time
                self.__f_time = _Time(master = self.__f, use12hr = format.use12hr, padx = 5, pady = 5)
                self.__f_time.pack(anchor = 'n', fill = 'x')
            def __buttons():
                nonlocal self
                # b
                self.__b = _tk.Frame(master = self)
                self.__b.pack(anchor = 'sw')
                # b_ok
                self.__b_ok = _ttk.Button(master = self.__b, text = "OK", command = self.__r_b_ok)
                self.__b_ok.pack(side = 'left')
                # b_cancel
                self.__b_cancel = _ttk.Button(master = self.__b, text = "Cancel", command = self.__r_b_cancel)
                self.__b_cancel.pack(side = 'left', padx = (5, 0))
            __form()
            __buttons()
        _widgets()

    #endregion

    #region fields

    __f:_tk.Frame
    __f_date:_Date
    __f_time:_Time
    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_cancel:_ttk.Button

    #endregion

    #region properties

    @property
    def value(self):
        """ Date/time value """
        return self.__value

    #endregion

    #region receivers

    def __r_b_ok(self):
        self.__value = self.__temp
        self.destroy()

    def __r_b_cancel(self):
        self.destroy()

    #endregion