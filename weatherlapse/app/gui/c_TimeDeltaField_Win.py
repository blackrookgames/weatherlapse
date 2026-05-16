import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from dataclasses import\
    dataclass as _dataclass
from typing import\
    Callable as _Callable,\
    TypeVar as _TypeVar

import engine.num as _num

from .c_SimpleCallback import SimpleCallback as _SimpleCallback
from .c_ValueField import ValueField as _ValueField

TValue = _TypeVar('TValue')

class _Win(_tk.Toplevel):

    #region nested

    @_dataclass(frozen = True)
    class __Sec:
        # const
        __MILLION = 1000000
        # fields
        seconds:int
        microseconds:int
        # operators
        def __str__(self):
            return str(self.seconds + self.microseconds / self.__MILLION)
        # methods
        @classmethod
        def from_float(cls, input:float):
            micros = round(input * cls.__MILLION)
            return cls(micros // cls.__MILLION, micros % cls.__MILLION)

    #endregion

    #region init

    def __init__(self,\
            initvalue:_dt.timedelta = _dt.timedelta(), title:str = "",\
            *args, **kwargs):
        # Initialize
        super().__init__(*args, **kwargs)
        self.title(title)
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.__ignore = False
        # Size
        WIN_WIDTH = 300
        WIN_HEIGHT = 140
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
                nonlocal self
                row = 0
                def ___add_field(prompt:str, field:_tk.Widget):
                    nonlocal self, row
                    # Label
                    label = _tk.Label(master = self.__f, justify = 'left', text = prompt)
                    label.grid(column = 0, row = row, padx = (0, 10), pady = (0, 5), sticky = 'we')
                    # Field
                    field.grid(column = 1, row = row, pady = (0, 5), sticky = 'we')
                    # Next row
                    row += 1
                def ___add_field_entry[TValue](\
                        prompt:str,\
                        parse:_Callable[[str], _num.ParseResult[TValue]],\
                        callback:_SimpleCallback[_ValueField[TValue]],\
                        default:TValue):
                    nonlocal self
                    entry = _ValueField[TValue](parse, default, master = self.__f)
                    entry.valuechanged = callback
                    ___add_field(prompt, entry)
                    return entry
                # f
                self.__f = _tk.Frame(master = self)
                self.__f.columnconfigure(1, weight = 1)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
                # f_days
                self.__f_days = ___add_field_entry(\
                    "Days:", self.__get_parse_func(min = 0, max = 999999999), self.__r_f_days, 0)
                # f_hours
                self.__f_hours = ___add_field_entry(\
                    "Hours:", self.__get_parse_func(min = 0, max = 23), self.__r_f_hours, 0)
                # f_minutes
                self.__f_minutes = ___add_field_entry(\
                    "Minutes:", self.__get_parse_func(min = 0, max = 59), self.__r_f_minutes, 0)
                # f_seconds
                self.__f_seconds = ___add_field_entry(\
                    "Seconds:", self.__parse_sec, self.__r_f_seconds, self.__F_SECONDS_DEFAULT)
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
        # Post-init
        self.__update_widgets()

    #endregion

    #region const

    __F_SECONDS_DEFAULT = __Sec(0, 0)

    #endregion

    #region fields

    __f:_tk.Frame
    __f_days:_ValueField[int]
    __f_hours:_ValueField[int]
    __f_minutes:_ValueField[int]
    __f_seconds:_ValueField[__Sec]
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

    #region helper methods

    @classmethod
    def __get_parse_func(cls, min:None|int = None, max:None|int = None):
        def _func(s:str):
            nonlocal min, max
            # Parse string
            result = _num.Parse.try_int(s)
            if not result.success: return result
            # Check range
            if min is not None and result.value < min:
                return _num.ParseResult(min, _num.ParseError("Too small!!!"))
            if max is not None and result.value > max:
                return _num.ParseResult(max, _num.ParseError("Too large!!!"))
            # Success
            return result
        return _func

    @classmethod
    def __parse_sec(cls, s:str):
        # Parse string
        result = _num.Parse.try_float(s)
        if not result.success:
            return _num.ParseResult(cls.__F_SECONDS_DEFAULT, result.error)
        # Check range
        if result.value < 0.0 or result.value >= 60.0:
            return _num.ParseResult(cls.__F_SECONDS_DEFAULT, _num.ParseError("Out of range!!!"))
        # Success!!!
        return _num.ParseResult(cls.__Sec.from_float(result.value), None)
    
    def __compute_tiledelta(self):
        return _dt.timedelta(\
            days = self.__f_days.value,\
            seconds = (self.__f_hours.value * 60 + self.__f_minutes.value) * 60 + self.__f_seconds.value.seconds,\
            microseconds = self.__f_seconds.value.microseconds)
    
    def __extract_tiledelta(self):
        _span = self.__temp.seconds
        # seconds
        seconds = _span % 60
        _span //= 60
        # minutes
        minutes = _span % 60
        _span //= 60
        # Return
        return self.__temp.days, _span, minutes, self.__Sec(seconds, self.__temp.microseconds)
    
    def __update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        days, hours, minutes, seconds = self.__extract_tiledelta()
        self.__f_days.value = days
        self.__f_hours.value = hours
        self.__f_minutes.value = minutes
        self.__f_seconds.value = seconds
        self.__ignore = False

    #endregion

    #region receivers

    def __r_b_ok(self):
        self.__value = self.__temp
        self.destroy()

    def __r_b_cancel(self):
        self.destroy()

    def __r_f_days(self, caller:_ValueField[int]):
        if self.__ignore: return
        self.__temp = self.__compute_tiledelta()
    
    def __r_f_hours(self, caller:_ValueField[int]):
        if self.__ignore: return
        self.__temp = self.__compute_tiledelta()
    
    def __r_f_minutes(self, caller:_ValueField[int]):
        if self.__ignore: return
        self.__temp = self.__compute_tiledelta()
    
    def __r_f_seconds(self, caller:_ValueField[__Sec]):
        if self.__ignore: return
        self.__temp = self.__compute_tiledelta()

    #endregion