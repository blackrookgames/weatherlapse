__all__ = ['SubExportProcess']

import multiprocessing as _mp

import tkinter.messagebox as _messagebox

from code.app.c_AppInfo import AppInfo as _AppInfo
from .c_SubExportSettings import SubExportSettings as _SubExportSettings
from .c_SubProcess import SubProcess as _SubProcess

from .c_SubExportProcess_process import _process

class SubExportProcess(_SubProcess):
    """
    Represents a progress window for exporting renders
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for SubExportProcess """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Exporting")
        # appinfo
        self.__appinfo = appinfo
        
    #endregion

    #region SubProcess

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue):
        args = (self.__appinfo.app_dir, self.__appinfo.iswindows,\
            _SubExportSettings.output, _SubExportSettings.options_landbg,\
            _SubExportSettings.options_landout, _SubExportSettings.options_alpha,\
            iqueue, oqueue)
        return _mp.Process(target = _process, args = args)
    
    def _on_finish(self):
        assert self.output is not None
        exported = int(self.output[0])
        _messagebox.showinfo("Success!!!", f"Successfully exported {exported} file{('s' if (exported != 1) else '')}!")
    
    def _on_error(self):
        _messagebox.showerror("Error", self.error)

    #endregion