import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.objtypes as _objtypes

from .c_ValueField import ValueField as _ValueField

from .c_DateTimeField_Time import _Time

class _Time24(_Time):

    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 0)
        self.columnconfigure(4, weight = 1)
        self.__ignore = False
        # Widgets
        def _widgets():
            nonlocal self
            def __colon():
                nonlocal self
                return _tk.Label(master = self, text = ':')
            # hours
            self.__field_hours = self._create_field_int(max = 23, master = self)
            self.__field_hours.valuechanged = self.__r_field_hours
            self.__field_hours.grid(column = 0, row = 0)
            __colon().grid(column = 1, row = 0)
            # minutes
            self.__field_minutes = self._create_field_int(max = 59, master = self)
            self.__field_minutes.valuechanged = self.__r_field_minutes
            self.__field_minutes.grid(column = 2, row = 0)
            __colon().grid(column = 3, row = 0)
            # seconds
            self.__field_seconds = self._create_field_sechand(master = self)
            self.__field_seconds.valuechanged = self.__r_field_seconds
            self.__field_seconds.grid(column = 4, row = 0)
        _widgets()
        # Post-init
        self._update_widgets()

    #endregion

    #region Time
    
    def _update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        self.__field_hours.value = self.value.hour
        self.__field_minutes.value = self.value.minute
        self.__field_seconds.value = _objtypes.SecHand(self.value.second, self.value.microsecond)
        self.__ignore = False

    #endregion

    #region fields

    __field_hours:_ValueField[int]
    __field_minutes:_ValueField[int]
    __field_seconds:_ValueField[_objtypes.SecHand]

    #endregion

    #region receivers
    
    def __r_field_hours(self, caller:_ValueField[int]):
        if self.__ignore: return
        self._change_value(False, hour = self.__field_hours.value)

    def __r_field_minutes(self, caller:_ValueField[int]):
        if self.__ignore: return
        self._change_value(False, minute = self.__field_minutes.value)
    
    def __r_field_seconds(self, caller:_ValueField[_objtypes.SecHand]):
        if self.__ignore: return
        self._change_value(False,\
            second = self.__field_seconds.value.second,\
            microsecond = self.__field_seconds.value.microsecond)

    #endregion