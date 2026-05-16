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

class _Time(_tk.LabelFrame):

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

    def __init__(self, use12hr:bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs, text = "Time")
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 0)
        self.columnconfigure(4, weight = 1)
        self.__ignore = False
        # value
        self.__value:_dt.time = _dt.time(0, 0, 0, 0)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Time] = None
        # Widgets
        def _widgets():
            nonlocal self, use12hr
            def __colon():
                nonlocal self
                return _tk.Label(master = self, text = ':')
            # hours
            self.__hours = _ValueField[int](\
                self.__get_parse_func(min = 0, max = 23), 0, master = self)
            self.__hours.valuechanged = self.__r_hours
            self.__hours.grid(column = 0, row = 0)
            __colon().grid(column = 1, row = 0)
            # minutes
            self.__minutes = _ValueField[int](\
                self.__get_parse_func(min = 0, max = 59), 0, master = self)
            self.__minutes.valuechanged = self.__r_minutes
            self.__minutes.grid(column = 2, row = 0)
            __colon().grid(column = 3, row = 0)
            # seconds
            self.__seconds = _ValueField[_Time.__Sec](\
                self.__parse_sec, self.__F_SECONDS_DEFAULT, master = self)
            self.__seconds.valuechanged = self.__r_seconds
            self.__seconds.grid(column = 4, row = 0)
        _widgets()
        # Post-init
        self.__update_widgets()

    #endregion

    #region const

    __F_SECONDS_DEFAULT = __Sec(0, 0)

    #endregion

    #region fields
    
    __hours:_ValueField[int]
    __minutes:_ValueField[int]
    __seconds:_ValueField[__Sec]

    #endregion

    #region properties

    @property
    def value(self):
        """ Time/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.time):
        self.__set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Time]'):
        self.__valuechanged = valuechanged

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

    def __set_value(self, value:_dt.time, updatewidgets:bool):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        if updatewidgets: self.__update_widgets()
        # Callback
        if self.__valuechanged is not None: self.__valuechanged(self)
    
    def __update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        self.__hours.value = self.__value.hour
        self.__minutes.value = self.__value.minute
        self.__seconds.value = self.__Sec(self.__value.second, self.__value.microsecond)
        self.__ignore = False

    #endregion

    #region receivers
    
    def __r_hours(self, caller:_ValueField[int]):
        if self.__ignore: return
    
    def __r_minutes(self, caller:_ValueField[int]):
        if self.__ignore: return
    
    def __r_seconds(self, caller:_ValueField[__Sec]):
        if self.__ignore: return

    #endregion