import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

import app.gui as _gui
import engine.objtypes as _objtypes

from .c_SubConfig_DTField import _DTField

class _DateTime(_tk.Frame):

    #region init

    def __init__(self, config:None|_objtypes.ConfigDateTime = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # config
        self.__config = config
        # f_format
        self.__format_frame = _tk.LabelFrame(master = self, text = "Format", padx = 2, pady = 2)
        self.__format_frame.pack(fill = 'x', anchor = 'w')
        self.__format = _gui.DTFormatField(master = self.__format_frame)
        self.__format.valuechanged = self.__r_format_valuechanged
        self.__format.pack(fill = 'x', anchor = 'w')
        # f_start
        self.__start = _DTField(master = self, text = "Start", cbtext = "Start timelapse at Specified Date/Time")
        self.__start.valuechanged = self.__r_start_valuechanged
        self.__start.pack(fill = 'x')
        # f_stop
        self.__stop = _DTField(master = self, text = "Stop", cbtext = "Stop timelapse at Specified Date/Time")
        self.__stop.valuechanged = self.__r_stop_valuechanged
        if self.__config is None or self.__config.stop is None:
            self.__stop.value = _dt.datetime(9999, 12, 31) # This will be the default when user first checks the checkbox
            self.__stop.value = None
        self.__stop.pack(fill = 'x')
        # f_interval
        self.__interval_frame = _tk.LabelFrame(master = self, text = "Interval", padx = 2, pady = 2)
        self.__interval_frame.pack(fill = 'x', anchor = 'w')
        self.__interval = _gui.TimeDeltaField(master = self.__interval_frame)
        self.__interval.dialogtitle = "Configure Interval"
        self.__interval.valuechanged = self.__r_interval_valuechanged
        self.__interval.pack(fill = 'x', anchor = 'w')
        # Post-init
        self.refresh()

    #endregion

    #region receivers

    def __r_format_valuechanged(self, caller:_gui.DTFormatField):
        if self.__config is not None:
            self.__config.format = self.__format.value
        self.__start.format = self.__format.value
        self.__stop.format = self.__format.value

    def __r_start_valuechanged(self, caller:_DTField):
        if self.__config is not None:
            self.__config.start = self.__start.value

    def __r_stop_valuechanged(self, caller:_DTField):
        if self.__config is not None:
            self.__config.stop = self.__stop.value

    def __r_interval_valuechanged(self, caller:_gui.TimeDeltaField):
        if self.__config is not None:
            self.__config.interval = self.__interval.value

    #endregion

    #region methods

    def refresh(self):
        if self.__config is None: return
        # format
        self.__format.value = self.__config.format
        # start
        self.__start.value = self.__config.start
        self.__start.format = self.__format.value
        # stop
        self.__stop.value = self.__config.stop
        self.__stop.format = self.__format.value
        # interval
        self.__interval.value = self.__config.interval

    #endregion