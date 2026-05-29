import os
import shutil
import sys
import tkinter.ttk as ttk

from async_tkinter_loop import async_mainloop
from pathlib import Path

import code.app as app
import code.engine as engine


def main():
    # Create title window
    win_title = app.TopTitle()
    win_title.mainloop()
    if not win_title.start: return False
    # Create render window
    win_render = app.TopRender()
    win_render.mainloop()
    # Continue
    return True

def exit():
    # Delete cache (if requested)
    appinfo = app.get_info_if_init()
    if appinfo.config_path.is_file() and appinfo.cache_dir.is_dir():
        config = engine.objtypes.Config()
        config.load_from_xml_file(str(appinfo.config_path))
        if config.deletecache: shutil.rmtree(appinfo.cache_dir)

if __name__ == "__main__" and len(sys.argv) > 0:
    app.init(Path(sys.argv[0]), os.name == 'nt')
    while main(): pass
    exit()
    sys.exit(0)