import datetime as _dt
import tkinter as _tk

import code.app.gui as _gui

import code.engine.objtypes as _objtypes

class _Timer:

    #region init

    def __init__(self, root:_tk.Tk, config:_objtypes.ConfigDateTime):
        self.__root = root
        self.__config = config
        # trigger
        def _trigger():
            nonlocal self
            # trigger
            self.__trigger = None
            # trigger at
            now = _dt.datetime.now()
            if self.__config.start is not None:
                self.__trigger_at = self.__compute_next_trigger(\
                    self.__config.start, self.__config.stop, self.__config.interval, now)
            else:
                self.__trigger_at = None if self.__compute_after_stop(now, self.__config.stop) else now
        _trigger()
        # Post-init
        self.__after = self.__root.after(self.__TIMER, self.__update)
        
    #endregion

    #region const

    __TIMER = 25

    #endregion

    #region field
    
    __root:_tk.Tk
    __config:_objtypes.ConfigDateTime

    __trigger:'None|_gui.SimpleCallback[_Timer]'
    __trigger_at:None|_dt.datetime

    __after:None|str

    #endregion

    #region helper methods
    
    @classmethod
    def __compute_after_stop(cls,\
            value:_dt.datetime, stop:None|_dt.datetime):
        return stop is not None and value >= stop
        

    @classmethod
    def __compute_next_trigger(cls,\
            start:_dt.datetime, stop:None|_dt.datetime,\
            interval:_dt.timedelta, now:_dt.datetime):
        # Determine next
        next = start
        while next < now: next += interval
        # Is stop before next?
        if cls.__compute_after_stop(next, stop):
            return None
        # No!
        return next

    def __update(self):
        # Get time
        now = _dt.datetime.now()
        # Stop timer?
        if self.__trigger_at is None:
            return # By returning here, we prevent the timer from restarting
        # Triggered?
        if self.__trigger_at is not None and now > self.__trigger_at:
            # Triggered!!!
            if self.__trigger is not None: self.__trigger(self)
            # Next trigger
            self.__trigger_at = self.__compute_next_trigger(\
                self.__trigger_at, self.__config.stop, self.__config.interval, _dt.datetime.now()) # Recheck current time
        # Next
        self.__after = self.__root.after(self.__TIMER, self.__update)

    #endregion

    #region properties

    @property
    def trigger(self):
        return self.__trigger
    @trigger.setter
    def trigger(self, value:'None|_gui.SimpleCallback[_Timer]'):
        self.__trigger = value

    @property
    def trigger_at(self):
        return self.__trigger_at

    #endregion

    #region methods

    def cancel(self):
        if self.__after is not None:
            self.__root.after_cancel(self.__after)
            self.__after = None

    #endregion