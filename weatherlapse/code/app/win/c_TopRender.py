__all__ = ['TopRender']

import datetime as _dt
import io as _io
import tkinter as _tk
import tkinter.ttk as _ttk

from PIL import\
    Image as _Image
from sys import\
    stderr as _stderr
from tkinter import\
    messagebox as _messagebox

import code.app.gui as _gui
import code.engine.objtypes as _objtypes

from code.app.c_AppInfo import AppInfo as _AppInfo
from .c_WinUtil import WinUtil as _WinUtil

from .c_TopRender_const import _NAME_IMAGE, _NAME_EXTRA
from .c_TopRender_Info import _Info
from .c_TopRender_Processor import _Processor
from .c_TopRender_Status import _Status
from .c_TopRender_Timer import _Timer

class TopRender(_tk.Tk):
    """
    Represents a render window
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for TopRender """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Weather Lapse")
        self.config(padx = 5, pady = 5)
        self.minsize(640, 480)
        _WinUtil.win_center(self, 800, 600)
        self.protocol("WM_DELETE_WINDOW", self.__r_WM_DELETE_WINDOW)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        # appinfo
        self.__appinfo = appinfo
        if self.__appinfo.iswindows:
            self.__icon = None
            self.iconbitmap(self.__appinfo.icon_path)
        else:
            self.__icon = _tk.PhotoImage(file = self.__appinfo.icon_path)
            self.iconphoto(True, self.__icon)
        # config
        self.__config = _objtypes.Config()
        self.__config.load_from_xml_file(str(self.__appinfo.config_path))
        # timer
        self.__timer = _Timer(self, self.__config.datetime)
        self.__timer.trigger = self.__r_timer
        # processor
        self.__processor = _Processor(self, self.__appinfo, self.__config)
        self.__processor.process_complete = self.__r_proccessor
        # view
        def _view():
            nonlocal self
            # view
            self.__view = _gui.ImageView(master = self)
            self.__view.grid(column = 0, row = 0, sticky = 'nswe')
            # view image
            self.__view.image_changed = self.__r_view_image_changed
            # view zoom
            self.__view.zoom_changed = self.__r_view_zoom_changed
        _view()
        # side
        def _side():
            nonlocal self
            # side
            self.__side = _tk.Frame(master = self)
            self.__side.grid(column = 1, row = 0, rowspan = 2, sticky = 'nswe')
            # info
            def __info():
                nonlocal self
                # info
                self.__side_info = _Info(self.__config, master = self.__side)
                self.__side_info.pack(fill = 'both', expand = True)
            __info()
            # clock
            def __clock():
                nonlocal self
                self.__side_clock = _tk.Label(master = self.__side, justify = 'right', anchor = 'se')
                self.__side_clock.pack(fill = 'both')
                self.__side_clock_after = self.__side_clock.after(self.__CLOCK_AFTER, self.__r_side_clock_after)
            __clock()
        _side()
        # status
        def _status():
            nonlocal self
            # status
            self.__status = _Status(self.__config.datetime.format, master = self)
            self.__status.grid(column = 0, row = 1, sticky = 'we')
            # status zoom
            self.__status.zoom_enabled = False
            self.__status.zoom_changed = self.__r_status_zoom_changed
            self.__status_zoom_ignore = False
        _status()
        # Post-init
        self.__ignore = True
        self.__status.zoom = self.__view.zoom
        self.__status.date_next = self.__timer.trigger_at
        self.__ignore = False
        
    #endregion

    #region const

    __CLOCK_AFTER = 500
        
    #endregion

    #region fields

    __appinfo:_AppInfo
    __config:_objtypes.Config
    __timer:_Timer
    __processor:_Processor

    __view:_gui.ImageView

    __side:_tk.Frame
    __side_info:_Info
    __side_clock:_tk.Label
    __side_clock_after:str

    __status:_Status
    __status_zoom_ignore:bool

    __ignore:bool

    #endregion

    #region receivers

    def __r_WM_DELETE_WINDOW(self):
        msg = _messagebox.askyesno(\
            "Stop Rendering",\
            "Are you sure you want to stop rendering?",\
            icon = 'warning')
        if not msg: return
        # Cancel timers
        self.__side_clock.after_cancel(self.__side_clock_after)
        self.__timer.cancel()
        self.__processor.cancel()
        # Now destroy
        self.destroy()

    def __r_timer(self, *args):
        self.__processor.process_start()

    def __r_proccessor(self, *args):
        # Output
        if self.__processor.output is not None:
            # Image
            with _Image.open(_io.BytesIO(self.__processor.output[_NAME_IMAGE])) as _image:
                with _Image.open(_io.BytesIO(self.__processor.output[_NAME_EXTRA])) as _extra:
                    if self.__config.layer == _objtypes.ConfigLayer.CLOUDS:
                        _newimg = _Image.alpha_composite(_extra, _image)
                    else:
                        _newimg = _Image.alpha_composite(_image, _extra)
                    self.__view.image = _newimg
        elif self.__processor.output_error is not None:
            # Error
            print("ERROR: ", file = _stderr, end = '')
            # Date/time
            if self.__processor.output_datetime is not None:
                _dt = self.__config.datetime.format.make_str(self.__processor.output_datetime)
                print(f"{_dt}: ", file = _stderr, end = '')
            # Message
            print(self.__processor.output_error, file = _stderr)
        # Last date/time
        self.__status.date_last = self.__processor.output_datetime
        self.__status.date_last_fail = self.__processor.output is None
        # Next date/time
        self.__status.date_next = self.__timer.trigger_at

    def __r_view_image_changed(self, *args):
        self.__status.zoom_enabled = self.__view.image is not None

    def __r_view_zoom_changed(self, *args):
        if self.__ignore or self.__status_zoom_ignore: return
        self.__status_zoom_ignore = True
        self.__status.zoom = self.__view.zoom
        self.__status_zoom_ignore = False

    def __r_side_clock_after(self):
        # Update
        self.__side_clock.config(text = self.__config.datetime.format.make_str(_dt.datetime.now()))
        # Next
        self.__side_clock_after = self.__side_clock.after(self.__CLOCK_AFTER, self.__r_side_clock_after)

    def __r_status_zoom_changed(self, *args):
        if self.__ignore or self.__status_zoom_ignore: return
        self.__status_zoom_ignore = True
        self.__view.zoom = self.__status.zoom
        self.__status_zoom_ignore = False

    #endregion