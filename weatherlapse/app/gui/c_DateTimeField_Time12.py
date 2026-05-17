import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.objtypes as _objtypes

from .c_ValueField import ValueField as _ValueField

from .c_DateTimeField_Time import _Time

class _Time12(_Time):

    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 0)
        self.columnconfigure(4, weight = 1)
        self.columnconfigure(5, weight = 0)
        self.columnconfigure(6, weight = 0)
        self.__ignore = False
        # hour
        self.__hour = 0
        self.__hour_pm = False
        # Widgets
        def _widgets():
            nonlocal self
            # hours
            self.__field_hours = self._create_field_int(min = 1, max = 12, master = self)
            self.__field_hours.valuechanged = self.__r_field_hours
            self.__field_hours.grid(column = 0, row = 0)
            _tk.Label(master = self, text = ':').grid(column = 1, row = 0)
            # minutes
            self.__field_minutes = self._create_field_int(max = 59, master = self)
            self.__field_minutes.valuechanged = self.__r_field_minutes
            self.__field_minutes.grid(column = 2, row = 0)
            _tk.Label(master = self, text = ':').grid(column = 3, row = 0)
            # seconds
            self.__field_seconds = self._create_field_sechand(master = self)
            self.__field_seconds.valuechanged = self.__r_field_seconds
            self.__field_seconds.grid(column = 4, row = 0)
            _tk.Label(master = self, text = ' ').grid(column = 5, row = 0)
            # ampm
            self.__field_ampm_value = _tk.StringVar()
            self.__field_ampm_value.trace_add('write', self.__r_field_ampm)
            self.__field_ampm = _ttk.Combobox(master = self, state = 'readonly', values = ["AM", "PM"],\
                width = 4, textvariable = self.__field_ampm_value)
            self.__field_ampm.grid(column = 6, row = 0)
        _widgets()
        # Post-init
        self._update_widgets()

    #endregion

    #region Time
    
    def _update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        self.__hour = self.value.hour % 12
        self.__hour_pm = self.value.hour >= 12
        self.__field_hours.value = 12 if (self.__hour == 0) else self.__hour
        self.__field_minutes.value = self.value.minute
        self.__field_seconds.value = _objtypes.SecHand(self.value.second, self.value.microsecond)
        self.__field_ampm_value.set("PM" if self.__hour_pm else "AM")
        self.__ignore = False

    #endregion

    #region fields

    __field_hours:_ValueField[int]
    __field_minutes:_ValueField[int]
    __field_seconds:_ValueField[_objtypes.SecHand]
    __field_ampm:_ttk.Combobox
    __field_ampm_value:_tk.StringVar

    #endregion

    #region receivers
    
    def __r_field_hours(self, caller:_ValueField[int]):
        if self.__ignore: return
        self.__hour = self.__field_hours.value % 12
        self._change_value(False, hour = self.__hour + (12 if self.__hour_pm else 0))

    def __r_field_minutes(self, caller:_ValueField[int]):
        if self.__ignore: return
        self._change_value(False, minute = self.__field_minutes.value)
    
    def __r_field_seconds(self, caller:_ValueField[_objtypes.SecHand]):
        if self.__ignore: return
        self._change_value(False,\
            second = self.__field_seconds.value.second,\
            microsecond = self.__field_seconds.value.microsecond)
    
    def __r_field_ampm(self, *args):
        if self.__ignore: return
        self.__hour_pm = self.__field_ampm_value.get().lower() == 'pm'
        self._change_value(False, hour = self.__hour + (12 if self.__hour_pm else 0))

    #endregion