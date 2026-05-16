import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui
import engine.col as _col
import engine.num as _num
import engine.objtypes as _objtypes

class _Region(_tk.LabelFrame):

    #region init

    def __init__(self, config:None|_objtypes.ConfigRegion = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(1, weight = 1)
        self.__ignore = False
        # config
        self.__config = config
        # Widgets
        def _widgets():
            nonlocal self
            row = 0
            def __add_field(prompt:str, field:_tk.Widget):
                nonlocal self, row
                # Label
                label = _tk.Label(master = self, justify = 'left', text = prompt)
                label.grid(column = 0, row = row, padx = (0, 10), pady = (0, 5), sticky = 'we')
                # Field
                field.grid(column = 1, row = row, pady = (0, 5), sticky = 'we')
                # Next row
                row += 1
            def __add_field_combo(prompt:str, textvariable, values):
                nonlocal self
                combo = _ttk.Combobox(\
                    master = self,\
                    values = [_value for _value in values],\
                    state = "readonly",\
                    textvariable = textvariable)
                __add_field(prompt, combo)
                return combo
            def __add_field_entry(prompt:str, callback:_gui.SimpleCallback[_gui.ValueField[int]]):
                nonlocal self
                entry = _gui.ValueField[_num.U16](_num.Parse.try_U16, _num.U16_MIN, master = self)
                entry.valuechanged = callback
                __add_field(prompt, entry)
                return entry
            # f_zoom
            self.__f_zoom_value = _tk.StringVar()
            self.__f_zoom_value.trace_add('write', self.__r_f_zoom)
            self.__f_zoom_combo = __add_field_combo("Zoom:", self.__f_zoom_value, self.__ZOOM_OPTIONS)
            # f_min_x
            self.__f_min_x_field = __add_field_entry("Min X:", self.__r_f_min_x)
            # f_min_y
            self.__f_min_y_field = __add_field_entry("Min Y:", self.__r_f_min_y)
            # f_max_x
            self.__f_max_x_field = __add_field_entry("Max X:", self.__r_f_max_x)
            # f_max_y
            self.__f_max_y_field = __add_field_entry("Max Y:", self.__r_f_max_y)
        _widgets()

    #endregion

    #region const
    
    __ZOOM_OPTIONS = _col.ROList([\
        f"Level {_i} ({(2 ** _i)}x{(2 ** _i)})"\
        for _i in range(_objtypes.ConfigRegion.MAXZOOM + 1)])

    #endregion

    #region fields
    
    __f_zoom_combo:_ttk.Combobox
    __f_zoom_value:_tk.StringVar
    __f_min_x_field:_gui.ValueField[_num.U16]
    __f_min_y_field:_gui.ValueField[_num.U16]
    __f_max_x_field:_gui.ValueField[_num.U16]
    __f_max_y_field:_gui.ValueField[_num.U16]

    #endregion

    #region receivers

    def __r_f_zoom(self, *args):
        if self.__config is None: return
        if self.__ignore: return
        # Find zoom value
        value = self.__f_zoom_value.get()
        index = 0
        for _i in range(1, len(self.__ZOOM_OPTIONS)):
            if self.__ZOOM_OPTIONS[_i] != value:
                continue
            index = _i
            break
        # Update config
        self.__config.zoom = index

    def __r_f_min_x(self, *args):
        if self.__config is None: return
        if self.__ignore: return
        self.__config.min_x = int(self.__f_min_x_field.value)

    def __r_f_min_y(self, *args):
        if self.__config is None: return
        if self.__ignore: return
        self.__config.min_y = int(self.__f_min_y_field.value)

    def __r_f_max_x(self, *args):
        if self.__config is None: return
        if self.__ignore: return
        self.__config.max_x = int(self.__f_max_x_field.value)

    def __r_f_max_y(self, *args):
        if self.__config is None: return
        if self.__ignore: return
        self.__config.max_y = int(self.__f_max_y_field.value)

    #endregion

    #region methods

    def refresh(self):
        if self.__config is None: return
        if self.__ignore: return
        self.__ignore = True
        self.__f_zoom_value.set(self.__ZOOM_OPTIONS[self.__config.zoom])
        self.__f_min_x_field.value = _num.U16(self.__config.min_x)
        self.__f_min_y_field.value = _num.U16(self.__config.min_y)
        self.__f_max_x_field.value = _num.U16(self.__config.max_x)
        self.__f_max_y_field.value = _num.U16(self.__config.max_y)
        self.__ignore = False

    #endregion