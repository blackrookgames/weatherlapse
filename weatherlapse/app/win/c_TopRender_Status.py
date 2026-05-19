import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui
import engine.objtypes as _objtypes

class _Status(_tk.Frame):

    #region init

    def __init__(self, dtformat:_objtypes.DTFormat, *args, **kwargs):
        # Initialize
        super().__init__(*args, **kwargs)
        # dtformat
        self.__dtformat = dtformat
        # date
        def _date():
            nonlocal self
            # frame
            frame = _tk.Frame(master = self)
            frame.pack(side = 'left')
            # headers
            _tk.Label(master = frame, anchor = 'w', justify = 'left', text = "Last: ").\
                grid(column = 0, row = 0, sticky = 'we')
            _tk.Label(master = frame, anchor = 'w', justify = 'left', text = "Next: ").\
                grid(column = 0, row = 1, sticky = 'we')
            # date last
            self.__date_last = None
            self.__date_last_label = _tk.Label(master = frame, anchor = 'w', justify = 'left')
            self.__date_last_label.grid(column = 1, row = 0, sticky = 'we')
            # date next
            self.__date_next = None
            self.__date_next_label = _tk.Label(master = frame, anchor = 'w', justify = 'left')
            self.__date_next_label.grid(column = 1, row = 1, sticky = 'we')
        _date()
        # empty
        _tk.Frame(master = self).pack(side = 'left', expand = True, fill = 'x')
        # zoom
        def _zoom():
            nonlocal self
            # zoom
            self.__zoom = 100
            self.__zoom_changed = None
            self.__zoom_enabled = True
            # zoom label
            self.__zoom_label = _tk.Label(master = self)
            self.__zoom_label.pack(side = 'left')
            # zoom field
            self.__zoom_field = _tk.Scale(master = self,\
                from_ = _gui.ImageView.ZOOM_MIN, to = _gui.ImageView.ZOOM_MAX,
                command = self.__r_zoom,\
                orient = 'horizontal', showvalue = False,\
                length = 200)
            self.__zoom_field.pack(side = 'left')
        _zoom()
        # Post-init
        self.__ignore = True
        self.__update_date_last_label()
        self.__update_date_next_label()
        self.__update_zoom_field()
        self.__update_zoom_label()
        self.__ignore = False
        
    #endregion

    #region fields

    __dtformat:_objtypes.DTFormat

    __date_last:None|_dt.datetime
    __date_last_label:_tk.Label
    __date_next:None|_dt.datetime
    __date_next_label:_tk.Label

    __zoom:float
    __zoom_changed:'None|_gui.SimpleCallback[_Status]'
    __zoom_enabled:bool
    __zoom_label:_tk.Label
    __zoom_field:_tk.Scale
                             
    __ignore:bool
        
    #endregion

    #region properties

    @property
    def date_last(self):
        """ Date/time of last render """
        return self.__date_last
    @date_last.setter
    def date_last(self, value:None|_dt.datetime):
        if self.__date_last == value: return
        self.__date_last = value
        self.__update_date_last_label()

    @property
    def date_next(self):
        """ Date/time of next render """
        return self.__date_next
    @date_next.setter
    def date_next(self, value:None|_dt.datetime):
        if self.__date_next == value: return
        self.__date_next = value
        self.__update_date_next_label()

    @property
    def zoom_enabled(self):
        """ Whether or not zoom slider is enabled """
        return self.__zoom_enabled
    @zoom_enabled.setter
    def zoom_enabled(self, value:bool):
        if self.__zoom_enabled == value: return
        self.__zoom_enabled = value
        self.__zoom_field.configure(state = 'normal' if self.__zoom_enabled else 'disabled')

    @property
    def zoom(self):
        """ Zoom percentage """
        return self.__zoom
    @zoom.setter
    def zoom(self, value:float):
        self.__set_zoom(value, True)
    
    @property
    def zoom_changed(self):
        """ Invoked when the zoom percentage is changed """
        return self.__zoom_changed
    @zoom_changed.setter
    def zoom_changed(self, value:'None|_gui.SimpleCallback[_Status]'):
        self.__zoom_changed = value

    #endregion

    #region helper methods

    def __set_zoom(self, value:float, updatewidget:bool):
        if self.__zoom == value: return
        self.__zoom = value
        # Widgets
        if updatewidget: self.__update_zoom_field()
        self.__update_zoom_label() # Always update label
        # Callback
        if self.__zoom_changed is not None: self.__zoom_changed(self)

    def __set_dtlabel(self, label:_tk.Label, value:None|_dt.datetime):
        label.configure(text = "" if (value is None) else self.__dtformat.make_str(value))

    def __update_date_last_label(self):
        self.__set_dtlabel(self.__date_last_label, self.__date_last)

    def __update_date_next_label(self):
        self.__set_dtlabel(self.__date_next_label, self.__date_next)

    def __update_zoom_label(self):
        self.__zoom_label.configure(text = f"{self.__zoom}%")

    def __update_zoom_field(self):
        self.__zoom_field.set(self.__zoom)

    #endregion
    
    #region receivers

    def __r_zoom(self, *args):
        if self.__ignore: return
        self.__set_zoom(self.__zoom_field.get(), False)

    #endregion