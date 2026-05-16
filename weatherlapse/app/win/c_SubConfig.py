__all__ = ['SubConfig']

import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from tkinter import\
    messagebox as _messagebox

import app.gui as _gui
import engine.col as _col
import engine.objtypes as _objtypes

from app.c_AppInfo import AppInfo as _AppInfo

from .c_WinUtil import WinUtil as _WinUtil

from .c_SubConfig_General import _General
from .c_SubConfig_DateTime import _DateTime
from .c_SubConfig_Region import _Region

class SubConfig(_tk.Toplevel):
    """
    Represents a configuration window
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for SubConfig """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Configure")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _WinUtil.win_center(self, 400, 400)
        self.protocol("WM_DELETE_WINDOW", self.__r_closing)
        self.__ignore = False
        # appinfo
        self.__appinfo = appinfo
        # Config
        self.__config = _objtypes.Config()
        if self.__appinfo.configpath.is_file():
            self.__config.load_from_xml_file(str(self.__appinfo.configpath))
        # Widgets
        def _widgets():
            nonlocal self
            def __form():
                nonlocal self
                # f
                self.__f = _ttk.Notebook(master = self)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
                # f_general
                self.__f_general = _General(master = self.__f, padx = 5, pady = 5,\
                    config = self.__config)
                self.__f.add(self.__f_general, text = "General")
                # f_region
                self.__f_region = _Region(master = self.__f, padx = 5, pady = 5,\
                    config = self.__config.region)
                self.__f.add(self.__f_region, text = "Region")
                # f_datetime
                self.__f_datetime = _DateTime(master = self.__f, padx = 5, pady = 5,\
                    config = self.__config.datetime)
                self.__f.add(self.__f_datetime, text = "Date/Time")
            def __buttons():
                nonlocal self
                # b
                self.__b = _tk.Frame(master = self)
                self.__b.pack(anchor = 'sw')
                # b_ok
                self.__b_ok = _ttk.Button(master = self.__b, text = "OK", command = self.__r_b_ok)
                self.__b_ok.pack(side = 'left', padx = (0, 5))
                # b_reset
                self.__b_reset = _ttk.Button(master = self.__b, text = "Reset", command = self.__r_b_reset)
                self.__b_reset.pack(side = 'left', padx = (0, 5))
                # b_cancel
                self.__b_cancel = _ttk.Button(master = self.__b, text = "Cancel", command = self.__r_b_cancel)
                self.__b_cancel.pack(side = 'left', padx = (0, 5))
            __form()
            __buttons()
        _widgets()
        # Post-init
        self.__refresh()

    #endregion

    #region fields

    __f:_ttk.Notebook
    __f_general:_General
    __f_region:_Region
    __f_datetime:_DateTime
    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_reset:_ttk.Button
    __b_cancel:_ttk.Button

    #endregion

    #region helper methods

    def __cancel(self):
        if not _messagebox.askyesno(\
                "Discard Changes",\
                "Any unsaved changes will be lost. Is This OK?",
                parent = self):
            return
        self.destroy()

    def __refresh(self):
        if self.__ignore: return
        self.__ignore = True
        self.__f_general.refresh()
        self.__f_region.refresh()
        self.__f_datetime.refresh()
        self.__ignore = False

    #endregion

    #region receivers

    def __r_closing(self):
        self.__cancel()

    def __r_b_ok(self):
        self.__config.save_to_xml_file(str(self.__appinfo.configpath))
        self.destroy()

    def __r_b_reset(self):
        if not _messagebox.askyesno(\
                "Reset",\
                "Reset to default configuration? This cannot be undone.",\
                parent = self):
            return
        self.__config.reset()
        self.__refresh()

    def __r_b_cancel(self):
        self.__cancel()
    
    #endregion