__all__ = ['TopTitle']

import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path
from tkinter import\
    messagebox as _messagebox

import code.app.gui as _gui
import code.app.info as _info
import code.engine.objtypes as _objtypes

from .c_SubConfig import SubConfig as _SubConfig
from .c_SubExport import SubExport as _SubExport
from .c_SubExportProcess import SubExportProcess as _SubExportProcess
from .c_SubMakeBack import SubMakeBack as _SubMakeBack
from .c_SubProcessState import SubProcessState as _SubProcessState
from .c_WinUtil import WinUtil as _WinUtil

class TopTitle(_tk.Tk):
    """
    Represents a title window
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for TopTitle
        
        :raise BadOpError: Application information has not been initialized
        """
        # appinfo
        self.__appinfo = _info.get_info_if_init()
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Weather Lapse")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _WinUtil.win_center(self, 400, 250)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, minsize = 50)
        # start
        self.__start = False
        # icon
        if self.__appinfo.iswindows:
            self.__icon = None
            self.iconbitmap(self.__appinfo.icon_path)
        else:
            self.__icon = _tk.PhotoImage(file = self.__appinfo.icon_path)
            self.iconphoto(True, self.__icon)
        # splash
        self.__splash = _gui.Splash(master = self)
        self.__splash.grid(column = 0, row = 0, columnspan = 3, sticky = 'nsew')
        self.__splash.images.add(_gui.SplashImage(\
            self.__appinfo.assets_dir.joinpath("splash.png"),\
            anchor = _gui.Anchor.CENTER,\
            letterbox = False))
        self.__splash.images.add(_gui.SplashImage(\
            self.__appinfo.assets_dir.joinpath("logo.png"),\
            anchor = _gui.Anchor.N,\
            letterbox = True))
        # start
        self.__button_start = _ttk.Button(\
            master = self,\
            command = self.__r_button_start,\
            text = "Start")
        self.__button_start.grid(column = 0, row = 1, padx = (0, 2.5), pady = (5, 0), sticky = 'nsew')
        # export
        self.__button_export = _ttk.Button(\
            master = self,\
            command = self.__r_button_export,\
            text = "Export")
        self.__button_export.grid(column = 1, row = 1, padx = (2.5, 2.5), pady = (5, 0), sticky = 'nsew')
        # config
        self.__button_config = _ttk.Button(\
            master = self,\
            command = self.__r_button_config,\
            text = "Config")
        self.__button_config.grid(column = 2, row = 1, padx = (2.5, 0), pady = (5, 0), sticky = 'nsew')
        # Post init
        self.__refresh()

    #endregion

    #region properties

    @property
    def start(self):
        """ Whether or not user clicked start """
        return self.__start

    #endregion

    #region helper methods

    def __refresh(self):
        # Refresh Start button
        if self.__appinfo.config_path.is_file():
            self.__button_start.config(state = 'normal')
            self.__button_export.config(state = 'normal')
        else:
            self.__button_start.config(state = 'disabled')
            self.__button_export.config(state = 'disabled')

    #endregion

    #region receivers

    def __r_button_start(self):
        # Open config
        config = _objtypes.Config()
        config.load_from_xml_file(str(self.__appinfo.config_path))
        # Create background
        bg_path_o = self.__appinfo.cache_world_bg_path(config.region, False)
        bg_path_f = self.__appinfo.cache_world_bg_path(config.region, True)
        if not (bg_path_o.is_file() and bg_path_f.is_file()):
            win = _SubMakeBack(master = self)
            _WinUtil.show_dialog(win, self)
            if win.state != _SubProcessState.FINISHED: return
        # Start
        self.__start = True
        self.destroy()

    def __r_button_export(self):
        # Settings
        win_settings = _SubExport(master = self)
        _WinUtil.show_dialog(win_settings, self)
        if not win_settings.confirmed: return
        # Export
        win_process = _SubExportProcess(master = self)
        _WinUtil.show_dialog(win_process, self)

    def __r_button_config(self):
        win = _SubConfig(master = self)
        _WinUtil.show_dialog(win, self)
        self.__refresh()

    #endregion