__all__ = ['SubProcess']

import multiprocessing as _mp
import tkinter as _tk
import tkinter.ttk as _ttk

from tkinter import\
    messagebox as _messagebox

import code.engine.help as _help

from .c_SubProcessState import SubProcessState as _SubProcessState
from .c_WinUtil import WinUtil as _WinUtil

class SubProcess(_tk.Toplevel):
    """ Represents a window indicating a process """

    #region init
    
    def __init__(self, alt:bool = False, *args, **kwargs):
        """
        Initializer for SubProcess

        :param alt: Whether or not to use alternative visual
        """
        super().__init__(*args, **kwargs)
        self.config(padx = 5, pady = 5)
        self.resizable(width = False, height = False)
        self.attributes('-toolwindow', True)
        self.protocol("WM_DELETE_WINDOW", self.__r_WM_DELETE_WINDOW)
        # started, state, progress, progmsg, output, error, cancelling
        self.__started = False
        self.__state = _SubProcessState.INIT
        self.__progress = 0.0
        self.__progmsg = ""
        self.__output:None|tuple[str, ...] = None
        self.__error:None|str = None
        self.__cancelling = False
        # iqueue, oqueue
        self.__iqueue = _mp.Queue()
        self.__oqueue = _mp.Queue()
        # Widgets
        self.__alt = alt
        if self.__alt:
            _WinUtil.win_center(self, 200, 75)
            # f_label
            self.__f_label = _ttk.Label(master = self, anchor = 'n', justify = 'center')
            self.__f_label.pack(fill = 'both', expand = True)
            # f_cancel
            self.__f_cancel = _ttk.Button(master = self, command = self.__r_f_cancel, text = "Cancel")
            self.__f_cancel.pack(anchor = 's')
        else:    
            _WinUtil.win_center(self, 350, 75)
            self.columnconfigure(0, weight = 1)
            self.columnconfigure(1, weight = 0)
            self.rowconfigure(0, weight = 0)
            self.rowconfigure(1, weight = 1)
            # f_bar
            self.__f_bar = _ttk.Progressbar(master = self)
            self.__f_bar.grid(column = 0, row = 0, padx = (0, 5), sticky = 'we')
            # f_label
            self.__f_label = _ttk.Label(master = self, anchor = 'e', justify = 'right', width = 5)
            self.__f_label.grid(column = 1, row = 0, sticky = 'we')
            # f_cancel
            self.__f_cancel = _ttk.Button(master = self, command = self.__r_f_cancel, text = "Cancel")
            self.__f_cancel.grid(column = 0, row = 1, sticky = 'sw')
        # Post-init
        self.after(self.__TIMER, self.__update)
        self.__redraw()
         
    #endregion

    #region const

    __TIMER = 100

    #endregion

    #region properties

    @property
    def state(self):
        """ State of the process """
        return self.__state

    @property
    def progress(self):
        """ Progress indicator (in percent) """
        return self.__progress

    @property
    def progmsg(self):
        """ Message about current progress """
        return self.__progmsg

    @property
    def output(self):
        """ Output """
        return self.__output
    
    @property
    def error(self):
        """ Error information """
        return self.__error
         
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
        # Has process started?
        if self.__started:
            # Check output
            while not self.__oqueue.empty():
                _argv = _help.StrUtil.to_argv(self.__oqueue.get_nowait())
                self.__state = _SubProcessState(int(_argv[0]))
                match self.__state:
                    case _SubProcessState.RUNNING:
                        self.__progress = float(_argv[1])
                        self.__progmsg = _argv[2]
                    case _SubProcessState.FINISHED:
                        self.__output = tuple(_argv[1:])
                        self._on_finish()
                        self.destroy()
                        return
                    case _SubProcessState.CANCELLED:
                        self._on_cancel()
                        self.destroy()
                        return
                    case _SubProcessState.ERROR:
                        self.__error = _argv[1]
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
        if (self.__state != _SubProcessState.INIT):
            if self.__alt:
                self.__f_label.configure(text = self.__progmsg)
            else:
                self.__f_bar.configure(value = self.__progress)
                self.__f_label.configure(text = f"{round(self.__progress)}%")
        else:
            if not self.__alt:
                self.__f_bar.configure(value = 0)
            self.__f_label.configure(text = "")

    #endregion

    #region receivers

    def __r_WM_DELETE_WINDOW(self):
        self.__cancel()

    def __r_f_cancel(self):
        self.__cancel()

    #endregion

    #region abstract methods

    def _create_process(self, iqueue:_mp.Queue, oqueue:_mp.Queue) -> _mp.Process:
        """
        Called to create the process

        :param iqueue: Input queue
        :param oqueue: Output queue
        :return: Created process
        """
        raise NotImplementedError("_create_process has not been implemented")

    #endregion

    #region virtual methods

    def _on_finish(self):
        """
        Called when the process completes successfully
        """
        pass

    def _on_cancel(self):
        """
        Called when the process is cancelled by the user
        """
        pass

    def _on_error(self):
        """
        Called when the process encounters an error
        """
        pass

    #endregion