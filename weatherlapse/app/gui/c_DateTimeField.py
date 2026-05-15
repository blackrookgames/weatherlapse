__all__ = ['DateTimeField']

import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

from .c_DateTimeField_Win import _Win

class DateTimeField(_tk.LabelFrame):
    """ Represents a date/time field """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for DateTimeField """
        super().__init__(*args, **kwargs)
        # enabled
        self.__enabled = True
        # value
        self.__value:_dt.datetime = _dt.datetime(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[DateTimeField] = None
        # label
        self.__label = _tk.Label(master = self, anchor = 'w', justify = 'left', text = str(self.__value))
        self.__label.pack(expand = True, side = 'left', fill = 'x')
        # button
        self.__button = _ttk.Button(master = self, text = "Choose", command = self.__r_button)
        self.__button.pack(side = 'left')

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
    def valuechanged(self, valuechanged:'None|_SimpleCallback[DateTimeField]'):
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