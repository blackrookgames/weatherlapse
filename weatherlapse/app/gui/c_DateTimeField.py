__all__ = ['DateTimeField']

import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.objtypes as _objtypes

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
        # dialogtitle
        self.__dialogtitle = "Pick Date/Time"
        # format
        self.__format:_objtypes.DTFormat = _objtypes.DTFormat(False, _objtypes.DTFormatDate.YEAR_MONTH_DAY)
        # value
        self.__value:_dt.datetime = _dt.datetime(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[DateTimeField] = None
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
    def format(self):
        """ Date/time display format """
        return self.__format
    @format.setter
    def format(self, value:_objtypes.DTFormat):
        if self.__format == value: return
        self.__format = value
        # Update widgets
        self.__update_label()

    @property
    def dialogtitle(self):
        """ Dialog title """
        return self.__dialogtitle
    @dialogtitle.setter
    def dialogtitle(self, value:str):
        self.__dialogtitle = value

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
        self.__update_label()

    def __update_label(self):
        match self.__format.date:
            case _objtypes.DTFormatDate.YEAR_MONTH_DAY: format_date = "%Y/%m/%d"
            case _objtypes.DTFormatDate.DAY_MONTH_YEAR: format_date = "%d/%m/%Y"
            case _objtypes.DTFormatDate.MONTH_DAY_YEAR: format_date = "%m/%d/%Y"
            case _: format_date = ""
        format_time = "%I:%M:%S %p" if self.__format.use12hr else "%H:%M:%S"
        self.__label.configure(text = self.__value.strftime(f"{format_date} {format_time}"))

    #endregion

    #region receivers

    def __r_button(self):
        # Open window
        win = _Win(self.__value, master = self, format = self.__format, title = self.__dialogtitle)
        win.transient(self.winfo_toplevel())
        win.grab_set()
        win.focus_set()
        win.wait_window()
        # Update value
        if self.__value != win.value:
            self.__set_value(win.value)

    #endregion