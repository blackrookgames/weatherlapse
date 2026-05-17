import datetime as _dt
import tkinter as _tk

import engine.num as _num
import engine.objtypes as _objtypes

from .c_SimpleCallback import SimpleCallback as _SimpleCallback
from .c_ValueField import ValueField as _ValueField

class _Time(_tk.LabelFrame):

    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, text = "Time")
        # value
        self.__value:_dt.time = _dt.time(0, 0, 0, 0)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Time] = None

    #endregion

    #region properties

    @property
    def value(self):
        """ Time/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.time):
        self._set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Time]'):
        self.__valuechanged = valuechanged

    #endregion

    #region private methods

    @classmethod
    def __get_parse_func(cls, min:int, max:int):
        def _func(s:str):
            nonlocal max
            # Parse string
            result = _num.Parse.try_int(s)
            if not result.success: return result
            # Check range
            if result.value < min: return _num.ParseResult(min, _num.ParseError("Too small!!!"))
            if result.value > max: return _num.ParseResult(max, _num.ParseError("Too large!!!"))
            # Success
            return result
        return _func
    
    #endregion

    #region protected methods

    def _set_value(self, value:_dt.time, updatewidgets:bool):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        if updatewidgets: self._update_widgets()
        # Callback
        if self.__valuechanged is not None: self.__valuechanged(self)

    def _change_value(self, updatewidgets:bool,\
            hour:None|int = None,\
            minute:None|int = None,\
            second:None|int = None,\
            microsecond:None|int = None):
        if hour is None: hour = self.__value.hour
        if minute is None: minute = self.__value.minute
        if second is None: second = self.__value.second
        if microsecond is None: microsecond = self.__value.microsecond
        self._set_value(_dt.time(hour, minute, second, microsecond), updatewidgets)
        
    @classmethod
    def _create_field_int(cls, min:int = 0, max:int = 999999999, *args, **kwargs):
        field = _ValueField[int](cls.__get_parse_func(min, max), min, *args, **kwargs)
        return field
    
    @classmethod
    def _create_field_sechand(cls, *args, **kwargs):
        DEFAULT = _objtypes.SecHand(0, 0)
        field = _ValueField[_objtypes.SecHand](_objtypes.SecHand.tryparse, DEFAULT, *args, **kwargs)
        return field

    #endregion

    #region abstract methods

    def _update_widgets(self):
        raise NotImplementedError("_update_widgets has not been implemented.")
    
    #endregion