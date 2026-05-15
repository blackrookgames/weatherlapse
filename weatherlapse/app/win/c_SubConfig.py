__all__ = ['SubConfig']

import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui
import engine.objtypes as _objtypes

from app.c_AppInfo import AppInfo as _AppInfo

from .c_WinUtil import WinUtil as _WinUtil

from .c_SubConfig_DTField import _DTField

class SubConfig(_tk.Toplevel):
    """
    Represents a configuration window
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for SubConfig """
        # appinfo
        self.__appinfo = appinfo
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Configure")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _WinUtil.win_center(self, 400, 550)
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
                    # f_apikey_entry
                    self.__f_apikey_entry = _ttk.Entry(master = self.__f_apikey, textvariable = self.__f_apikey_value)
                    self.__f_apikey_entry.pack(fill = 'x')
                def ___init_region():
                    nonlocal self
                    row = 0
                    def ____add_field(prompt:str, field:_tk.Widget):
                        nonlocal self, row
                        # Label
                        label = _tk.Label(master = self.__f_region, justify = 'left', text = prompt)
                        label.grid(column = 0, row = row, padx = (0, 10), pady = (0, 5), sticky = 'we')
                        # Field
                        field.grid(column = 1, row = row, pady = (0, 5), sticky = 'we')
                        # Next row
                        row += 1
                    def ____add_field_combo(prompt:str, textvariable, values):
                        nonlocal self
                        combo = _ttk.Combobox(\
                            master = self.__f_region,\
                            values = values,\
                            state = "readonly",\
                            textvariable = textvariable)
                        ____add_field(prompt, combo)
                        return combo
                    def ____add_field_entry(prompt:str, textvariable):
                        nonlocal self
                        entry = _ttk.Entry(master = self.__f_region, textvariable = textvariable)
                        ____add_field(prompt, entry)
                        return entry
                    # f_region
                    self.__f_region = ___create_labelframe("Region")
                    self.__f_region.columnconfigure(1, weight = 1)
                    # f_region_zoom
                    self.__f_region_zoom_value = _tk.StringVar()
                    self.__f_region_zoom_value.set(self.__REGION_ZOOM_OPTIONS[0])
                    self.__f_region_zoom_combo = ____add_field_combo("Zoom:", self.__f_region_zoom_value, self.__REGION_ZOOM_OPTIONS)
                    # f_region_min_x
                    self.__f_region_min_x_value = _tk.IntVar()
                    self.__f_region_min_x_entry = ____add_field_entry("Min X:", self.__f_region_min_x_value)
                    # f_region_min_y
                    self.__f_region_min_y_value = _tk.IntVar()
                    self.__f_region_min_y_entry = ____add_field_entry("Min Y:", self.__f_region_min_y_value)
                    # f_region_max_x
                    self.__f_region_max_x_value = _tk.IntVar()
                    self.__f_region_max_x_entry = ____add_field_entry("Max X:", self.__f_region_max_x_value)
                    # f_region_max_y
                    self.__f_region_max_y_value = _tk.IntVar()
                    self.__f_region_max_y_entry = ____add_field_entry("Max Y:", self.__f_region_max_y_value)
                def ___init_layer():
                    nonlocal self
                    # f_layer
                    self.__f_layer = ___create_labelframe("Layer")
                    # f_layer_value
                    self.__f_layer_value = _tk.StringVar()
                    self.__f_layer_value.set(self.__LAYER_OPTIONS[0])
                    # f_layer_entry
                    self.__f_layer_combo = _ttk.Combobox(\
                            master = self.__f_layer,\
                            values = self.__LAYER_OPTIONS,\
                            state = "readonly",\
                            textvariable = self.__f_layer_value)
                    self.__f_layer_combo.pack(fill = 'x')
                # f
                self.__f = _tk.Frame(\
                    master = self)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
                # f_apikey
                ___init_apikey()
                # f_region
                ___init_region()
                # f_layer
                ___init_layer()
                # f_start
                self.__f_start = _DTField(master = self.__f, text = "Start", cbtext = "Start timelapse at Specified Date/Time")
                self.__f_start.valuechanged = self.__r_start_valuechanged
                self.__f_start.pack(fill = 'x')
                # f_stop
                self.__f_stop = _DTField(master = self.__f, text = "Stop", cbtext = "Stop timelapse at Specified Date/Time")
                self.__f_stop.valuechanged = self.__r_stop_valuechanged
                self.__f_stop.value = _dt.datetime(9999, 12, 31) # This will be the default when user first checks the checkbox
                self.__f_stop.value = None
                self.__f_stop.pack(fill = 'x')
            def __buttons():
                nonlocal self
                # b
                self.__b = _tk.Frame(\
                    master = self)
                self.__b.pack(anchor = 'sw')
                # b_ok
                self.__b_ok = _ttk.Button(\
                    master = self.__b,\
                    text = "OK")
                self.__b_ok.pack(side = 'left')
                # b_cancel
                self.__b_cancel = _ttk.Button(\
                    master = self.__b,\
                    text = "Cancel")
                self.__b_cancel.pack(side = 'left', padx = (5, 0))
            __form()
            __buttons()
        _widgets()

    #endregion

    #region const

    __REGION_ZOOM_OPTIONS = [\
        f"Level {_i} ({(2 ** _i)}x{(2 ** _i)})"\
        for _i in range(_objtypes.ConfigRegion.MAXZOOM + 1)]
    
    __LAYER_OPTIONS = [\
        f"{_name.name[0]}{_name.name[1:].lower()}"\
        for _name in _objtypes.ConfigLayer]

    #endregion

    #region fields

    __f:_tk.Frame
    __f_apikey:_tk.LabelFrame
    __f_apikey_entry:_ttk.Entry
    __f_apikey_value:_tk.StringVar
    __f_region:_tk.LabelFrame
    __f_region_zoom_combo:_ttk.Combobox
    __f_region_zoom_value:_tk.StringVar
    __f_region_min_x_entry:_ttk.Entry
    __f_region_min_x_value:_tk.IntVar
    __f_region_min_y_entry:_ttk.Entry
    __f_region_min_y_value:_tk.IntVar
    __f_region_max_x_entry:_ttk.Entry
    __f_region_max_x_value:_tk.IntVar
    __f_region_max_y_entry:_ttk.Entry
    __f_region_max_y_value:_tk.IntVar
    __f_layer:_tk.LabelFrame
    __f_layer_combo:_ttk.Combobox
    __f_layer_value:_tk.StringVar
    __f_start:_DTField
    __f_stop:_DTField
    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_cancel:_ttk.Button

    #endregion

    #region receivers

    def __r_start_valuechanged(self, caller:_DTField):
        print(self.__f_start.value)

    def __r_stop_valuechanged(self, caller:_DTField):
        print(self.__f_stop.value)

    def __r_region_zoom_field(self, event = None):
        pass

    def __r_layer_field(self, event = None):
        pass

    #endregion