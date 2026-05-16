import datetime as _dt
import tkinter as _tk
import tkinter.ttk as _ttk

class _Win(_tk.Toplevel):

    #region init

    def __init__(self, initvalue:_dt.timedelta, *args, **kwargs):
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Pick Time Delta")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        # Size
        WIN_WIDTH = 300
        WIN_HEIGHT = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_x = round(screen_width / 2 - WIN_WIDTH / 2)
        win_y = round(screen_height / 2 - WIN_HEIGHT / 2)
        self.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}+{win_x}+{win_y}')
        # value
        self.__value = initvalue
        self.__temp = self.__value
        # Widgets
        def _widgets():
            nonlocal self
            def __form():
                nonlocal self
                # f
                self.__f = _tk.Frame(master = self)
                self.__f.pack(anchor = 'n', expand = True, fill = 'both')
            def __buttons():
                nonlocal self
                # b
                self.__b = _tk.Frame(master = self)
                self.__b.pack(anchor = 'sw')
                # b_ok
                self.__b_ok = _ttk.Button(master = self.__b, text = "OK", command = self.__r_b_ok)
                self.__b_ok.pack(side = 'left')
                # b_cancel
                self.__b_cancel = _ttk.Button(master = self.__b, text = "Cancel", command = self.__r_b_cancel)
                self.__b_cancel.pack(side = 'left', padx = (5, 0))
            __form()
            __buttons()
        _widgets()

    #endregion

    #region fields

    __f:_tk.Frame
    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_cancel:_ttk.Button

    #endregion

    #region properties

    @property
    def value(self):
        """ Date/time value """
        return self.__value

    #endregion

    #region receivers

    def __r_b_ok(self):
        self.__value = self.__temp
        self.destroy()

    def __r_b_cancel(self):
        self.destroy()

    #endregion