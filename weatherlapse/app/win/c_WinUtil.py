__all__ = ['WinUtil']

import tkinter as _tk
import tkinter.ttk as _ttk

class WinUtil:
    """ Utility for window-related operations """

    @classmethod
    def win_center(cls, win:_tk.Tk|_tk.Toplevel, width:int, height:int):
        """
        Sets a window geometry so it is in the center of the screen

        :param win: Window
        :param width: Window width
        :param height: Width height
        """
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = round(screen_width / 2 - width / 2)
        y = round(screen_height / 2 - height / 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
