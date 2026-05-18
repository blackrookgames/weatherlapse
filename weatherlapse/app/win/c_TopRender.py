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
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        _WinUtil.win_center(self, 640, 480)
        # appinfo
        self.__appinfo = appinfo
        # queue
        self.__queue = _mp.Queue(1)
        # processing
        self.__processing = False
        # canvas
        self.__canvas = _tk.Canvas(master = self)
        self.__canvas.pack()
        self.__canvas_id:None|int = None
        self.__canvas_image:None|_Image.Image = None
        self.__canvas_photo:None|_ImageTk.PhotoImage = None
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
                # Delete previous
                if self.__canvas_id is not None:
                    self.__canvas.delete(self.__canvas_id)
                # Reload image
                with _Image.open(data) as self.__canvas_image:
                    self.__canvas_image.load()
                self.__canvas_photo = _ImageTk.PhotoImage(self.__canvas_image)
                self.__canvas_id = self.__canvas.create_image(0, 0, image = self.__canvas_photo, anchor = 'nw')
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
        self.after(self.__LONGTIMER_MS, self.__longtimer_func)

    #endregion