import calendar as _cal
import datetime as _dt
import math as _math
import tkinter as _tk
import tkinter.ttk as _ttk

from dataclasses import\
    dataclass as _dataclass
from PIL import\
    Image as _Image,\
    ImageTk as _ImageTk

from .c_SimpleCallback import SimpleCallback as _SimpleCallback

class _Calendar(_tk.Frame):
    
    #region init

    def __init__(self, *args, **kwargs):
        super().__init__(takefocus = True, *args, **kwargs)
        self.__ignore = False
        # value
        self.__value:_dt.date = _dt.date(2000, 1, 1)
        # valuechanged
        self.__valuechanged:None|_SimpleCallback[_Calendar] = None
        # highlighted
        self.__highlighted = -1
        # canvas
        def _canvas():
            nonlocal self
            # canvas
            self.__canvas = _tk.Canvas(master = self, height = 140, background = 'white')
            self.__canvas.bind('<Configure>', self.__r_canvas_Configure)
            self.__canvas.bind('<Button-1>', self.__r_canvas_Button_1)
            self.__canvas.bind('<ButtonRelease-1>', self.__r_canvas_ButtonRelease_1)
            self.__canvas.pack(fill = 'x')
            self.__canvas_x0 = 0
            self.__canvas_y0 = 0
            self.__canvas_x1 = 0
            self.__canvas_y1 = 0
            self.__canvas_width = 0
            self.__canvas_height = 0
            # canvas_current
            self.__canvas_current = self.__canvas.create_rectangle(0, 0, 0, 0, fill = '#AAAAFF')
            # canvas_border
            self.__canvas_border = self.__canvas.create_rectangle(0, 0, 0, 0,\
                outline = self.__OUTLINE_NOFOCUS)
            # canvas_hlines
            self.__canvas_hlines = [self.__canvas.create_line(0, 0, 0, 0,\
                fill = self.__OUTLINE_NOFOCUS)\
                for _ in range(6)]
            # canvas_vlines
            self.__canvas_vlines = [self.__canvas.create_line(0, 0, 0, 0,\
                fill = self.__OUTLINE_NOFOCUS)\
                for _ in range(6)]
            # canvas_headers
            self.__canvas_headers = [\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Su',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Mo',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Tu',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'We',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Th',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Fr',\
                    fill = self.__TEXT_INMONTH),\
                self.__canvas.create_text(0, 0, anchor = 'center', text = 'Sa',\
                    fill = self.__TEXT_INMONTH),]
            # canvas_days
            self.__canvas_days = [self.__canvas.create_text(0, 0, anchor = 'center', text = '31')\
                for _ in range(7 * 6)]
            self.__canvas_days_dates = [_dt.date(2000, 1, 1) for _ in self.__canvas_days]
            # canvas_highlight
            self.__canvas_highlight = self.__canvas.create_rectangle(0, 0, 0, 0,\
                outline = 'gray')
        _canvas()
        # events
        self.bind("<FocusIn>", self.__r_FocusIn)
        self.bind("<FocusOut>", self.__r_FocusOut)
        self.bind('<Left>', self.__r_Left)
        self.bind('<Right>', self.__r_Right)
        self.bind('<Up>', self.__r_Up)
        self.bind('<Down>', self.__r_Down)
        self.bind('<Home>', self.__r_Home)
        self.bind('<End>', self.__r_End)
        self.bind('<Prior>', self.__r_Prior)
        self.bind('<Next>', self.__r_Next)
        self.bind('<Shift-Prior>', self.__r_Shift_Prior)
        self.bind('<Shift-Next>', self.__r_Shift_Next)
        # Post-init
        self.__update_widget()

    #endregion

    #region const

    __OUTLINE_FOCUS = 'black'
    __OUTLINE_NOFOCUS = 'gray'

    __TEXT_INMONTH = 'black'
    __TEXT_OUTMONTH = 'gray'

    #endregion

    #region fields

    __canvas:_tk.Canvas
    __canvas_x0:int 
    __canvas_y0:int 
    __canvas_x1:int 
    __canvas_y1:int 
    __canvas_width:int 
    __canvas_height:int 
    __canvas_current:int
    __canvas_border:int
    __canvas_hlines:list[int]
    __canvas_vlines:list[int]
    __canvas_headers:list[int]
    __canvas_days:list[int]
    __canvas_days_dates:list[_dt.date]
    __canvas_highlight:int

    #endregion

    #region properties

    @property
    def value(self):
        """ Calendar/time value """
        return self.__value
    @value.setter
    def value(self, value:_dt.date):
        self.__set_value(value, True)

    @property
    def valuechanged(self):
        """ Called when the value is changed """
        return self.__valuechanged
    @valuechanged.setter
    def valuechanged(self, valuechanged:'None|_SimpleCallback[_Calendar]'):
        self.__valuechanged = valuechanged

    #endregion

    #region helper methods

    @classmethod
    def __month_range(cls, date:_dt.date):
        start, numdays = _cal.monthrange(date.year, date.month)
        start = (start + 1) % 7 # This will make Sunday = 0 and Monday = 1
        return start, numdays
    
    @classmethod
    def __month_start(cls, date:_dt.date):
        start, _ = cls.__month_range(date)
        return start

    @classmethod
    def __month_numdays(cls, date:_dt.date):
        _, numdays = _cal.monthrange(date.year, date.month)
        return numdays

    @classmethod
    def __prev_month(cls, date:_dt.date):
        prev_lastday = date.replace(day = 1) - _dt.timedelta(days = 1)
        prev_day = min(prev_lastday.day, date.day)
        return _dt.date(prev_lastday.year, prev_lastday.month, prev_day)
    
    @classmethod
    def __next_month(cls, date:_dt.date):
        next = date.replace(day = 1) + _dt.timedelta(days = 31)
        next_day = min(cls.__month_numdays(next), date.day)
        return _dt.date(next.year, next.month, next_day)
    
    @classmethod
    def __change_year(cls, date:_dt.date, year:int):
        new = _dt.date(year, date.month, 1)
        return _dt.date(new.year, new.month, min(cls.__month_numdays(new), date.day))
    
    @classmethod
    def __change_month(cls, date:_dt.date, month:int):
        new = _dt.date(date.year, month, 1)
        return _dt.date(new.year, new.month, min(cls.__month_numdays(new), date.day))

    def __compute_highlighted(self, x:float, y:float):
        return _math.floor(self.__iderp_x(x)) + _math.floor(self.__iderp_y(y)) * 7 - 7
        
    def __derp_x(self, x:float):
        return self.__canvas_x0 + (x / 7.0) * self.__canvas_width

    def __derp_y(self, y:float):
        return self.__canvas_y0 + (y / 7.0) * self.__canvas_height
    
    def __iderp_x(self, x:float):
        if self.__canvas_width <= 0.0: return 0.0
        return ((x - self.__canvas_x0) / self.__canvas_width) * 7.0

    def __iderp_y(self, y:float):
        if self.__canvas_height <= 0.0: return 0.0
        return ((y - self.__canvas_y0) / self.__canvas_height) * 7.0

    def __set_value(self, value:_dt.date, updatewidget:bool):
        if self.__value == value: return
        self.__value = value
        # Update widget
        if updatewidget: self.__update_widget()
        # Callback
        if self.__valuechanged is not None: self.__valuechanged(self)

    def __update_widget(self):
        # canvas_days
        prev_month = self.__prev_month(self.__value)
        next_month = self.__next_month(self.__value)
        currmonth_start, currmonth_days = self.__month_range(self.__value)
        prevmonth_days = self.__month_numdays(prev_month)
        for _i in range(len(self.__canvas_days)):
            _rel = _i - currmonth_start
            if _rel < 0:
                _color = self.__TEXT_OUTMONTH
                _date = _dt.date(prev_month.year, prev_month.month, prevmonth_days + 1 + _rel)
            elif _rel >= currmonth_days:
                _color = self.__TEXT_OUTMONTH
                _date = _dt.date(next_month.year, next_month.month, 1 + _rel - currmonth_days)
            else:
                _color = self.__TEXT_INMONTH
                _date = _dt.date(self.__value.year, self.__value.month, 1 + _rel)
            self.__canvas.itemconfig(self.__canvas_days[_i], fill = _color, text = str(_date.day))
            self.__canvas_days_dates[_i] = _date
        # canvas_current (do this after canvas_days)
        self.__pos_canvas_current()
        # canvas_highlight
        self.__pos_canvas_highlight()
    
    def __update_colors(self, focused:bool):
        outline = self.__OUTLINE_FOCUS if focused else self.__OUTLINE_NOFOCUS
        # canvas_border
        self.__canvas.itemconfig(self.__canvas_border, outline = outline)
        # canvas_hlines
        for _line in self.__canvas_hlines:
            self.__canvas.itemconfig(_line, fill = outline)
        # canvas_vlines
        for _line in self.__canvas_vlines:
            self.__canvas.itemconfig(_line, fill = outline)

    def __pos_canvas_current(self):
        # Find index
        index = -1
        for _i in range(len(self.__canvas_days_dates)):
            if self.__canvas_days_dates[_i] != self.__value:
                continue
            index = _i
            break
        # Position
        x = index % 7
        y = index // 7
        self.__canvas.coords(self.__canvas_current,\
            self.__derp_x(x), self.__derp_y(y + 1.0),\
            self.__derp_x(x + 1.0), self.__derp_y(y + 2.0))

    def __pos_canvas_highlight(self):
        if self.__highlighted >= 0:
            x = self.__highlighted % 7
            y = self.__highlighted // 7
            self.__canvas.coords(self.__canvas_highlight,\
                self.__derp_x(x) + 1.0, self.__derp_y(y + 1.0) + 1.0,\
                self.__derp_x(x + 1.0) - 1.0, self.__derp_y(y + 2.0) - 1.0)
            self.__canvas.itemconfig(self.__canvas_highlight, state = 'normal')
        else:
            self.__canvas.itemconfig(self.__canvas_highlight, state = 'hidden')

    #endregion

    #region receivers

    def __r_FocusIn(self, event = None):
        self.__update_colors(True)

    def __r_FocusOut(self, event = None):
        self.__highlighted = -1
        self.__update_colors(False)
        self.__pos_canvas_highlight()

    def __r_Left(self, event = None):
        newdate = self.__value
        try: newdate -= _dt.timedelta(days = 1)
        except: pass
        self.__set_value(newdate, True)

    def __r_Right(self, event = None):
        newdate = self.__value
        try: newdate += _dt.timedelta(days = 1)
        except: pass
        self.__set_value(newdate, True)
    
    def __r_Up(self, event = None):
        newdate = self.__value
        try: newdate -= _dt.timedelta(days = 7)
        except: pass
        self.__set_value(newdate, True)

    def __r_Down(self, event = None):
        newdate = self.__value
        try: newdate += _dt.timedelta(days = 7)
        except: pass
        self.__set_value(newdate, True)

    def __r_Home(self, event = None):
        self.__set_value(self.__value.replace(day = 1), True)

    def __r_End(self, event = None):
        self.__set_value(self.__value.replace(day = self.__month_numdays(self.__value)), True)

    def __r_Prior(self, event = None):
        try: newdate = self.__prev_month(self.__value)
        except: return
        self.__set_value(newdate, True)

    def __r_Next(self, event = None):
        try: newdate = self.__next_month(self.__value)
        except: return
        self.__set_value(newdate, True)

    def __r_Shift_Prior(self, event = None):
        try: newdate = self.__change_year(self.__value, self.__value.year - 1)
        except: return
        self.__set_value(newdate, True)

    def __r_Shift_Next(self, event = None):
        try: newdate = self.__change_year(self.__value, self.__value.year + 1)
        except: return
        self.__set_value(newdate, True)

    def __r_canvas_Button_1(self, event):
        # Make sure window is in focus
        if self.winfo_toplevel().focus_displayof() is None:
            return
        # Gain focus
        self.focus_set()
        # Highlight hovered item
        self.__highlighted = self.__compute_highlighted(event.x, event.y)
        self.__pos_canvas_highlight()

    def __r_canvas_ButtonRelease_1(self, event):
        # Make sure highlighted item and hovered item match
        if self.__highlighted >= 0 and self.__highlighted == self.__compute_highlighted(event.x, event.y):
            self.__set_value(self.__canvas_days_dates[self.__highlighted], True)
        # Reset highlight
        self.__highlighted = -1
        self.__pos_canvas_highlight()

    def __r_canvas_Configure(self, event = None):
        # canvas_x0, canvas_y0, canvas_x1, canvas_y1
        self.__canvas_x0 = 2
        self.__canvas_y0 = 2
        self.__canvas_x1 = self.__canvas.winfo_width() - 3
        self.__canvas_y1 = self.__canvas.winfo_height() - 3
        self.__canvas_width = self.__canvas_x1 - self.__canvas_x0
        self.__canvas_height = self.__canvas_y1 - self.__canvas_y0
        # canvas_current
        self.__pos_canvas_current()
        # canvas_border
        self.__canvas.coords(self.__canvas_border,\
            self.__canvas_x0, self.__canvas_y0, self.__canvas_x1, self.__canvas_y1)
        # canvas_hlines
        for _i in range(len(self.__canvas_hlines)):
            _line = self.__canvas_hlines[_i]
            _y = self.__derp_y(_i + 1.0)
            self.__canvas.coords(_line, self.__canvas_x0, _y, self.__canvas_x1, _y)
        # canvas_vlines
        for _i in range(len(self.__canvas_vlines)):
            _line = self.__canvas_vlines[_i]
            _x = self.__derp_x(_i + 1.0)
            self.__canvas.coords(_line, _x, self.__canvas_y0, _x, self.__canvas_y1)
        # canvas_headers
        _y = self.__derp_y(0.5)
        for _i in range(len(self.__canvas_headers)):
            _header = self.__canvas_headers[_i]
            _x = self.__derp_x(_i + 0.5)
            self.__canvas.coords(_header, _x, _y)
        # canvas_days
        for _i in range(len(self.__canvas_days)):
            _day = self.__canvas_days[_i]
            _x = self.__derp_x(_i % 7 + 0.5)
            _y = self.__derp_y(_i // 7 + 1.5)
            self.__canvas.coords(_day, _x, _y)
        # canvas_highlight
        self.__pos_canvas_highlight()

    #endregion

    #region methods

    def change_year(self, year:int):
        new = self.__change_year(self.__value, year)
        self.__set_value(new, True)

    def change_month(self, month:int):
        if month < 1 or month > 12: raise ValueError("Month is invalid.")
        new = self.__change_month(self.__value, month)
        self.__set_value(new, True)

    #endregion