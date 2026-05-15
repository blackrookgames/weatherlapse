import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui

class _DTField(_tk.LabelFrame):

    #region init

    def __init__(self, cbtext:str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ignore = False
        # value
        self.__value:None|_dt.datetime = None
        # valuechanged
        self.__valuechanged:None|_gui.SimpleCallback[_DTField] = None
        # checkbox
        self.__checkbox_value = _tk.BooleanVar()
        self.__checkbox = _tk.Checkbutton(\
            master = self, anchor = 'w', justify = 'left', text = cbtext,\
            variable = self.__checkbox_value, command = self.__r_checkbox)
        self.__checkbox.pack(fill = 'x', anchor = 'w')
        # field
        self.__field = _gui.DateTimeField(master = self)
        self.__field.enabled = False
        self.__field.valuechanged = self.__r_field_valuechanged
        self.__field.pack(fill = 'x')

    #endregion

    #region properties

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, value:None|_dt.datetime):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        self.__ignore = True
        if self.__value is not None:
            self.__checkbox_value.set(True)
            self.__field.enabled = True
            self.__field.value = self.__value
        else:
            self.__checkbox_value.set(False)
            self.__field.enabled = False
        self.__ignore = False
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_gui.SimpleCallback[_DTField]'):
        self.__valuechanged = valuechanged

    #endregion

    #region receivers

    def __r_checkbox(self):
        if self.__ignore: return
        # Update widgets
        self.__ignore = True
        if self.__checkbox_value.get():
            self.__field.enabled = True
            self.__value = self.__field.value
        else:
            self.__field.enabled = False
            self.__value = None
        self.__ignore = False
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)
    
    def __r_field_valuechanged(self, caller:_gui.DateTimeField):
        if self.__ignore: return
        # Update widgets
        self.__ignore = True
        self.__value = self.__field.value
        self.__checkbox_value.set(True)
        self.__field.enabled = True
        self.__ignore = False
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)

    #endregion