import sys

from async_tkinter_loop import async_mainloop
from pathlib import Path

import gui
import objtypes

def main(exepath:Path):
    # Look for config file
    config = objtypes.Config()
    configpath = Path(f"{exepath}.config")
    if Path.is_file(configpath):
        config.load_from_xml_file(str(configpath))
    config.save_to_xml_file(str(configpath))
    # Create title window
    win_title = gui.WinTitle()
    win_title.mainloop()
    # async_mainloop(window)
    # Success!!!
    return 0

if __name__ == "__main__" and len(sys.argv) > 0:
    sys.exit(main(Path(sys.argv[0]).resolve()))