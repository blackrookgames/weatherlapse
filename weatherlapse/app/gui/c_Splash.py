__all__ = ['Splash']

from collections.abc import\
    Iterable as _Iterable
from PIL import\
    ImageTk as _ImageTk
import tkinter as _tk
import tkinter.ttk as _ttk

from .c_Anchor import\
    Anchor as _Anchor
from .c_SplashImages import\
    SplashImages as _SplashImages

class Splash(_ttk.Frame):
    """ Represents a splash visual """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for Splash """
        super().__init__(*args, **kwargs)
        # Canvas
        self.__canvas = _tk.Canvas(\
            master = self,\
            borderwidth = 0,\
            highlightthickness = 0,\
            background = 'gray')
        self.__canvas.bind("<Configure>", self.__r_canvas_Configure)
        self.__canvas.pack(expand = True, fill = 'both')
        # Images
        self.__images = _SplashImages(self)
        # Refresh Timer
        self.__refresh_timer:None|str = None
        self.__refresh_first = True

    #endregion

    #region properties

    @property
    def images(self):
        """ Splash images """
        return self.__images

    #endregion

    #region private methods

    def __image_refresh(self, entry:_SplashImages._Entry, target_width: int, target_height: int):
        # Remove from canvas
        if entry.canvasid is not None: self.__canvas.delete(entry.canvasid)
        # Render
        entry.image = entry.source._render(max(1, target_width), max(1, target_height))
        entry.imagetk = _ImageTk.PhotoImage(entry.image)
        # Compute coordinates
        match entry.source.anchor:
            case _Anchor.NW:
                x = 0
                y = 0
            case _Anchor.N:
                x = target_width // 2
                y = 0
            case _Anchor.NE:
                x = target_width
                y = 0
            case _Anchor.W:
                x = 0
                y = target_height // 2
            case _Anchor.CENTER:
                x = target_width // 2
                y = target_height // 2
            case _Anchor.E:
                x = target_width
                y = target_height // 2
            case _Anchor.SW:
                x = 0
                y = target_height
            case _Anchor.S:
                x = target_width // 2
                y = target_height
            case _Anchor.SE:
                x = target_width
                y = target_height
            case _:
                x = 0
                y = 0
        # Add to canvas
        entry.canvasid = self.__canvas.create_image(x, y,\
            image = entry.imagetk,\
            anchor = entry.source.anchor.name.lower())
        # Success!!!
        return
    
    def __refresh_timer_func(self):
        self.__refresh_timer = None
        self.__images._refresh_entries()

    #endregion

    #region internal methods

    def _image_add(self, entry:_SplashImages._Entry, infront:None|int):
        """
        Also accessed by SplashImages
        """
        target_width = self.__canvas.winfo_width()
        target_height = self.__canvas.winfo_height()
        # Add to canvas
        self.__image_refresh(entry, target_width, target_height)
        # Adjust order
        assert entry.canvasid is not None
        self.__canvas.tag_raise(entry.canvasid, infront)
    
    def _image_remove(self, entry:_SplashImages._Entry):
        """
        Also accessed by SplashImages
        """
        # Remove from canvas
        if entry.canvasid is not None:
            self.__canvas.delete(entry.canvasid)
        # Clear data
        entry.canvasid = None
        entry.image = None
        entry.imagetk = None

    def _image_refresh(self, entries:_Iterable[_SplashImages._Entry]):
        """
        Also accessed by SplashImages
        """
        target_width = self.__canvas.winfo_width()
        target_height = self.__canvas.winfo_height()
        for entry in entries:
            self.__image_refresh(entry, target_width, target_height)

    #endregion

    #region receivers

    def __r_canvas_Configure(self, event = None):
        if self.__refresh_first:
            self.__images._refresh_entries()
            self.__refresh_first = False
        else:
            if self.__refresh_timer is not None:
                self.after_cancel(self.__refresh_timer)
            self.__refresh_timer = self.after(100, self.__refresh_timer_func)

    #endregion