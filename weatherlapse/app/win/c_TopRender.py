__all__ = ['TopRender']

import multiprocessing as _mp
import tkinter as _tk
import tkinter.ttk as _ttk

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import app.gui as _gui
import engine.objtypes as _objtypes

from app.c_AppInfo import AppInfo as _AppInfo
from .c_WinUtil import WinUtil as _WinUtil

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
        _WinUtil.win_center(self, 640, 480)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        # appinfo
        self.__appinfo = appinfo
        if self.__appinfo.iswindows:
            self.__icon = None
            self.iconbitmap(self.__appinfo.iconpath)
        else:
            self.__icon = _tk.PhotoImage(file = self.__appinfo.iconpath)
            self.iconphoto(True, self.__icon)
        # config
        self.__config = _objtypes.Config()
        self.__config.load_from_xml_file(str(self.__appinfo.configpath))
        # timer
        self.__timer = _Timer(self, self.__config.datetime)
        self.__timer.trigger = self.__r_timer
        # processor
        self.__processor = _Processor(self, self.__config, self.__appinfo.appdir)
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
        # status
        def _status():
            nonlocal self
            # status
            self.__status = _Status(master = self)
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

    #region fields

    __appinfo:_AppInfo
    __config:_objtypes.Config
    __timer:_Timer
    __processor:_Processor

    __view:_gui.ImageView

    __status:_Status
    __status_zoom_ignore:bool

    __ignore:bool

    #endregion

    #region receivers

    def __r_timer(self, *args):
        self.__processor.process_start()

    def __r_proccessor(self, *args):
        if self.__processor.output_datetime is not None:
            # Last date/time
            self.__status.date_last = self.__processor.output_datetime
            # Last image
            self.__view.image = self.__processor.output_image
        # Next date/time
        self.__status.date_next = self.__timer.trigger_at

    def __r_view_image_changed(self, *args):
        self.__status.zoom_enabled = self.__view.image is not None

    def __r_view_zoom_changed(self, *args):
        if self.__ignore or self.__status_zoom_ignore: return
        self.__status_zoom_ignore = True
        self.__status.zoom = self.__view.zoom
        self.__status_zoom_ignore = False

    def __r_status_zoom_changed(self, *args):
        if self.__ignore or self.__status_zoom_ignore: return
        self.__status_zoom_ignore = True
        self.__view.zoom = self.__status.zoom
        self.__status_zoom_ignore = False

    #endregion