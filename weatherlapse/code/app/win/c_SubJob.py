__all__ = ['SubJob']

import multiprocessing as _mp
import tkinter as _tk
import tkinter.ttk as _ttk

from tkinter import\
    messagebox as _messagebox

import code.app.info as _info

from .c_SubJobState import SubJobState as _SubJobState
from .c_WinUtil import WinUtil as _WinUtil

from .c_SubJob_OQEntry import _OQEntry

class SubJob(_tk.Toplevel):
    """ Represents a window indicating a job """

    #region init
    
    def __init__(self,\
        show_main_desc:bool = True,\
        show_main_bar:bool = True,\
        show_sub_desc:bool = False,\
        show_sub_bar:bool = False,\
        *args, **kwargs):
        """
        Initializer for SubJob

        :param show_main_desc: Whether or not to display main progress description
        :param show_main_bar: Whether or not to display main progress bar
        :param show_sub_desc: Whether or not to display sub progress description
        :param show_sub_bar: Whether or not to display sub progress bar
        :raise BadOpError: Application information has not been initialized
        """
        super().__init__(*args, **kwargs)
        self.config(padx = 5, pady = 5)
        self.resizable(width = False, height = False)
        self.protocol("WM_DELETE_WINDOW", self.__r_WM_DELETE_WINDOW)
        # appinfo
        self.__appinfo = _info.get_info_if_init()
        if self.__appinfo.iswindows: self.attributes('-toolwindow', True)
        # Process
        self.__started = False
        self.__state = _SubJobState.INIT
        self.__main_desc = ""
        self.__main_prog = 0.0
        self.__sub_desc = ""
        self.__sub_prog = 0.0
        self.__output = None
        self.__error = None
        self.__cancelling = False
        self.__iqueue = _mp.Queue()
        self.__oqueue = _mp.Queue()
        # Widgets
        def _widgets():
            # wf
            self.__wf = _tk.Frame(master = self)
            self.__wf.pack(fill = 'x')
            # wf_main_desc
            self.__wf_main_desc = _ttk.Label(master = self.__wf, justify = 'left')
            # wf_main_bar
            self.__wf_main_bar = _ttk.Progressbar(master = self.__wf)
            # wf_sub_desc
            self.__wf_sub_desc = _ttk.Label(master = self.__wf, justify = 'left')
            # wf_sub_bar
            self.__wf_sub_bar = _ttk.Progressbar(master = self.__wf)
            # w_cancel
            self.__w_cancel = _ttk.Button(master = self, command = self.__r_w_cancel, text = "Cancel")
            self.__w_cancel.pack(anchor = 'w')
        _widgets()
        # Show/hide
        self.__show_main_desc = show_main_desc
        self.__show_main_bar = show_main_bar
        self.__show_sub_desc = show_sub_desc
        self.__show_sub_bar = show_sub_bar
        # Dirty
        self.__isdirty = True
        # Post-init
        self.after(self.__TIMER, self.__update)
        self.__redraw()
         
    #endregion

    #region const

    __TIMER = 100
    __WIN_WIDTH = 350

    #endregion

    #region fields
    
    __appinfo:_info.Info

    __started:bool
    __state:_SubJobState
    __main_desc:str
    __main_prog:float
    __sub_desc:str
    __sub_prog:float
    __output:None|bytes
    __error:None|str
    __cancelling:bool
    __iqueue:_mp.Queue
    __oqueue:_mp.Queue

    __wf:_tk.Frame
    __wf_main_desc:_ttk.Label
    __wf_main_bar:_ttk.Progressbar
    __wf_sub_desc:_ttk.Label
    __wf_sub_bar:_ttk.Progressbar
    __w_cancel:_ttk.Button

    __show_main_desc:bool
    __show_main_bar:bool
    __show_sub_desc:bool
    __show_sub_bar:bool

    __isdirty:bool

    #endregion

    #region properties

    @property
    def state(self):
        """ Job state """
        return self.__state
    
    @property
    def main_desc(self):
        """ Main progress description """
        return self.__main_desc

    @property
    def main_prog(self):
        """ Main progress (in percent) """
        return self.__main_prog
    
    @property
    def sub_desc(self):
        """ Main progress description """
        return self.__sub_desc

    @property
    def sub_prog(self):
        """ Main progress (in percent) """
        return self.__sub_prog

    @property
    def output(self):
        """ Job output """
        return self.__output
    
    @property
    def error(self):
        """ Information about error that occurred during job """
        return self.__error
    
    @property
    def show_main_desc(self):
        """ Whether or not to display main progress description """
        return self.__show_main_desc
    @show_main_desc.setter
    def show_main_desc(self, value:bool):
        self.show_main_desc = value 
        self.__isdirty = True
    
    @property
    def show_main_bar(self):
        """ Whether or not to display main progress bar  """
        return self.__show_main_bar
    @show_main_bar.setter
    def show_main_bar(self, value:bool):
        self.show_main_bar = value 
        self.__isdirty = True
    
    @property
    def show_sub_desc(self):
        """ Whether or not to display sub progress description """
        return self.__show_sub_desc
    @show_sub_desc.setter
    def show_sub_desc(self, value:bool):
        self.show_sub_desc = value 
        self.__isdirty = True
    
    @property
    def show_sub_bar(self):
        """ Whether or not to display sub progress bar  """
        return self.__show_sub_bar
    @show_sub_bar.setter
    def show_sub_bar(self, value:bool):
        self.show_sub_bar = value 
        self.__isdirty = True
         
    #endregion

    #region helper methods

    def __cancel(self):
        # Make sure user hasn't cancelled already
        if self.__cancelling: return
        # Warn user
        msg = _messagebox.askyesno(\
            "Cancel",\
            "Are you sure you want to cancel",\
            icon = 'warning')
        if not msg: return
        # Cancel
        self.__cancelling = True
        self.__iqueue.put_nowait('CANCEL')
        self.title("Cancelling")

    def __update(self):
        # Has job started?
        if self.__started:
            # Check output
            while not self.__oqueue.empty():
                _oqentry = _OQEntry.unpickle(self.__oqueue.get_nowait())
                self.__state = _oqentry.state
                match self.__state:
                    case _SubJobState.RUNNING:
                        self.__main_desc = _oqentry.data.main_desc # type: ignore
                        self.__main_prog = _oqentry.data.main_prog # type: ignore
                        self.__sub_desc = _oqentry.data.sub_desc # type: ignore
                        self.__sub_prog = _oqentry.data.sub_prog # type: ignore
                    case _SubJobState.FINISHED:
                        self.__output = _oqentry.data.data # type: ignore
                        self._on_finish()
                        self.destroy()
                        return
                    case _SubJobState.CANCELLED:
                        self._on_cancel()
                        self.destroy()
                        return
                    case _SubJobState.ERROR:
                        self.__error = _oqentry.data.message # type: ignore
                        self._on_error()
                        self.destroy()
                        return
        # No! Start it.
        else:
            self.__started = True
            p = self._create_process(self.__iqueue, self.__oqueue)
            p.start()
        # Redraw
        self.__redraw()
        # Next
        self.after(self.__TIMER, self.__update)
        
    def __redraw(self):
        # Is display dirty?
        if self.__isdirty:
            # Remove widgets
            if self.__wf_main_desc.winfo_ismapped(): self.__wf_main_desc.pack_forget()
            if self.__wf_main_bar.winfo_ismapped(): self.__wf_main_bar.pack_forget()
            if self.__wf_sub_desc.winfo_ismapped(): self.__wf_sub_desc.pack_forget()
            if self.__wf_sub_bar.winfo_ismapped(): self.__wf_sub_bar.pack_forget()
            # Add widgets back
            if self.__show_main_desc: self.__wf_main_desc.pack(fill = 'x')
            if self.__show_main_bar: self.__wf_main_bar.pack(fill = 'x')
            if self.__show_sub_desc: self.__wf_sub_desc.pack(fill = 'x')
            if self.__show_sub_bar: self.__wf_sub_bar.pack(fill = 'x')
            # Fix window size
            self.update_idletasks()
            _WinUtil.win_center(self, self.__WIN_WIDTH, self.winfo_reqheight())
            # Mark as clean
            self.__isdirty = False
        # Update display content
        if not (self.__state == _SubJobState.INIT or self.__cancelling):
            self.__wf_main_desc.configure(text = self.__main_desc)
            self.__wf_sub_desc.configure(text = self.__sub_desc)
        else:
            self.__wf_main_desc.configure(text = "")
            self.__wf_sub_desc.configure(text = "")
        if self.__state != _SubJobState.INIT:
            self.__wf_main_bar.configure(value = self.__main_prog)
            self.__wf_sub_bar.configure(value = self.__sub_prog)
        else:
            self.__wf_main_bar.configure(value = 0.0)
            self.__wf_sub_bar.configure(value = 0.0)

    #endregion

    #region receivers

    def __r_WM_DELETE_WINDOW(self):
        self.__cancel()

    def __r_w_cancel(self):
        self.__cancel()

    #endregion

    #region abstract methods

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue) -> _mp.Process:
        """
        Called to create the job process

        :param iqueue: Input queue
        :param oqueue: Output queue
        :return: Created job process
        """
        raise NotImplementedError("_create_process has not been implemented")

    #endregion

    #region virtual methods

    def _on_finish(self):
        """
        Called when the job completes successfully
        """
        pass

    def _on_cancel(self):
        """
        Called when the job is cancelled by the user
        """
        pass

    def _on_error(self):
        """
        Called when the job encounters an error
        """
        pass


    #endregion