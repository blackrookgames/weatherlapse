__all__ = ['SubExportProcess']

import multiprocessing as _mp

import tkinter.messagebox as _messagebox

import code.app.info as _info
import code.engine.num as _num

from .c_SubExportSettings import SubExportSettings as _SubExportSettings
from .c_SubJob import SubJob as _SubJob

from .c_SubExportProcess_process import _process

class SubExportProcess(_SubJob):
    """
    Represents a progress window for exporting renders
    """

    #region init

    def __init__(self, *args, **kwargs):
        """
        Initializer for SubExportProcess
        
        :raise BadOpError: Application information has not been initialized
        """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Exporting")
        # appinfo
        self.__appinfo = _info.get_info_if_init()
        
    #endregion

    #region SubJob

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue):
        args = (self.__appinfo.pickle(),\
            _SubExportSettings.output, _SubExportSettings.options_landbg,\
            _SubExportSettings.options_landout, _SubExportSettings.options_alpha,\
            iqueue, oqueue)
        return _mp.Process(target = _process, args = args)
    
    def _on_finish(self):
        assert self.output is not None
        exported = _num.Pickle.unpickle_I32_l(self.output)
        _messagebox.showinfo("Success!!!", f"Successfully exported {exported} file{('s' if (exported != 1) else '')}!")
    
    def _on_error(self):
        _messagebox.showerror("Error", self.error)

    #endregion