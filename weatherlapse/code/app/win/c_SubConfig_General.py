import shutil as _shutil
import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path
from tkinter import\
    messagebox as _messagebox

import code.app.gui as _gui
import code.engine.col as _col
import code.engine.objtypes as _objtypes

class _General(_tk.Frame):

    #region init

    def __init__(self,\
            config:None|_objtypes.Config = None,\
            reldir:None|_Path = None,\
            cachedir:None|_Path = None,\
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ignore = False
        # config
        self.__config = config
        # cachedir
        self.__cachedir = cachedir
        # Widgets
        def _widgets():
            nonlocal self
            def __create_labelframe(title:str):
                nonlocal self
                frame = _tk.LabelFrame(master = self, padx = 5, pady = 5, text = title)
                frame.pack(fill = 'x')
                return frame
            # f_apikey
            def ___init_apikey():
                nonlocal self
                # f_apikey
                self.__f_apikey = __create_labelframe("OpenWeather API Key")
                # f_apikey_value
                self.__f_apikey_value = _tk.StringVar()
                self.__f_apikey_value.trace_add('write', self.__r_f_apikey)
                # f_apikey_entry
                self.__f_apikey_entry = _ttk.Entry(master = self.__f_apikey, textvariable = self.__f_apikey_value)
                self.__f_apikey_entry.pack(fill = 'x')
            ___init_apikey()
            # f_useragent
            def ___init_useragent():
                nonlocal self
                # f_useragent
                self.__f_useragent = __create_labelframe("User Agent (ex: 'WeatherApp/1.0 (johndoe@email.com)')")
                # f_useragent_value
                self.__f_useragent_value = _tk.StringVar()
                self.__f_useragent_value.trace_add('write', self.__r_f_useragent)
                # f_useragent_entry
                self.__f_useragent_entry = _ttk.Entry(master = self.__f_useragent, textvariable = self.__f_useragent_value)
                self.__f_useragent_entry.pack(fill = 'x')
            ___init_useragent()
            # f_layer
            def ___init_layer():
                nonlocal self
                # f_layer
                self.__f_layer = __create_labelframe("Layer")
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
            ___init_layer()
            # f_output
            def ___init_output():
                nonlocal self
                # f_output
                self.__f_output = __create_labelframe("Output Directory")
                # f_output_field
                self.__f_output_field = _gui.PathField(\
                    master = self.__f_output)
                self.__f_output_field.dialogtitle = "Select Output Directory"
                self.__f_output_field.askdirectory = True
                self.__f_output_field.relativepath = reldir
                self.__f_output_field.valuechanged = self.__r_f_output
                self.__f_output_field.pack(fill = 'x')
            ___init_output()
            # f_deletecache
            def ___init_deletecache():
                nonlocal self
                # f_deletecache
                self.__f_deletecache = __create_labelframe("Cache")
                # f_deletecache_value
                self.__f_deletecache_value = _tk.BooleanVar()
                # f_deletecache_check
                self.__f_deletecache_check = _ttk.Checkbutton(\
                    master = self.__f_deletecache,\
                    variable = self.__f_deletecache_value,\
                    command = self.__r_f_deletecache,\
                    text = "Delete on exit")
                self.__f_deletecache_check.pack(side = 'left', fill = 'x', expand = True)
                # f_deletecache_clear
                self.__f_deletecache_clear = _ttk.Button(\
                    master = self.__f_deletecache,\
                    command = self.__r_f_deletecache_clear,\
                    text = "Delete")
                self.__f_deletecache_clear.pack(side = 'left')
            ___init_deletecache()
        _widgets()
        # Post-init
        self.refresh()

    #endregion

    #region const
    
    __LAYER_OPTIONS = _col.RODict({\
        _name: f"{_name.name[0]}{_name.name[1:].lower()}"\
        for _name in _objtypes.ConfigLayer})

    #endregion

    #region fields

    __f_apikey:_tk.LabelFrame
    __f_apikey_entry:_ttk.Entry
    __f_apikey_value:_tk.StringVar
    __f_useragent:_tk.LabelFrame
    __f_useragent_entry:_ttk.Entry
    __f_useragent_value:_tk.StringVar
    __f_layer:_tk.LabelFrame
    __f_layer_combo:_ttk.Combobox
    __f_layer_value:_tk.StringVar
    __f_output:_tk.LabelFrame
    __f_output_field:_gui.PathField
    __f_deletecache:_tk.LabelFrame
    __f_deletecache_check:_ttk.Checkbutton
    __f_deletecache_value:_tk.BooleanVar
    __f_deletecache_clear:_ttk.Button

    #endregion

    #region receivers

    def __r_f_apikey(self, *args):
        if self.__ignore: return
        if self.__config is None: return
        self.__config.apikey = self.__f_apikey_value.get()

    def __r_f_useragent(self, *args):
        if self.__ignore: return
        if self.__config is None: return
        self.__config.useragent = self.__f_useragent_value.get()

    def __r_f_layer(self, *args):
        if self.__ignore: return
        if self.__config is None: return
        # Find layer value
        layer = self.__LAYER_OPTIONS.find_key(self.__f_layer_value.get())
        if layer is None: layer = _objtypes.ConfigLayer.CLOUDS
        # Set value
        self.__config.layer = layer

    def __r_f_output(self, caller:_gui.PathField):
        if self.__ignore: return
        if self.__config is None: return
        self.__config.output = self.__f_output_field.value

    def __r_f_deletecache(self):
        if self.__ignore: return
        if self.__config is None: return
        value = self.__f_deletecache_value.get()
        # Warn user about deleting cache
        if value:
            msg = _messagebox.askyesno(\
                "Delete on exit",\
                "Are you sure you want to delete the cache on every exit?",\
                icon = 'warning')
            if not msg:
                self.__ignore = True
                self.__f_deletecache_value.set(False)
                self.__ignore = False
                return
        # Update value
        self.__config.deletecache = value
    
    def __r_f_deletecache_clear(self):
        if self.__cachedir is None: return
        # Warn user about deleting cache
        msg = _messagebox.askyesno(\
            "Delete Cache",\
            "Are you sure you want to delete the cache?",\
            icon = 'warning')
        if not msg: return
        # Delete cache
        if self.__cachedir.is_dir(): _shutil.rmtree(self.__cachedir)
        # Refresh
        self.refresh()

    #endregion

    #region methods

    def refresh(self):
        if self.__ignore: return
        if self.__config is None: return
        # Refresh begin
        self.__ignore = True
        # f_apikey
        self.__f_apikey_value.set(self.__config.apikey)
        # f_useragent
        self.__f_useragent_value.set(self.__config.useragent)
        # f_layer
        self.__f_layer_value.set(self.__LAYER_OPTIONS[self.__config.layer])
        # f_output
        self.__f_output_field.value = self.__config.output
        # f_deletecache
        self.__f_deletecache_value.set(self.__config.deletecache)
        if self.__cachedir is not None and self.__cachedir.is_dir():
            self.__f_deletecache_clear.config(state = 'normal')
        else: self.__f_deletecache_clear.config(state = 'disabled')
        # Refresh end
        self.__ignore = False

    #endregion