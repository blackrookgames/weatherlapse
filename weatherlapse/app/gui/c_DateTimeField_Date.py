import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import engine.col as _col
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
            # year
            self.__year_value = _tk.StringVar()
            self.__year_value.trace_add('write', self.__r_year)
            self.__year_field = _ttk.Combobox(\
                master = self,\
                state = "readonly",\
                values = [str(_i) for _i in range(1900, 10000)],\
                textvariable = self.__year_value)
            # month
            self.__month_value = _tk.StringVar()
            self.__month_value.trace_add('write', self.__r_month)
            self.__month_field = _ttk.Combobox(\
                master = self,\
                state = "readonly",\
                values = self.__MONTHS_NAMES,\
                textvariable = self.__month_value)
            # calendar
            self.__calendar = _Calendar(master = self)
            self.__calendar.valuechanged = self.__r_calendar
            # Place on grid
            if format == _objtypes.DTFormatDate.YEAR_MONTH_DAY:
                self.__year_field.grid(column = 0, row = 0, padx = 2.5, pady = 2.5)
                self.__month_field.grid(column = 1, row = 0, padx = 2.5, pady = 2.5)
            else:
                self.__month_field.grid(column = 0, row = 0)
                self.__year_field.grid(column = 1, row = 0)
            self.__calendar.grid(column = 0, row = 1, columnspan = 2)
        _widgets()
        # Post-init
        self.__update_widgets()

    #endregion

    #region const
    
    __MONTHS = _col.RODict({\
        "January": 1,\
        "February": 2,\
        "March": 3,\
        "April": 4,\
        "May": 5,\
        "June": 6,\
        "July": 7,\
        "August": 8,\
        "September": 9,\
        "October": 10,\
        "November": 11,\
        "December": 12,})
    __MONTHS_NAMES = __MONTHS.keys()

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

    def __compute_date(self):
        return _dt.date(\
            int(self.__year_value.get()),\
            self.__MONTHS[self.__month_value.get()],\
            self.__calendar.value.day)

    def __update_year(self):
        """
        Assume:
        - __ignore == True
        """
        self.__year_value.set(str(self.__value.year))

    def __update_month(self):
        """
        Assume:
        - __ignore == True
        """
        self.__month_value.set(self.__MONTHS_NAMES[self.__value.month - 1])

    def __update_calendar(self):
        """
        Assume:
        - __ignore == True
        """
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
        self.__ignore = True
        self.__set_value(self.__compute_date(), False)
        self.__update_month()
        self.__update_calendar()
        self.__ignore = False
    
    def __r_month(self, *args):
        if self.__ignore: return
        self.__ignore = True
        self.__set_value(self.__compute_date(), False)
        self.__update_year()
        self.__update_calendar()
        self.__ignore = False
    
    def __r_calendar(self, *args):
        if self.__ignore: return
        self.__ignore = True
        self.__set_value(self.__compute_date(), False)
        self.__update_year()
        self.__update_month()
        self.__ignore = False

    #endregion