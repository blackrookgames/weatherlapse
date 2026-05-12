import sys

from async_tkinter_loop import async_mainloop
from pathlib import Path

import app

def main(appinfo:app.AppInfo):
    # Create title window
    win_title = app.WinTitle(appinfo)
    win_title.mainloop()
    # async_mainloop(window)
    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    sys.exit(main(app.AppInfo(Path(sys.argv[0]))))