import datetime as _dt
import multiprocessing as _mp
import re as _re
import tkinter as _tk

from pathlib import Path as _Path
from PIL import Image as _Image

import code.app.gui as _gui
import code.engine.help as _help
import code.engine.num as _num
import code.engine.objtypes as _objtypes

from code.app.c_AppInfo import AppInfo as _AppInfo

from .c_TopRender_process import _process, _NAME_IMAGE

class _Processor:

    #region init

    def __init__(self, root:_tk.Tk, appinfo:_AppInfo, config:_objtypes.Config):
        self.__root = root
        self.__appinfo = appinfo
        self.__config = config
        self.__queue = _mp.Queue(maxsize = 1)
        self.__processing = False
        self.__process_start = False
        self.__process_complete = None
        self.__output = None
        self.__output_error = None
        self.__output_datetime = None
        # Post-init
        self.__after = self.__root.after(self.__TIMER, self.__update)
        
    #endregion

    #region field
    
    __root:_tk.Tk
    __appinfo:_AppInfo
    __config:_objtypes.Config

    __queue:_mp.Queue

    __processing:bool

    __process_start:bool
    __process_complete:'None|_gui.SimpleCallback[_Processor]'

    __output:None|_objtypes.BinaryData
    __output_error:None|str
    __output_datetime:None|_dt.datetime

    __after:None|str

    #endregion

    #region const

    __TIMER = 100

    #endregion

    #region properties

    @property
    def process_complete(self):
        return self.__process_complete
    @process_complete.setter
    def process_complete(self, value:'None|_gui.SimpleCallback[_Processor]'):
        self.__process_complete = value

    @property
    def output(self):
        return self.__output

    @property
    def output_error(self):
        return self.__output_error

    @property
    def output_datetime(self):
        return self.__output_datetime

    #endregion

    #region helper methods

    def __update(self):
        # Are we processing?
        if self.__processing:
            # Queue from queue
            if not self.__queue.empty():
                output_argv = _help.StrUtil.to_argv(self.__queue.get())
                # Get date/time
                def _output_datetime(arg):
                    return _dt.datetime(\
                        year = int(arg[0:4]), month = int(arg[4:6]), day = int(arg[6:8]),\
                        hour = int(arg[8:10]), minute = int(arg[10:12]), second = int(arg[12:14]), microsecond = int(arg[14:]))
                self.__output_datetime = _output_datetime(output_argv[0])
                # Was it successful?
                if _num.Parse.to_bool(output_argv[1]):
                    self.__output = _objtypes.BinaryData()
                    self.__output.load(output_argv[2])
                # No! What happened?
                else:
                    self.__output_error = output_argv[2]
                    self.__output = None
                # End of processing
                self.__processing = False
                if self.__process_complete is not None: self.__process_complete(self)
        # No! Should we start processing?
        elif self.__process_start:
            self.__process_start = False
            self.__processing = True
            p_outdir = _help.PathUtil.absolute(self.__config.output, self.__appinfo.parent_dir)
            p_args = (str(self.__appinfo.app_dir), self.__appinfo.iswindows, str(p_outdir), self.__queue)
            p = _mp.Process(target = _process, args = p_args)
            p.start()
        # Next
        self.__after = self.__root.after(self.__TIMER, self.__update)

    #endregion

    #region methods

    def process_start(self):
        self.__process_start = True

    def cancel(self):
        if self.__after is not None:
            self.__root.after_cancel(self.__after)
            self.__after = None

    #endregion