__all__ = ['TimeDeltaField']

import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.objtypes as _objtypes

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

from .c_TimeDeltaField_Win import _Win

class TimeDeltaField(_tk.LabelFrame):
    """ Represents a time delta field """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for TimeDeltaField """
        super().__init__(*args, **kwargs)
        # enabled
        self.__enabled = True
        # value
        self.__value:_dt.timedelta = _dt.timedelta()
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[TimeDeltaField] = None
        # label
        self.__label = _tk.Label(master = self, anchor = 'w', justify = 'left')
        self.__label.pack(expand = True, side = 'left', fill = 'x')
        # button
        self.__button = _ttk.Button(master = self, text = "Choose", command = self.__r_button)
        self.__button.pack(side = 'left')
        # Post-init
        self.__update_label()

    #endregion

    #region properties

    @property
    def enabled(self):
        """ Whether or not field is enabled """
        return self.__enabled
    @enabled.setter
    def enabled(self, value:bool):
        if self.__enabled == value: return
        self.__enabled = value
        # Update widgets
        self.__label.configure(state = 'normal' if self.__enabled else 'disabled')
        self.__button.state(['!disabled' if self.__enabled else 'disabled'])

    @property
    def value(self):
        """ Time delta value """
        return self.__value
    @value.setter
    def value(self, value:_dt.timedelta):
        if self.__value == value: return
        self.__set_value(value)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[TimeDeltaField]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:_dt.timedelta):
        self.__value = value
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)
        # Update widgets
        self.__update_label()

    def __update_label(self):
        # Compute hours, minutes, seconds
        _span = self.__value.seconds
        seconds = (_span % 60) + self.__value.microseconds / 1000
        _span //= 60
        minutes = _span % 60
        hours = _span // 60
        # Create text
        text_days = f"{self.__value.days} day{('s' if (self.__value.days != 1) else '')}"
        text_hours = f"{hours} hour{('s' if (hours != 1) else '')}"
        text_minutes = f"{minutes} minute{('s' if (minutes != 1) else '')}"
        text_seconds = f"{seconds} second{('s' if (hours != 1) else '')}"
        self.__label.configure(text = f"{text_days}; {text_hours}; {text_minutes}; {text_seconds}")

    #endregion

    #region receivers

    def __r_button(self):
        # Open window
        win = _Win(self.__value, master = self)
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.focus_set()
        win.wait_window()
        # Update value
        if self.__value != win.value:
            self.__set_value(win.value)

    #endregion