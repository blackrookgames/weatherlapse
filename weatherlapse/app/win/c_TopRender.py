__all__ = ['TopRender']

import multiprocessing as _mp
import tkinter as _tk
import tkinter.ttk as _ttk

from pathlib import\
    Path as _Path
from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

import app.gui as _gui

from app.c_AppInfo import AppInfo as _AppInfo
from .c_SubConfig import SubConfig as _SubConfig
from .c_WinUtil import WinUtil as _WinUtil

def hardjob(queue):
    print("start")
    img = _Image.new('RGBA', (1024, 1024))
    for _y in range(img.size[1]):
        for _x in range(img.size[0]):
            img.putpixel((_x, _y), (_x % 256, _y % 256, 0, 255))
    img.save("./output.png")
    queue.put("./output.png") 

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
        # queue
        self.__queue = _mp.Queue(1)
        # processing
        self.__processing = False
        # view
        self.__view = _gui.ImageView(master = self)
        self.__view.grid(column = 0, row = 0, sticky = 'nswe')
        # shorttimer
        self.__shorttimer = self.after(self.__SHORTTIMER_MS, self.__shorttimer_func)
        # longtimer
        self.__longtimer = self.after(self.__LONGTIMER_MS, self.__longtimer_func)
        
    #endregion

    #region const

    __SHORTTIMER_MS = 100
    __LONGTIMER_MS = 10000

    #endregion

    #region helper methods
    
    def __shorttimer_func(self):
        if self.__processing:
            # Queue from queue
            try: data = self.__queue.get(block = False) 
            except: data = None
            if data is not None:
                # Set image
                with _Image.open(data) as image:
                    image.load()
                self.__view.set_image(image)
                # End of processing
                self.__processing = False
        # Reset timer
        self.after(self.__SHORTTIMER_MS, self.__shorttimer_func)
    
    def __longtimer_func(self):
        if not self.__processing:
            self.__processing = True
            p = _mp.Process(target = hardjob, args = (self.__queue, ))
            p.start()
        # Reset timer
        # self.after(self.__LONGTIMER_MS, self.__longtimer_func)

    #endregion