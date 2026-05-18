import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.col as _col
import engine.help as _help
import engine.num as _num
import engine.objtypes as _objtypes

from .c_SimpleCallback import SimpleCallback as _SimpleCallback
from .c_DateTimeField_Calendar import _Calendar

class _Date(_tk.LabelFrame):

    #region init

    def __init__(self,\
            format:_objtypes.DTFormatDate = _objtypes.DTFormatDate.YEAR_MONTH_DAY,\
            *args, **kwargs):
        super().__init__(*args, **kwargs, text = "Date")
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.__ignore = False
        # value
        self.__value:_dt.date = _dt.date(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Date] = None
        # Widgets
        def _widgets():
            nonlocal self, format
            def __year():
                nonlocal self
                self.__year_value = _tk.StringVar()
                self.__year_value.trace_add('write', self.__r_year)
                self.__year_field = _ttk.Combobox(\
                    master = self,\
                    values = [str(_i) for _i in range(1900, 2500)],\
                    textvariable = self.__year_value)
                return self.__year_field
            def __month():
                nonlocal self
                self.__month_value = _tk.StringVar()
                self.__month_value.trace_add('write', self.__r_month)
                self.__month_field = _ttk.Combobox(\
                    master = self,\
                    state = "readonly",\
                    values = [_month for _month in self.__MONTHS],\
                    textvariable = self.__month_value)
                return self.__month_field
            def __calendar():
                nonlocal self
                self.__calendar = _Calendar(master = self)
                self.__calendar.valuechanged = self.__r_calendar
                return self.__calendar
            if format == _objtypes.DTFormatDate.YEAR_MONTH_DAY:
                __year().grid(column = 0, row = 0, padx = 2.5, pady = 2.5)
                __month().grid(column = 1, row = 0, padx = 2.5, pady = 2.5)
            else:
                __month().grid(column = 0, row = 0, padx = 2.5, pady = 2.5)
                __year().grid(column = 1, row = 0, padx = 2.5, pady = 2.5)
            __calendar().grid(column = 0, row = 1, columnspan = 2, padx = 0.5, pady = 0.5)
        _widgets()
        # Post-init
        self.__update_widgets()

    #endregion

    #region const
    
    __MONTHS = _col.ROList([\
        "January", "February", "March", "April", "May", "June",\
        "July", "August", "September", "October",  "November", "December",])

    __YEAR_GOOD = 'black'
    __YEAR_BAD  = 'red'

    #endregion

    #region fields

    __year_value:_tk.StringVar
    __year_field:_ttk.Combobox
    __month_value:_tk.StringVar
    __month_field:_ttk.Combobox
    __calendar:_Calendar

    #endregion

    #region properties

    @property
    def value(self):
        """ Date/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.date):
        self.__set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Date]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:_dt.date, updatewidgets:bool):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        if updatewidgets: self.__update_widgets()
        # Callback
        if self.__valuechanged is not None: self.__valuechanged(self)

    def __update_year(self):
        self.__year_value.set(str(self.__value.year))
        self.__year_field.configure(foreground = self.__YEAR_GOOD)

    def __update_month(self):
        self.__month_value.set(self.__MONTHS[self.__value.month - 1])

    def __update_calendar(self):
        self.__calendar.value = self.__value

    def __update_widgets(self):
        if self.__ignore: return
        self.__ignore = True
        self.__update_year()
        self.__update_month()
        self.__update_calendar()
        self.__ignore = False

    #endregion

    #region receivers

    def __r_year(self, *args):
        if self.__ignore: return
        # Parse
        parse_result = _num.Parse.try_int(self.__year_value.get())
        if not parse_result.success:
            self.__year_field.configure(foreground = self.__YEAR_BAD)
            return
        # Range check
        if parse_result.value < _help.DateUtil.YEAR_MIN:
            self.__year_field.configure(foreground = self.__YEAR_BAD)
            return
        if parse_result.value > _help.DateUtil.YEAR_MAX:
            self.__year_field.configure(foreground = self.__YEAR_BAD)
            return
        # Update
        self.__ignore = True
        self.__set_value(_help.DateUtil.change_year(self.__value, parse_result.value), False)
        self.__update_month()
        self.__update_calendar()
        self.__ignore = False
        # Success!!!
        self.__year_field.configure(foreground = self.__YEAR_GOOD)
    
    def __r_month(self, *args):
        if self.__ignore: return
        self.__ignore = True
        self.__month_field.current()
        self.__set_value(_help.DateUtil.change_month(self.__value, self.__month_field.current() + 1), False)
        self.__update_year()
        self.__update_calendar()
        self.__ignore = False
    
    def __r_calendar(self, *args):
        if self.__ignore: return
        self.__ignore = True
        self.__set_value(self.__calendar.value, False)
        self.__update_year()
        self.__update_month()
        self.__ignore = False

    #endregion