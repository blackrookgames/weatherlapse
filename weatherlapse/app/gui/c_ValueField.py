__all__ = ['ValueField']

import tkinter as _tk
import tkinter.ttk as _ttk

from typing import\
    Callable as _Callable,\
    Generic as _Generic,\
    TypeVar as _TypeVar

import engine.col as _col
import engine.num as _num
import engine.objtypes as _objtypes

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

TValue = _TypeVar('TValue')

class ValueField(_tk.Frame, _Generic[TValue]):
    """ Represents a value field """

    #region init

    def __init__(self,\
            parse:_Callable[[str], _num.ParseResult[TValue]],\
            default:TValue,\
            *args, **kwargs):
        """
        Initializer for ValueField

        :param parse: Parse function
        :param default: Default value
        """
        super().__init__(*args, **kwargs)
        self.__ignore = False
        # parse
        self.__parse = parse
        # default
        self.__default = default
        # enabled
        self.__enabled = True
        # value
        self.__value = self.__default
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[ValueField] = None
        # entry
        self.__entry_value = _tk.StringVar()
        self.__entry_value.trace_add('write', self.__r_entry_value)
        self.__entry = _ttk.Entry(master = self, textvariable = self.__entry_value)
        self.__entry.pack(fill = 'both')
        # Post-init
        self.__update()

    #endregion

    #region const

    __COLOR_VALID = 'black'
    __COLOR_INVALID = 'red'

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
        self.__entry.state(['!disabled' if self.__enabled else 'disabled'])

    @property
    def value(self):
        """ Value """
        return self.__value
    @value.setter
    def value(self, value:TValue):
        self.__set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[ValueField]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    def __set_value(self, value:TValue, update_widgets:bool):
        if self.__value == value: return
        self.__value = value
        # Update widgets
        if update_widgets:
            self.__update()
        # Callback
        if self.__valuechanged is not None:
            self.__valuechanged(self)

    def __update(self):
        if self.__ignore: return
        self.__ignore = True
        self.__entry_value.set(str(self.__value))
        self.__entry.configure(foreground = self.__COLOR_VALID)
        self.__ignore = False

    #endregion

    #region receivers

    def __r_entry_value(self, *args):
        if self.__ignore: return
        result = self.__parse(self.__entry_value.get())
        if result.success:
            self.__set_value(result.value, False)
            self.__entry.configure(foreground = self.__COLOR_VALID)
        else:
            self.__set_value(self.__default, False)
            self.__entry.configure(foreground = self.__COLOR_INVALID)

    #endregion