__all__ = ['PathField']

import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path

import engine.num as _num

from .c_SimpleCallback import SimpleCallback as _SimpleCallback
from .c_ValueField import ValueField as _ValueField

class PathField(_tk.LabelFrame):
    """ Represents a date/time field """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for PathField """
        super().__init__(*args, **kwargs)
        # enabled
        self.__enabled = True
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[PathField] = None
        # field
        self.__field = _ValueField(self.__parse, _Path(), master = self)
        self.__field.valuechanged = self.__r_field_valuechanged
        self.__field.pack(expand = True, side = 'left', fill = 'x')
        # button
        self.__button = _ttk.Button(master = self, text = "...", width = 3, command = self.__r_button)
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
        self.__field.enabled = self.__enabled
        self.__button.state(['!disabled' if self.__enabled else 'disabled'])

    @property
    def value(self):
        """ Path """
        return self.__field.value
    @value.setter
    def value(self, value:_Path):
        self.__field.value = value

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[PathField]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    @classmethod
    def __parse(cls, s:str):
        try: return _num.ParseResult(_Path(s), None)
        except: return _num.ParseResult(_Path(), _num.ParseError())

    #endregion

    #region receivers

    def __r_field_valuechanged(self, caller:_ValueField[_Path]):
        if self.__valuechanged is not None: self.__valuechanged(self)

    def __r_button(self):
        pass

    #endregion