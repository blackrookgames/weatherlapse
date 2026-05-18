__all__ = ['ImageView']

import tkinter as _tk
import tkinter.ttk as _ttk

from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

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
        # scroll_x
        self.__scroll_x = _tk.Scrollbar(master = self, orient = _tk.HORIZONTAL)
        # scroll_y
        self.__scroll_y = _tk.Scrollbar(master = self, orient = _tk.VERTICAL)
        # canvas 
        self.__canvas = _tk.Canvas(master = self, xscrollcommand = self.__scroll_x.set, yscrollcommand = self.__scroll_y.set)
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
        # Events
        self.bind('<Configure>', self.__r_Configure)

    #endregion

    #region properties

    @property
    def image(self):
        """ Image being displayed """
        return self.__image

    #endregion

    #region helper methods

    def __fixdims(self):
        # Show/hide Horizontal Scroll
        if self.__image_tk_width > self.__width:
            if self.__scroll_x.grid_info(): return
            self.__scroll_x.grid(column = 0, row = 1, sticky = 'we')
        else:
            if not self.__scroll_x.grid_info(): return
            self.__scroll_x.grid_remove()
        # Show/hide Vertical Scroll
        if self.__image_tk_height > self.__height:
            if self.__scroll_y.grid_info(): return
            self.__scroll_y.grid(column = 1, row = 0, sticky = 'ns')
        else:
            if not self.__scroll_y.grid_info(): return
            self.__scroll_y.grid_remove()

    #endregion

    #region methods

    def set_image(self, image:None|_Image.Image):
        """
        Sets the display image\n
        NOTE: Modifications to the display image are not automatically reflected. Use redraw() to show any modifcations.

        :param image: Image to display
        """
        # Set image
        self.__image = image
        # Redraw
        self.redraw()

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
            self.__image_tk = _ImageTk.PhotoImage(self.__image)
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
        # event.delta is typically 120 on Windows; divide by -120 to scroll by 1 unit
        scroll = int(-1 * ( event.delta / 120))
        if event.state & 0x0004: # 0x0004 is Ctrl
            # TODO: Zoom in/out
            pass
        else:
            if event.state & 0x0001: # 0x0001 is Shift
                self.__canvas.xview_scroll(scroll, "units")
            else:
                self.__canvas.yview_scroll(scroll, "units")

    #endregion