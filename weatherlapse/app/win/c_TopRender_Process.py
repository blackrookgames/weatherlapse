import datetime as _dt
import hashlib as _hl
import io as _io
import multiprocessing as _mp
import requests as _rq

from pathlib import Path as _Path
from PIL import Image as _Image

_MAXZOOM = 9
_MAXCOORDS = [ 2 ** _i for _i in range(_MAXZOOM + 1) ]
_LAYERS = [ 'clouds_new', 'precipitation_new', 'pressure_new', 'wind_new', 'temp_new', ]
_TILE_DIM = 256

def _process(\
        apikey:str, useragent:str, layer:int, outdir:str,\
        zoom:int, min_x:int, min_y:int, max_x:int, max_y:int,\
        queue:_mp.Queue):
    global _MAXZOOM, _MAXCOORDS, _LAYERS, _TILE_DIM
    def _output(args:tuple[str, ...]):
        with _io.StringIO() as _s:
            # Loop thru each argument
            for _arg in args:
                # Open quote
                _s.write("\"")
                # Loop thru each character
                for _c in _arg:
                    _o = ord(_c)
                    # Is this not a "printable" character
                    if _o < 0x20 or _o >= 0x7F:
                        if _o <= 0xFF: _s.write(f"\\x{_o:02X}")
                        else: _s.write(f"\\u{_o:04X}")
                    # Quotes or backslashes?
                    elif _o == 0x22 or _o == 0x27 or _o == 0x5C:
                        _s.write(f"\\{_c}")
                    # Anything else?
                    else: _s.write(_c)
                # Close quote
                _s.write("\" ")
            # Success!!!
            return _s.getvalue()
    # What time is it?
    dt = _dt.datetime.now()
    dt_str = f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}"
    # Time to start!
    log:None|_io.TextIOWrapper = None
    try:
        # Generate path base
        path_dir = _Path(outdir)
        path_dir.mkdir(parents = True, exist_ok = True)
        path_name = f"{dt.year:04d}{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}{dt.microsecond:06d}"
        path_base = path_dir.joinpath(path_name)
        # Create log file
        log = open(f"{path_base}.txt", 'w')
        # Fix layer
        def _layer():
            nonlocal log, layer
            assert log is not None
            # Print raw layer
            log.write(f"Input layer: {layer}\n")
            # Fix layer
            layer = max(0, min(len(_LAYERS) - 1, layer))
            layer_name = _LAYERS[layer]
            # Print fixed layer
            log.write(f"Fixed layer: {layer} ({layer_name})\n")
            # Success!!!
            return layer_name
        layer_name = _layer()
        # Fix region
        def _fixregion():
            nonlocal log, zoom, min_x, min_y, max_x, max_y
            assert log is not None
            def __str():
                nonlocal zoom, min_x, min_y, max_x, max_y
                return f"{{Zoom: {zoom}, Min X: {min_x}, Min Y: {min_y}, Max X: {max_x}, Max Y: {max_y}}}"
            def __swap(val0, val1):
                return val1, val0
            # Print raw region
            log.write(f"Input region: {__str()}\n")
            # Clamp zoom
            zoom = max(0, min(_MAXZOOM, zoom))
            # Clamp region
            maxx = _MAXCOORDS[zoom]
            min_x = max(0, min(maxx, min_x))
            min_y = max(0, min(maxx, min_y))
            max_x = max(0, min(maxx, max_x))
            max_y = max(0, min(maxx, max_y))
            # Fix min/max
            if min_x > max_x: min_x, max_x = __swap(min_x, max_x)
            if min_y > max_y: min_y, max_y = __swap(min_y, max_y)
            # Print fixed region
            log.write(f"Fixed region: {__str()}\n")
            # Make sure width and height are valid
            if min_x == max_x: raise Exception("Region width cannot be zero.")
            if min_y == max_y: raise Exception("Region height cannot be zero.")
            # Compute size
            tiles_cols = max_x - min_x
            tiles_rows = max_y - min_y
            return tiles_cols, tiles_rows, (tiles_cols * _TILE_DIM, tiles_rows * _TILE_DIM)
        tiles_cols, tiles_rows, image_size = _fixregion()
        # Background
        def _background():
            nonlocal useragent, zoom, min_x, min_y, max_x, max_y
            nonlocal log, path_base, tiles_cols, tiles_rows, image_size
            def __generatechecksum(path):
                _hash = _hl.md5()
                with open(path, 'rb') as _f:
                    for _chunk in iter(lambda: _f.read(4096), b""): _hash.update(_chunk)
                return _hash.digest()
            assert log is not None
            log.write("Retrieving background image\n")
            base = path_dir.joinpath(f"_{zoom}_{min_x}_{min_y}_{max_x}_{max_y}")
            binpath = _Path(f"{base}.bin")
            imgpath = _Path(f"{base}.png")
            # Check if background already exists
            if binpath.is_file() and imgpath.is_file():
                log.write("  Verifying\n")
                # Read expected checksum
                with open(binpath, 'rb') as _f: _expected = _f.read()
                # Generate checksum
                _checksum = __generatechecksum(imgpath)
                # Verify
                if _checksum == _expected:
                    with _Image.open(imgpath) as _image:
                        if _image.size == image_size:
                            _image.load()
                            log.write("  Found\n")
                            return _image
            # Background not found! Create it.
            log.write("  Not found. Creating\n")
            raws:list[_Image.Image] = []
            headers = { 'User-Agent': useragent }
            for _y in range(min_y, max_y):
                for _x in range(min_x, max_x):
                    log.write(f"    Tile {_x},{_y}\n")
                    # URL
                    _url = f"https://tile.openstreetmap.org/{zoom}/{_x}/{_y}.png"
                    log.write(f"      {_url}\n")
                    # Request
                    response = _rq.get(_url, headers = headers)
                    if response.status_code != 200:
                        raise Exception(f"OpenStreetMap Status {response.status_code}")
                    # Add raw image
                    with _Image.open(_io.BytesIO(response.content)) as _img: raws.append(_img.convert('RGBA'))
            log.write("  Compiling\n")
            image = _Image.new('RGBA', image_size)
            for _y in range(tiles_rows):
                for _x in range(tiles_cols):
                    image.paste(raws[_x + _y * tiles_cols], (_x * _TILE_DIM, _y * _TILE_DIM))
            image.save(imgpath)
            # Generate checksum
            with open(binpath, 'wb') as _f: _f.write(__generatechecksum(imgpath))
            # Success!!!
            log.write("  Created\n")
            return image
        background = _background()
        # Foreground
        def _foreground():
            nonlocal apikey, zoom, min_x, min_y, max_x, max_y
            nonlocal log, layer_name, tiles_cols, tiles_rows, image_size
            assert log is not None
            log.write("Creating foreground\n")
            raws:list[_Image.Image] = []
            params = { 'appid': apikey }
            for _y in range(min_y, max_y):
                for _x in range(min_x, max_x):
                    log.write(f"  Tile {_x},{_y}\n")
                    # URL
                    _url = f"https://tile.openweathermap.org/map/{layer_name}/{zoom}/{_x}/{_y}.png"
                    log.write(f"    {_url}\n")
                    # Request
                    response = _rq.get(_url, params = params)
                    if response.status_code != 200:
                        raise Exception(f"OpenWeatherMap Status {response.status_code}")
                    # Add raw image
                    with _Image.open(_io.BytesIO(response.content)) as _img: raws.append(_img.convert('RGBA'))
            log.write("  Compiling\n")
            image = _Image.new('RGBA', image_size)
            for _y in range(tiles_rows):
                for _x in range(tiles_cols):
                    image.paste(raws[_x + _y * tiles_cols], (_x * _TILE_DIM, _y * _TILE_DIM))
            return image
        foreground = _foreground()
        foreground.save(f"{path_base}.fg.png")
        # image
        log.write("Creating final image\n")
        image = _Image.alpha_composite(background, foreground)
        image_output = f"{path_base}.png"
        image.save(image_output)
        # success!!!
        log.write(f"Success!!!\n")
        queue.put(_output((dt_str, "True", image_output)))
    except Exception as _e:
        if log is not None: log.write(f"ERROR: {_e}\n")
        queue.put(_output((dt_str, "False", str(_e))))
    finally:
        if log is not None: log.close()