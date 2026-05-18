import os
import sys
import tkinter.ttk as ttk

from async_tkinter_loop import async_mainloop
from pathlib import Path

import app
import engine

def main(appinfo:app.AppInfo):
    # Create title window
    win_title = app.TopTitle(appinfo)
    win_title.mainloop()
    # async_mainloop(window)
    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    apppath = Path(sys.argv[0])
    iswindows = os.name == 'nt'
    appinfo = app.AppInfo(apppath, iswindows)
    config = engine.objtypes.Config()
    sys.exit(main(appinfo))