__all__ = ['SubMakeBack']

import multiprocessing as _mp

import tkinter.messagebox as _messagebox

import code.app.info as _info

from .c_SubJob import SubJob as _SubJob
from .c_SubMakeBack_process import _process

class SubMakeBack(_SubJob):
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
        super().__init__(*args, **kwargs)
        self.title("Rendering Background")
        # appinfo
        self.__appinfo = _info.get_info_if_init()
        
    #endregion

    #region SubJob

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue):
        args = (self.__appinfo.pickle(), iqueue, oqueue)
        return _mp.Process(target = _process, args = args)
    
    def _on_error(self):
        _messagebox.showerror("Error", self.error)

    #endregion