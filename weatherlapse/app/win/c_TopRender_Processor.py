import datetime as _dt
import multiprocessing as _mp
import re as _re
import tkinter as _tk

from pathlib import Path as _Path
from PIL import Image as _Image

import app.gui as _gui
import engine.help as _help
import engine.objtypes as _objtypes

from .c_TopRender_Process import _process

class _Processor:

    #region init

    def __init__(self, root:_tk.Tk, config:_objtypes.Config, reldir:_Path):
        self.__root = root
        self.__config = config
        self.__reldir = reldir
        self.__queue = _mp.Queue(maxsize = 1)
        self.__processing = False
        self.__process_start = False
        self.__process_complete = None
        self.__output_datetime = None
        self.__output_image = None
        # Post-init
        self.__root.after(self.__TIMER, self.__update)
        
    #endregion

    #region field
    
    __root:_tk.Tk
    __config:_objtypes.Config
    __reldir:_Path

    __queue:_mp.Queue

    __processing:bool

    __process_start:bool
    __process_complete:'None|_gui.SimpleCallback[_Processor]'

    __output_datetime:None|_dt.datetime
    __output_image:None|_Image.Image

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
    def output_image(self):
        return self.__output_image

    @property
    def output_datetime(self):
        return self.__output_datetime

    #endregion

    #region helper methods

    def __update(self):
        # Are we processing?
        if self.__processing:
            # Queue from queue
            try: output = self.__queue.get(block = False) 
            except: output = None
            if output is not None:
                try:
                    output_args = _help.StrUtil.to_argv(output)
                    # output_datetime
                    def _output_datetime(arg):
                        values = _re.split(r'[ /:]', arg)
                        return _dt.datetime(\
                            year = int(values[0]), month = int(values[1]), day = int(values[2]),\
                            hour = int(values[3]), minute = int(values[4]), second = int(values[5]), microsecond = int(values[6]))
                    self.__output_datetime = _output_datetime(output_args[0])
                    # output_image
                    with _Image.open(output_args[1]) as self.__output_image:
                        self.__output_image.load()
                except:
                    self.__output_datetime = None
                    self.__output_image = None
                # End of processing
                self.__processing = False
                if self.__process_complete is not None: self.__process_complete(self)
        # No! Should we start processing?
        elif self.__process_start:
            self.__process_start = False
            self.__processing = True
            p_args = (\
                self.__config.apikey, self.__config.layer.value, self.__config.output,\
                self.__config.region.zoom,\
                self.__config.region.min_x, self.__config.region.min_y,\
                self.__config.region.max_x, self.__config.region.max_y,\
                self.__queue, )
            p = _mp.Process(target = _process, args = p_args)
            p.start()
        # Next
        self.__root.after(self.__TIMER, self.__update)

    #endregion

    #region methods

    def process_start(self):
        self.__process_start = True

    #endregion