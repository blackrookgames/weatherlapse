__all__ = ['SubMakeBack']

import multiprocessing as _mp

import tkinter.messagebox as _messagebox

import code.engine.objtypes as _objtypes

from code.app.c_AppInfo import AppInfo as _AppInfo
from .c_SubProcess import SubProcess as _SubProcess
from .c_SubMakeBack_process import _process

class SubMakeBack(_SubProcess):
    """
    Represents a progress window for creating a .geojson file
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for SubMakeBack """
        # Initialize
        super().__init__(alt = True, *args, **kwargs)
        self.title("Rendering Background")
        # appinfo
        self.__appinfo = appinfo
        
    #endregion

    #region SubProcess

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue):
        args = (self.__appinfo.app_dir, self.__appinfo.iswindows, iqueue, oqueue)
        return _mp.Process(target = _process, args = args)
    
    def _on_error(self):
        _messagebox.showerror("Error", self.error)

    #endregion