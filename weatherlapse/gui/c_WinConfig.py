__all__ = ['WinConfig']

import tkinter as _tk
import tkinter.ttk as _ttk

import objtypes as _objtypes

from .c_DTEntry import DTEntry as _DTEntry
from .c_GUIUtil import GUIUtil as _GUIUtil

class WinConfig(_tk.Toplevel):
    """
    Represents a configuration window
    """

    #region init

    def __init__(self, appinfo:_objtypes.AppInfo, *args, **kwargs):
        """ Initializer for WinConfig """
        # appinfo
        self.__appinfo = appinfo
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Configure")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _GUIUtil.win_center(self, 400, 350)
        self.columnconfigure(1, weight = 1)
        # Widgets
        def _widgets():
            nonlocal self
            _row = 0
            def __add_field(_text:str, _field:_tk.Widget):
                nonlocal self, _row
                # Label
                __label = _ttk.Label(\
                    master = self,\
                    justify = 'left',\
                    text = _text)
                __label.grid(\
                    column = 0, row = _row,\
                    padx = (0, 10), pady = (0, 5),\
                    sticky = 'we')
                # Field
                _field.grid(\
                    column = 1, row = _row,\
                    pady = (0, 5),\
                    sticky = 'we')
                # Next row
                _row += 1
            #region apikey
            # value
            self.__apikey_value = _tk.StringVar()
            # field
            self.__apikey_field = _tk.Entry(\
                master = self,\
                textvariable = self.__apikey_value)
            # add
            __add_field("OpenWeather API Key:", self.__apikey_field)
            #endregion
            #region region_zoom
            # value
            self.__region_zoom_value = _tk.StringVar()
            self.__region_zoom_value.set(self.__REGION_ZOOM_OPTIONS[0])
            # field
            self.__region_zoom_field = _ttk.Combobox(\
                master = self,\
                values = self.__REGION_ZOOM_OPTIONS,\
                state = "readonly",\
                textvariable = self.__region_zoom_value)
            self.__region_zoom_field.bind("<<ComboboxSelected>>", self.__r_region_zoom_field)
            # add
            __add_field("Region Zoom:", self.__region_zoom_field)
            #endregion
            #region region_min_x
            # value
            self.__region_min_x_value = _tk.IntVar()
            # field
            self.__region_min_x_field = _tk.Entry(\
                master = self,\
                textvariable = self.__region_min_x_value)
            # add
            __add_field("Region Min X:", self.__region_min_x_field)
            #endregion
            #region region_min_y
            # value
            self.__region_min_y_value = _tk.IntVar()
            # field
            self.__region_min_y_field = _tk.Entry(\
                master = self,\
                textvariable = self.__region_min_y_value)
            # add
            __add_field("Region Min Y:", self.__region_min_y_field)
            #endregion
            #region region_max_x
            # value
            self.__region_max_x_value = _tk.IntVar()
            # field
            self.__region_max_x_field = _tk.Entry(\
                master = self,\
                textvariable = self.__region_max_x_value)
            # add
            __add_field("Region Max X:", self.__region_max_x_field)
            #endregion
            #region region_max_y
            # value
            self.__region_max_y_value = _tk.IntVar()
            # field
            self.__region_max_y_field = _tk.Entry(\
                master = self,\
                textvariable = self.__region_max_y_value)
            # add
            __add_field("Region Max Y:", self.__region_max_y_field)
            #endregion
            #region layer
            # value
            self.__layer_value = _tk.StringVar()
            self.__layer_value.set(self.__LAYER_OPTIONS[0])
            # field
            self.__layer_field = _ttk.Combobox(\
                master = self,\
                values = self.__LAYER_OPTIONS,\
                state = "readonly",\
                textvariable = self.__layer_value)
            self.__layer_field.bind("<<ComboboxSelected>>", self.__r_layer_field)
            # add
            __add_field("Region Zoom:", self.__layer_field)
            #endregion
            #region start
            # field
            self.__start_field = _DTEntry(master = self)
            # add
            __add_field("Start:", self.__start_field)
        _widgets()
        # Post init
        self.__setupfields()

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

    __apikey_field:_tk.Entry
    __apikey_value:_tk.StringVar

    __region_zoom_field:_ttk.Combobox
    __region_zoom_value:_tk.StringVar

    __region_min_x_field:_tk.Entry
    __region_min_x_value:_tk.IntVar

    __region_min_y_field:_tk.Entry
    __region_min_y_value:_tk.IntVar

    __region_max_x_field:_tk.Entry
    __region_max_x_value:_tk.IntVar

    __region_max_y_field:_tk.Entry
    __region_max_y_value:_tk.IntVar

    __layer_field:_ttk.Combobox
    __layer_value:_tk.StringVar

    __start_field:_DTEntry

    #endregion

    #region receivers

    def __r_region_zoom_field(self, event = None):
        pass

    def __r_layer_field(self, event = None):
        pass

    #endregion

    #region helper methods

    def __setupfields(self):
        # Make sure config file exists
        if not self.__appinfo.configpath.is_file():
            return
        # Open config file
        config = _objtypes.Config()
        config.load_from_xml_file(str(self.__appinfo.configpath))
        # apikey
        self.__apikey_value.set(config.apikey)
        # region_zoom
        config_region_zoom = max(0, min(_objtypes.ConfigRegion.MAXZOOM, config.region.zoom))
        self.__region_zoom_value.set(self.__REGION_ZOOM_OPTIONS[config_region_zoom])
        # region_min_x
        self.__region_min_x_value.set(config.region.min_x)
        # region_min_y
        self.__region_min_y_value.set(config.region.min_y)
        # region_max_x
        self.__region_max_x_value.set(config.region.max_x)
        # region_max_y
        self.__region_max_y_value.set(config.region.max_y)
        # layer
        self.__layer_value.set(self.__LAYER_OPTIONS[config.layer.value - 1])


    #endregion