import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

from tkinter import\
    font as _font
from typing import\
    Any as _Any

import app.gui as _gui
import engine.help as _help
import engine.objtypes as _objtypes

class _Info(_tk.Frame):

    #region init

    def __init__(self, config:_objtypes.Config, *args, **kwargs):
        # Initialize
        super().__init__(width = 300, *args, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        # config
        self.__config = config
        # treeview
        def _treeview():
            nonlocal self
            self.__treeview_tip = None
            self.__treeview_tip_item = None
            self.__treeview_tip_col = None
            # treeview
            self.__treeview = _ttk.Treeview(master = self, show = 'headings',\
                columns = self.__TREEVIEW_COLUMNS)
            for _i in range(len(self.__TREEVIEW_COLUMNS)):
                self.__treeview.heading(self.__TREEVIEW_COLUMNS[_i], text = self.__TREEVIEW_COLUMNS_TEXT[_i])
            self.__treeview.column(0, width = 75, minwidth = 50, stretch = False)
            self.__treeview.bind('<Motion>', self.__r_treeview_resize)
            self.__treeview.bind('<Button-1>', self.__r_treeview_resize) # Prevents initial click/drag on border
            self.__treeview.bind("<Motion>", self.__r_treeview_Motion)
            self.__treeview.bind("<Leave>", self.__r_treeview_Leave)
            self.__treeview.pack(fill = 'both', expand = True, padx = (5, 2.5))
            # treeview font
            self.__treeview_font = _font.Font(font = "TkDefaultFont")
            # User-agent
            self.__treeview.insert('', _tk.END, values = (\
                "User Agent", self.__config.useragent))
            # Layer
            self.__treeview.insert('', _tk.END, values = (\
                "Layer", self.__config.layer.name))
            # Output
            self.__treeview.insert('', _tk.END, values = (\
                "Output", str(self.__config.output)))
            # Region
            self.__treeview.insert('', _tk.END, values = (\
                "Region Zoom", str(self.__config.region.zoom)))
            self.__treeview.insert('', _tk.END, values = (\
                "Region Min X", str(self.__config.region.min_x)))
            self.__treeview.insert('', _tk.END, values = (\
                "Region Min Y", str(self.__config.region.min_y)))
            self.__treeview.insert('', _tk.END, values = (\
                "Region Max X", str(self.__config.region.max_x)))
            self.__treeview.insert('', _tk.END, values = (\
                "Region Max Y", str(self.__config.region.max_y)))
            # Date/Time
            if self.__config.datetime.start is not None:
                self.__treeview.insert('', _tk.END, values = (\
                    "Start", self.__config.datetime.format.make_str(self.__config.datetime.start)))
            if self.__config.datetime.stop is not None:
                self.__treeview.insert('', _tk.END, values = (\
                    "Stop", self.__config.datetime.format.make_str(self.__config.datetime.stop)))
            self.__treeview.insert('', _tk.END, values = (\
                "Interval", _help.TimeDeltaUtil.make_str(self.__config.datetime.interval)))
        _treeview()
        # Post-init
        self.__treeview_fixsize()

    #endregion

    #region const

    __TREEVIEW_COLUMNS = ('property', 'value')
    __TREEVIEW_COLUMNS_TEXT = ("Property", "Value")

    #endregion

    #region fields

    __config:_objtypes.Config

    __treeview:_ttk.Treeview
    __treeview_font:_font.Font
    __treeview_tip:_Any
    __treeview_tip_item:_Any
    __treeview_tip_col:_Any
        
    #endregion

    #region helper methods

    def __treeview_fixsize(self):
        # Start with the width of the heading text itself
        max_width = self.__treeview_font.measure(self.__TREEVIEW_COLUMNS_TEXT[0])
        for row in self.__treeview.get_children():
            # Update max width if this cell is wider
            _width = self.__treeview_font.measure(self.__treeview.set(row, 0))
            if max_width < _width: max_width = _width
        # Apply width with a small padding buffer (e.g., 20 pixels)
        self.__treeview.column(0, width = max_width + 20)

    def show_tooltip(self, text, x, y):
        # Create a borderless, floating window
        self.__treeview_tip = _tk.Toplevel(self.__treeview)
        self.__treeview_tip.wm_overrideredirect(True) # Removes window borders/title bar
        self.__treeview_tip.wm_geometry(f"+{x}+{y}")
        # Style the tooltip label (light yellow background, solid black border)
        label = _tk.Label(\
            self.__treeview_tip, text=text, justify=_tk.LEFT,\
            background="#ffffe0", relief=_tk.SOLID, borderwidth=1, padx=4, pady=2)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.__treeview_tip:
            self.__treeview_tip.destroy()
            self.__treeview_tip = None
            self.__treeview_tip_item = None
            self.__treeview_tip_col = None
        
    #endregion

    #region receivers

    def __r_treeview_resize(self, event):
        # 'identify region' detects what part of the treeview the mouse is over
        if self.__treeview.identify_region(event.x, event.y) == "separator":
            return "break"  # Intercepts and blocks the resize action
    
    def __r_treeview_Motion(self, event):
        # Identify which item and column the mouse is hovering over
        item = self.__treeview.identify_row(event.y)
        column = self.__treeview.identify_column(event.x) # Returns '#1', '#2', etc.
        # If the mouse moved to a new cell
        if item != self.__treeview_tip_item or column != self.__treeview_tip_col:
            self.__treeview_tip_item = item
            self.__treeview_tip_col = column
            self.hide_tooltip() # Clear the old tooltip
            # Ensure the mouse is actually over a valid cell, not headings/empty space
            if item and column:
                # Convert '#1' string into an integer index (0, 1, 2)
                col_idx = int(column.replace('#', '')) - 1
                row_values = self.__treeview.item(item, "values")
                if row_values and col_idx < len(row_values):
                    cell_text = str(row_values[col_idx])
                    # Position the tooltip slightly offset from the mouse pointer
                    self.show_tooltip(cell_text, event.x_root + 15, event.y_root + 10)
        # If the mouse leaves valid cells but stays inside the widget, hide tooltip
        elif not item or not column:
            self.hide_tooltip()
    
    def __r_treeview_Leave(self, event):
        self.hide_tooltip()

    #endregion