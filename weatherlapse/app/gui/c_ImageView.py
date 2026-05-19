__all__ = ['ImageView']

import tkinter as _tk
import tkinter.ttk as _ttk

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

from .c_SimpleCallback import\
    SimpleCallback as _SimpleCallback

class ImageView(_tk.Frame):
    """ Represents an image view """

    #region init

    def __init__(self, *args, **kwargs):
        """ Initializer for ImageView """
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.__width = 0
        self.__height = 0
        # zoom
        self.__zoom = 100.0
        self.__zoom_timer:None|str = None
        self.__zoom_changed:None|_SimpleCallback[ImageView] = None
        # scroll_x
        self.__scroll_x = _tk.Scrollbar(master = self, orient = _tk.HORIZONTAL)
        # scroll_y
        self.__scroll_y = _tk.Scrollbar(master = self, orient = _tk.VERTICAL)
        # canvas 
        self.__canvas = _tk.Canvas(master = self, background = '#808080',\
            xscrollcommand = self.__scroll_x.set, yscrollcommand = self.__scroll_y.set)
        self.__canvas.bind_all("<MouseWheel>", self.__r_canvas_MouseWheel)
        self.__canvas.grid(column = 0, row = 0, sticky = 'nswe')
        self.__scroll_x.configure(command = self.__canvas.xview)
        self.__scroll_y.configure(command = self.__canvas.yview)
        # image
        self.__image:None|_Image.Image = None
        self.__image_tk:None|_ImageTk.PhotoImage = None
        self.__image_id:None|int = None
        self.__image_tk_width = 0
        self.__image_tk_height = 0
        self.__image_changed:None|_SimpleCallback[ImageView] = None
        # Events
        self.bind('<Configure>', self.__r_Configure)

    #endregion

    #region const

    ZOOM_MIN = 10
    """ Minimum zoom percentage """

    ZOOM_MAX = 200
    """ Maximum zoom percentage """

    #endregion

    #region properties

    @property
    def zoom(self):
        """ Zoom percentage """
        return self.__zoom
    @zoom.setter
    def zoom(self, value:float):
        if self.__zoom == value: return
        self.__zoom = value
        self.__zoom_timer_set()
        if self.__zoom_changed is not None: self.__zoom_changed(self)
    
    @property
    def zoom_changed(self):
        """ Invoked when the zoom percentage is changed """
        return self.__zoom_changed
    @zoom_changed.setter
    def zoom_changed(self, value:'None|_SimpleCallback[ImageView]'):
        self.__zoom_changed = value

    @property
    def image(self):
        """
        Display image\n
        NOTE: Modifications to the display image are not automatically reflected. Use redraw() to show any modifcations.
        """
        return self.__image
    @image.setter
    def image(self, value:None|_Image.Image):
        if self.__image is value: return
        self.__image = value
        self.redraw()
        if self.__image_changed is not None: self.__image_changed(self)
    
    @property
    def image_changed(self):
        """ Invoked when the display image is changed """
        return self.__image_changed
    @image_changed.setter
    def image_changed(self, value:'None|_SimpleCallback[ImageView]'):
        self.__image_changed = value

    #endregion

    #region helper methods

    def __zoom_timer_set(self):
        if self.__zoom_timer is not None:
            self.after_cancel(self.__zoom_timer)
        self.__zoom_timer = self.after(50, self.__zoom_timer_trigger)

    def __zoom_timer_trigger(self):
        self.__zoom_timer = None
        self.redraw()

    def __fixdims(self):
        # Show/hide Horizontal Scroll
        if self.__image_tk_width > self.__width:
            if not self.__scroll_x.grid_info():
                self.__scroll_x.grid(column = 0, row = 1, sticky = 'we')
        else:
            if self.__scroll_x.grid_info():
                self.__scroll_x.grid_remove()
        # Show/hide Vertical Scroll
        if self.__image_tk_height > self.__height:
            if not self.__scroll_y.grid_info():
                self.__scroll_y.grid(column = 1, row = 0, sticky = 'ns')
        else:
            if self.__scroll_y.grid_info():
                self.__scroll_y.grid_remove()

    #endregion

    #region methods

    def redraw(self):
        """ Redraws the display image, reflecting any modifcations made to the image """
        # Delete previous
        if self.__image_id is not None:
            self.__canvas.delete(self.__image_id)
            self.__image_tk = None
            self.__image_id = None
            self.__image_tk_width = 0
            self.__image_tk_height = 0
        # Create new
        if self.__image is not None:
            new_width = max(1, round(self.__image.size[0] * (self.__zoom / 100.0)))
            new_height = max(1, round(self.__image.size[1] * (self.__zoom / 100.0)))
            self.__image_tk = _ImageTk.PhotoImage(self.__image.resize((new_width, new_height), _Image.Resampling.NEAREST))
            self.__image_id = self.__canvas.create_image(0, 0, image = self.__image_tk, anchor = 'nw')
            self.__image_tk_width = self.__image_tk.width()
            self.__image_tk_height = self.__image_tk.height()
            self.__canvas.configure(scrollregion = (0, 0, self.__image_tk_width, self.__image_tk_height))
        # Fix dimensions
        self.__fixdims()

    #endregion

    #region helper methods

    def __r_Configure(self, event = None):
        self.__width = self.winfo_width()
        self.__height = self.winfo_height()
        self.__fixdims()

    def __r_canvas_MouseWheel(self, event):
        if self.__image is None: return
        # event.delta is typically 120 on Windows; divide by -120 to scroll by 1 unit
        scroll = int(-1 * ( event.delta / 120))
        if event.state & 0x0004: # 0x0004 is Ctrl
            zoom = self.__zoom + int(10 * ( event.delta / 120))
            if zoom < self.ZOOM_MIN: zoom = self.ZOOM_MIN
            if zoom > self.ZOOM_MAX: zoom = self.ZOOM_MAX
            if self.__zoom != zoom:
                self.__zoom = zoom
                self.redraw()
                if self.__zoom_changed is not None: self.__zoom_changed(self)
        else:
            if event.state & 0x0001: # 0x0001 is Shift
                self.__canvas.xview_scroll(scroll, "units")
            else:
                self.__canvas.yview_scroll(scroll, "units")

    #endregion