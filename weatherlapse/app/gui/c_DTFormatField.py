__all__ = ['DTFormatField']

import tkinter as _tk
import tkinter.ttk as _ttk

import engine.col as _col
import engine.objtypes as _objtypes

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

class DTFormatField(_tk.Frame):
    """ Represents a date/time field """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for DTFormatField """
        super().__init__(*args, **kwargs)
        self.__ignore = False
        # enabled
        self.__enabled = True
        # value
        self.__value:_objtypes.DTFormat = _objtypes.DTFormat(False, _objtypes.DTFormatDate.YEAR_MONTH_DAY)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[DTFormatField] = None
        # use12hr
        self.__use12hr_value = _tk.BooleanVar()
        self.__use12hr = _tk.Checkbutton(\
            master = self, anchor = 'w', justify = 'left', text = "12-Hour Format",\
            variable = self.__use12hr_value, command = self.__r_use12hr)
        self.__use12hr.pack(fill = 'x', anchor = 'w')
        # date
        self.__date_value = _tk.StringVar()
        self.__date_value.trace_add("write", self.__r_date)
        self.__date = _ttk.Combobox(\
            master = self, values = self.__DATE_OPTIONS.values(),\
            state = "readonly", textvariable = self.__date_value)
        self.__date.pack(fill = 'x', anchor = 'w')
        # Post-init
        self.__update_widgets()

    #endregion

    #region const

    __DATE_OPTIONS = _col.RODict[_objtypes.DTFormatDate, str]({\
        _objtypes.DTFormatDate.YEAR_MONTH_DAY: "Year/Month/Day",\
        _objtypes.DTFormatDate.DAY_MONTH_YEAR: "Day/Month/Year",\
        _objtypes.DTFormatDate.MONTH_DAY_YEAR: "Month/Day/Year"})

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
        self.__use12hr.configure(state = 'normal' if self.__enabled else 'disabled')
        self.__date.state(['!disabled' if self.__enabled else 'disabled'])

    @property
    def value(self):
        """ Date/time value """
        return self.__value
    @value.setter
    def value(self, value:_objtypes.DTFormat):
        self.__set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[DTFormatField]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:_objtypes.DTFormat, update_widgets:bool):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        if update_widgets:
            self.__update_widgets()
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)

    def __update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        self.__use12hr_value.set(self.__value.use12hr)
        self.__date_value.set(self.__DATE_OPTIONS[self.__value.date])
        self.__ignore = False

    #endregion

    #region receivers

    def __r_use12hr(self):
        if self.__ignore: return
        # Set value
        self.__set_value(\
            _objtypes.DTFormat(self.__use12hr_value.get(), self.__value.date),\
            False)

    def __r_date(self, *args):
        if self.__ignore: return
        # Find date value
        date = self.__DATE_OPTIONS.find_key(self.__date_value.get())
        if date is None: date = _objtypes.DTFormatDate.YEAR_MONTH_DAY
        # Set value
        self.__set_value(\
            _objtypes.DTFormat(self.__value.use12hr, date),\
            False)

    #endregion