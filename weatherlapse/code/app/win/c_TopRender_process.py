import datetime as _dt
import hashlib as _hl
import io as _io
import multiprocessing as _mp
import requests as _rq

from pathlib import Path as _Path
from PIL import Image as _Image

import code.engine.help as _help
import code.engine.objtypes as _objtypes

from code.app.c_AppInfo import AppInfo as _AppInfo
from .c_TopRender_const import _NAME_EXTRA, _NAME_IMAGE, _NAME_META

_LAYERS = [ 'clouds_new', 'precipitation_new', 'pressure_new', 'wind_new', 'temp_new', ]
_TILE_DIM = 256

def _process(appdir:str, iswindows:bool, outdir:str, queue:_mp.Queue):
    global _LAYERS, _TILE_DIM
    # What time is it?
    dt = _dt.datetime.now()
    dt_str = f"{dt.year:04d}{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}{dt.microsecond:06d}"
    # Time to start!
    log:None|_io.TextIOWrapper = None
    try:
        appinfo = _AppInfo(_Path(appdir), iswindows)
        config = _objtypes.Config()
        config.load_from_xml_file(str(appinfo.config_path))
        # Generate path base
        path_dir = _Path(outdir)
        path_dir.mkdir(parents = True, exist_ok = True)
        path_name = f"{dt.year:04d}{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}{dt.microsecond:06d}"
        path_base = path_dir.joinpath(path_name)
        # Output
        output = _objtypes.BinaryData()
        output_path = f"{path_base}.bin"
        # Create log file
        log = open(f"{path_base}.txt", 'w')
        # Layer name
        layer_name = _LAYERS[max(0, min(len(_LAYERS) - 1, config.layer.value - 1))]
        log.write(f"Layer {layer_name}\n")
        # Fix region
        region_zoom, region_xmin, region_ymin, region_xmax, region_ymax = config.region.normalize()
        log.write("{")
        log.write(f"Zoom: {region_zoom}, ")
        log.write(f"Min X: {region_xmin}, ")
        log.write(f"Min Y: {region_ymin}, ")
        log.write(f"Max X: {region_xmax}, ")
        log.write(f"Max Y: {region_ymax}")
        log.write("}\n")
        if region_xmin == region_xmax: raise Exception("Region width cannot be zero.")
        if region_ymin == region_ymax: raise Exception("Region height cannot be zero.")
        # Compute size
        tiles_cols = region_xmax - region_xmin
        tiles_rows = region_ymax - region_ymin
        image_w = tiles_cols * _TILE_DIM
        image_h = tiles_rows * _TILE_DIM
        log.write(f"Image size {image_w}x{image_h}\n")
        # Create image
        image = _Image.new('RGBA', (image_w, image_h))
        image_params = { 'appid': config.apikey }
        log.write(f"Creating image\n")
        for _tile_y in range(tiles_rows):
            for _tile_x in range(tiles_cols):
                _x = region_xmin + _tile_x
                _y = region_ymin + _tile_y
                _url = f"https://tile.openweathermap.org/map/{layer_name}/{region_zoom}/{_x}/{_y}.png"
                log.write(f"  Tile {_x},{_y} ({_url})\n")
                # Fetch
                _res = _rq.get(_url, params = image_params)
                if _res.status_code != 200: raise Exception(f"OpenWeatherMap Status {_res.status_code}")
                # Add to image
                with _Image.open(_io.BytesIO(_res.content)) as _img:
                    _img.putalpha(255)
                    image.paste(_img, (_tile_x * _TILE_DIM, _tile_y * _TILE_DIM))
        # Save image
        log.write("Saving image\n")
        image_buf = _io.BytesIO()
        image.save(image_buf, format = 'PNG')
        output.add(_NAME_IMAGE, image_buf.getvalue())
        # Save extra
        log.write("Saving extra\n")
        extra_path = appinfo.cache_world_bg_path(config.region, config.layer == _objtypes.ConfigLayer.CLOUDS)
        with open(extra_path, 'rb') as _f: output.add(_NAME_EXTRA, _f.read())
        # Save meta
        log.write("Saving meta\n")
        meta = _objtypes.RenderMeta()
        meta.date = dt
        meta.layer = config.layer
        meta.zoom = region_zoom
        meta.min_x = region_xmin
        meta.min_y = region_ymin
        meta.max_x = region_xmax
        meta.max_y = region_ymax
        meta_bytes = _io.BytesIO()
        meta.save(meta_bytes)
        output.add(_NAME_META, meta_bytes.getvalue())
        # Save
        log.write(f"Saving output\n")
        output.save(output_path)
        # success!!!
        log.write(f"Success!!!\n")
        queue.put(_help.StrUtil.from_argv(dt_str, True, output_path))
    except Exception as _e:
        if log is not None: log.write(f"ERROR: {_e}\n")
        queue.put(_help.StrUtil.from_argv(dt_str, False, _e))
    finally:
        if log is not None: log.close()