__all__ = ['PathField']

import tkinter as _tk
import tkinter.ttk as _ttk

from collections.abc import\
    Iterable as _Iterable
from pathlib import\
    Path as _Path
from tkinter import\
    filedialog as _filedialog

import engine.num as _num

from .c_SimpleCallback import SimpleCallback as _SimpleCallback
from .c_ValueField import ValueField as _ValueField

type _filetypes = _Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None

class PathField(_tk.LabelFrame):
    """ Represents a date/time field """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for PathField """
        super().__init__(*args, **kwargs)
        # enabled
        self.__enabled = True
        # dialogtitle
        self.__dialogtitle = "Select Path"
        # askdirectory
        self.__askdirectory = False
        # filetypes
        self.__filetypes:_filetypes = None
        # relativepath
        self.__relativepath:None|_Path = None
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
    def dialogtitle(self):
        """ Dialog title """
        return self.__dialogtitle
    @dialogtitle.setter
    def dialogtitle(self, value:str):
        self.__dialogtitle = value

    @property
    def askdirectory(self):
        """ Whether or not clicking '...' opens a directory dialog """
        return self.__askdirectory
    @askdirectory.setter
    def askdirectory(self, value:bool):
        self.__askdirectory = value

    @property
    def filetypes(self):
        """ File types (ignored if askdirectory == True) """
        return self.__filetypes
    @filetypes.setter
    def filetypes(self, value:_filetypes):
        self.__filetypes = value

    @property
    def relativepath(self):
        """ 
        If not None, paths returned from '...' dialog that are relative to 
        this path will be displayed as a relative path (ex: folder/file.txt).
        """
        return self.__relativepath
    @relativepath.setter
    def relativepath(self, value:None|_Path):
        self.__relativepath = value

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
        if self.__askdirectory:
            rawpath = _filedialog.askdirectory(title = self.__dialogtitle)
        else:
            if self.__filetypes is not None:
                rawpath = _filedialog.askopenfilename(title = self.__dialogtitle, filetypes = self.__filetypes)
            else:
                rawpath = _filedialog.askopenfilename(title = self.__dialogtitle)
        if rawpath:
            path = _Path(rawpath)
            if self.__relativepath is not None:
                try: path = path.relative_to(self.__relativepath)
                except: pass
            self.__field.value = path

    #endregion