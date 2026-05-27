__all__ = ['SubMakeBack']

import multiprocessing as _mp

import tkinter.messagebox as _messagebox

import code.app.info as _info

from .c_SubProcess import SubProcess as _SubProcess
from .c_SubMakeBack_process import _process

class SubMakeBack(_SubProcess):
    """
    Represents a progress window for creating background images
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for SubMakeBack
        
        :raise BadOpError: Application information has not been initialized
        """
        # Initialize
        super().__init__(alt = True, *args, **kwargs)
        self.title("Rendering Background")
        # appinfo
        self.__appinfo = _info.get_info_if_init()
        
    #endregion

    #region SubProcess

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue):
        args = (self.__appinfo.app_dir, self.__appinfo.iswindows, iqueue, oqueue)
        return _mp.Process(target = _process, args = args)
    
    def _on_error(self):
        _messagebox.showerror("Error", self.error)

    #endregion