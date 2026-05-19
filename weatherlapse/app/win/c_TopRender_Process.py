import datetime as _dt
import multiprocessing as _mp

from pathlib import Path as _Path
from PIL import Image as _Image

def _process(\
        apikey:str, layer:int, outdir:str,\
        zoom:int, min_x:int, min_y:int, max_x:int, max_y:int,\
        queue:_mp.Queue):
    dt = _dt.datetime.now()
    img = _Image.new('RGBA', (1024, 1024))
    def test():
        nonlocal dt, img
        _offset = (dt.hour * 3600 + dt.minute * 60 + dt.second) 
        for _y in range(img.size[1]):
            for _x in range(img.size[0]):
                _r = _offset & 0xFF
                _g = (_offset >> 8) & 0xFF
                _b = (_offset >> 16) & 0xFF
                img.putpixel((_x, _y), (_r, _g, _b, 255))
                _offset += 15
    test()
    output_datetime = f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}"
    output_image = "./output.png"
    img.save(output_image)
    queue.put(f"\"{output_datetime}\" \"{output_image}\"")