import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path

import app.gui as _gui
import engine.col as _col
import engine.objtypes as _objtypes

class _General(_tk.Frame):

    #region init

    def __init__(self, config:None|_objtypes.Config = None, reldir:None|_Path = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ignore = False
        # config
        self.__config = config
        # Widgets
        def _widgets():
            nonlocal self
            def __create_labelframe(title:str):
                nonlocal self
                frame = _tk.LabelFrame(master = self, padx = 5, pady = 5, text = title)
                frame.pack(fill = 'x')
                return frame
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
            # f_apikey
            ___init_apikey()
            # f_layer
            ___init_layer()
            # f_output
            ___init_output()
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
    __f_layer:_tk.LabelFrame
    __f_layer_combo:_ttk.Combobox
    __f_layer_value:_tk.StringVar
    __f_output:_tk.LabelFrame
    __f_output_field:_gui.PathField

    #endregion

    #region receivers

    def __r_f_apikey(self, *args):
        if self.__ignore: return
        if self.__config is None: return
        self.__config.apikey = self.__f_apikey_value.get()

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

    #endregion

    #region methods

    def refresh(self):
        if self.__ignore: return
        if self.__config is None: return
        self.__ignore = True
        self.__f_apikey_value.set(self.__config.apikey)
        self.__f_layer_value.set(self.__LAYER_OPTIONS[self.__config.layer])
        self.__f_output_field.value = self.__config.output
        self.__ignore = False

    #endregion