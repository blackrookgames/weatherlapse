import sys

from async_tkinter_loop import async_mainloop
from pathlib import Path

import gui
import objtypes

def main(appinfo:objtypes.AppInfo):
    # Create title window
    win_title = gui.WinTitle(appinfo)
    win_title.mainloop()
    # async_mainloop(window)
    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    sys.exit(main(objtypes.AppInfo(Path(sys.argv[0]))))