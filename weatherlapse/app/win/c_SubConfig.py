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
        _WinUtil.win_center(self, 400, 650)
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
                def ___create_labelframe(title:str):
                    nonlocal self
                    frame = _tk.LabelFrame(master = self.__f, padx = 5, pady = 5, text = title)
                    frame.pack(fill = 'x')
                    return frame
                def ___init_apikey():
                    nonlocal self
                    # f_apikey
                    self.__f_apikey = ___create_labelframe("OpenWeather API Key")
                    # f_apikey_value
                    self.__f_apikey_value = _tk.StringVar()
                    self.__f_apikey_value.trace_add('write', self.__r_f_apikey)
                    # f_apikey_entry
                    self.__f_apikey_entry = _ttk.Entry(master = self.__f_apikey, textvariable = self.__f_apikey_value)
                    self.__f_apikey_entry.pack(fill = 'x')
                def ___init_layer():
                    nonlocal self
                    # f_layer
                    self.__f_layer = ___create_labelframe("Layer")
                    # f_layer_value
                    self.__f_layer_value = _tk.StringVar()
                    self.__f_layer_value.trace_add('write', self.__r_f_layer)
                    # f_layer_entry
                    self.__f_layer_combo = _ttk.Combobox(\
                        master = self.__f_layer,\
                        values = self.__LAYER_OPTIONS.values(),\
                        state = "readonly",\
                        textvariable = self.__f_layer_value)
                    self.__f_layer_combo.pack(fill = 'x')
                def ___init_output():
                    nonlocal self
                    # f_output
                    self.__f_output = ___create_labelframe("Output Directory")
                    # f_output_field
                    self.__f_output_field = _gui.PathField(\
                        master = self.__f_output)
                    self.__f_output_field.valuechanged = self.__r_f_output
                    self.__f_output_field.pack(fill = 'x')
                # f
                self.__f = _tk.Frame(\
                    master = self)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
                # f_apikey
                ___init_apikey()
                # f_region
                self.__f_region = _Region(master = self.__f, padx = 5, pady = 5, text = "Region",\
                    config = self.__config.region)
                self.__f_region.pack(fill = 'x')
                # f_layer
                ___init_layer()
                # f_datetime
                self.__f_datetime = _DateTime(master = self.__f, padx = 5, pady = 5, text = "Date/Time",\
                    config = self.__config.datetime)
                self.__f_datetime.pack(fill = 'x')
                # f_output
                ___init_output()
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

    #region const
    
    __LAYER_OPTIONS = _col.RODict({\
        _name: f"{_name.name[0]}{_name.name[1:].lower()}"\
        for _name in _objtypes.ConfigLayer})

    #endregion

    #region fields

    __f:_tk.Frame
    __f_apikey:_tk.LabelFrame
    __f_apikey_entry:_ttk.Entry
    __f_apikey_value:_tk.StringVar
    __f_region:_Region
    __f_layer:_tk.LabelFrame
    __f_layer_combo:_ttk.Combobox
    __f_layer_value:_tk.StringVar
    __f_datetime:_DateTime
    __f_output:_tk.LabelFrame
    __f_output_field:_gui.PathField
    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_reset:_ttk.Button
    __b_cancel:_ttk.Button

    #endregion

    #region helper methods

    def __cancel(self):
        if not _messagebox.askyesno("Discard Changes", "Any unsaved changes will be lost. Is This OK?"):
            return
        self.destroy()

    def __refresh(self):
        if self.__ignore: return
        self.__ignore = True
        self.__f_apikey_value.set(self.__config.apikey)
        self.__f_region.refresh()
        self.__f_layer_value.set(self.__LAYER_OPTIONS[self.__config.layer])
        self.__f_datetime.refresh()
        self.__f_output_field.value = self.__config.output
        self.__ignore = False

    #endregion

    #region receivers

    def __r_closing(self):
        self.__cancel()

    def __r_b_ok(self):
        self.__config.save_to_xml_file(str(self.__appinfo.configpath))
        self.destroy()

    def __r_b_reset(self):
        if not _messagebox.askyesno("Reset", "Reset to default configuration? This cannot be undone."):
            return
        self.__config.reset()
        self.__refresh()

    def __r_b_cancel(self):
        self.__cancel()

    def __r_f_apikey(self, *args):
        if self.__ignore: return
        self.__config.apikey = self.__f_apikey_value.get()

    def __r_f_layer(self, *args):
        if self.__ignore: return
        # Find layer value
        layer = self.__LAYER_OPTIONS.find_key(self.__f_layer_value.get())
        if layer is None: layer = _objtypes.ConfigLayer.CLOUDS
        # Set value
        self.__config.layer = layer

    def __r_f_output(self, caller:_gui.PathField):
        if self.__ignore: return
        self.__config.output = self.__f_output_field.value

    #endregion