__all__ = ['SubExport']

import tkinter as _tk
import tkinter.ttk as _ttk

import code.app.gui as _gui
import code.engine.help as _help
import code.engine.objtypes as _objtypes

from code.app.c_AppInfo import AppInfo as _AppInfo

from .c_WinUtil import WinUtil as _WinUtil

from .c_SubExportSettings import\
    SubExportSettings as _SubExportSettings

class SubExport(_tk.Toplevel):
    """
    Represents a configuration window
    """

    #region init

    def __init__(self, appinfo:_AppInfo, *args, **kwargs):
        """ Initializer for SubExport """
        # Initialize
        super().__init__(*args, **kwargs)
        self.title("Export")
        self.resizable(width = False, height = False)
        self.config(padx = 5, pady = 5)
        self.attributes('-toolwindow', True)
        _WinUtil.win_center(self, 400, 220)
        self.__ignore = False
        # confirmed
        self.__confirmed = False
        # appinfo
        self.__appinfo = appinfo
        # Config
        self.__config = _objtypes.Config()
        self.__config.load_from_xml_file(str(self.__appinfo.config_path))
        # Fix settings
        if _SubExportSettings.output.is_absolute():
            _SubExportSettings.output = _help.PathUtil.relative(_SubExportSettings.output, self.__config.output)
        # Widgets
        def _widgets():
            nonlocal self
            def __create_labelframe(title:str):
                nonlocal self
                frame = _tk.LabelFrame(master = self.__f, padx = 5, pady = 5, text = title)
                frame.pack(fill = 'x')
                return frame
            # f
            self.__f = _tk.Frame(master = self)
            self.__f.pack(anchor = 'n', expand = True, fill = 'both')
            # f_output
            self.__f_output = __create_labelframe("Output Directory")
            # f_output_field
            self.__f_output_field = _gui.PathField(\
                master = self.__f_output)
            self.__f_output_field.dialogtitle = "Select Output Directory"
            self.__f_output_field.askdirectory = True
            self.__f_output_field.relativepath = self.__config.output
            self.__f_output_field.valuechanged = self.__r_f_output
            self.__f_output_field.pack(fill = 'x')
            # f_options
            self.__f_options = __create_labelframe("Options")
            # f_options_landbg
            self.__f_options_landbg_value = _tk.BooleanVar()
            self.__f_options_landbg_value.trace_add('write', self.__r_f_options_landbg)
            self.__f_options_landbg_field = _ttk.Checkbutton(\
                master = self.__f_options,\
                variable = self.__f_options_landbg_value,\
                text = "Show Land Background")
            self.__f_options_landbg_field.pack(fill = 'x')
            # f_options_landout
            self.__f_options_landout_value = _tk.BooleanVar()
            self.__f_options_landout_value.trace_add('write', self.__r_f_options_landout)
            self.__f_options_landout_field = _ttk.Checkbutton(\
                master = self.__f_options,\
                variable = self.__f_options_landout_value,\
                text = "Show Land Outline")
            self.__f_options_landout_field.pack(fill = 'x')
            # f_options_alpha
            self.__f_options_alpha_value = _tk.BooleanVar()
            self.__f_options_alpha_value.trace_add('write', self.__r_f_options_alpha)
            self.__f_options_alpha_field = _ttk.Checkbutton(\
                master = self.__f_options,\
                variable = self.__f_options_alpha_value,\
                text = "Normalize alpha")
            self.__f_options_alpha_field.pack(fill = 'x')
            # b
            self.__b = _tk.Frame(master = self)
            self.__b.pack(anchor = 'sw')
            # b_ok
            self.__b_ok = _ttk.Button(master = self.__b, text = "OK", command = self.__r_b_ok)
            self.__b_ok.pack(side = 'left', padx = (0, 5))
            # b_cancel
            self.__b_cancel = _ttk.Button(master = self.__b, text = "Cancel", command = self.__r_b_cancel)
            self.__b_cancel.pack(side = 'left', padx = (0, 5))
        _widgets()
        # Post-init
        self.__refresh()

    #endregion

    #region fields

    __b:_tk.Frame
    __b_ok:_ttk.Button
    __b_cancel:_ttk.Button

    __f:_tk.Frame
    __f_output:_tk.LabelFrame
    __f_output_field:_gui.PathField
    __f_options:_tk.LabelFrame
    __f_options_landbg_field:_ttk.Checkbutton
    __f_options_landbg_value:_tk.BooleanVar
    __f_options_landout_field:_ttk.Checkbutton
    __f_options_landout_value:_tk.BooleanVar
    __f_options_alpha_field:_ttk.Checkbutton
    __f_options_alpha_value:_tk.BooleanVar

    #endregion

    #region helper methods

    def __refresh(self):
        if self.__ignore: return
        self.__ignore = True
        self.__f_output_field.value = _SubExportSettings.output
        self.__f_options_landbg_value.set(_SubExportSettings.options_landbg)
        self.__f_options_landout_value.set(_SubExportSettings.options_landout)
        self.__f_options_alpha_value.set(_SubExportSettings.options_alpha)
        self.__ignore = False

    #endregion

    #region properties

    @property
    def confirmed(self):
        """ Whether or not user confirmed """
        return self.__confirmed

    #endregion

    #region receivers

    def __r_b_ok(self):
        self.__confirmed = True
        self.destroy()

    def __r_b_cancel(self):
        self.destroy()

    def __r_f_output(self, *args):
        if self.__ignore: return
        _SubExportSettings.output = self.__f_output_field.value
    
    def __r_f_options_landbg(self, *args):
        if self.__ignore: return
        _SubExportSettings.options_landbg = self.__f_options_landbg_value.get()
    
    def __r_f_options_landout(self, *args):
        if self.__ignore: return
        _SubExportSettings.options_landout = self.__f_options_landout_value.get()
    
    def __r_f_options_alpha(self, *args):
        if self.__ignore: return
        _SubExportSettings.options_alpha = self.__f_options_alpha_value.get()

    #endregion