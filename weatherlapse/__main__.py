import os
import sys

from async_tkinter_loop import async_mainloop
from pathlib import Path

import app
import engine

def main(appinfo:app.AppInfo):
    # Create title window
    win_title = app.WinTitle(appinfo)
    win_title.mainloop()
    # async_mainloop(window)
    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    directory = Path(sys.argv[0])
    iswindows = os.name == 'nt'
    appinfo = app.AppInfo(directory, iswindows)
    config = engine.objtypes.Config()
    sys.exit(main(appinfo))