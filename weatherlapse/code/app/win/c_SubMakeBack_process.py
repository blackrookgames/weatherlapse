import geopandas as _gpd
import io as _io
import mapbox_vector_tile as _mvt
import matplotlib as _mpl
_mpl.use('agg') # Must be called before importing pyplot
import matplotlib.pyplot as _mplplt
import multiprocessing as _mp
import os as _os
import pandas as _pd
import requests as _requests
import shapely.geometry as _shp_geo
import shapely.ops as _shp_ops

from pathlib import Path as _Path
from PIL import Image as _Image
from typing import Callable as _Callable

from ...engine.objtypes.c_Config import Config as _Config
from ..c_AppInfo import AppInfo as _AppInfo
from .c_SubProcessUtil import SubProcessUtil as _SubProcessUtil

_INPUT_DIM = 2048
_OUTPUT_DIM = 256

def _process(appdir:str, iswindows:bool, iqueue:_mp.Queue, oqueue:_mp.Queue):
    global _INPUT_DIM, _OUTPUT_DIM
    def __percent(num:float, den:float):
        return round(100 * (num / den))
    def __cancelled():
        nonlocal iqueue, oqueue
        if not _SubProcessUtil.user_cancelled(iqueue):
            return False
        _SubProcessUtil.output_cancelled(oqueue)
        return True
    try:
        appinfo = _AppInfo(_Path(appdir), iswindows)
        config = _Config()
        config.load_from_xml_file(str(appinfo.config_path))
        if __cancelled(): return
        # Create cache directory (if it doesn't exist)
        if not appinfo.cache_dir.is_dir():
            _os.mkdir(appinfo.cache_dir)
        # Fix region
        region_zoom, region_min_x, region_min_y, region_max_x, region_max_y = config.region.normalize()
        tile_cols = region_max_x - region_min_x
        tile_rows = region_max_y - region_min_y
        tile_total = tile_cols * tile_rows
        if (tile_cols == 0): raise Exception("Width cannot be zero.")
        if (tile_rows == 0): raise Exception("Height cannot be zero.")
        # Fetch
        MSG_FETCH = "Fetching world coordinates"
        _SubProcessUtil.output_running(oqueue, message = MSG_FETCH)
        _headers = { "User-Agent": config.useragent }
        rawgeos:dict[int, _gpd.GeoDataFrame] = {}
        for _i in range(tile_total):
            # Fetch
            _x = region_min_x + _i % tile_cols
            _y = region_min_y + _i // tile_cols
            _url = f"https://vector.openstreetmap.org/shortbread_v1/{region_zoom}/{_x}/{_y}.mvt"
            _req = _requests.get(_url, headers = _headers)
            if _req.status_code != 200:
                raise Exception(f"{_url}\nStatus Code {_req.status_code}")
            # Decode
            _decoded = _mvt.decode(_req.content)
            for _layer_name, _layer_data in _decoded.items():
                # Make sure this is the ocean
                if _layer_name != "ocean": continue
                # Extract features
                _features = []
                for _feature in _layer_data["features"]:
                    # Extract properties (attributes)
                    _feature_props = _feature["properties"]
                    # Convert the MVT geometry dict into a Shapely geometry object
                    _feature_geom = _shp_geo.shape(_feature["geometry"])
                    # Combine geometry and properties into a single dictionary
                    feature_dict = {"geometry": _feature_geom, **_feature_props}
                    _features.append(feature_dict)
                # Create GeoDataFrame
                if _features: rawgeos[_i] = _gpd.GeoDataFrame(_features, crs = "EPSG:3857")
            # Next
            if __cancelled(): return
            _SubProcessUtil.output_running(oqueue, message = f"{MSG_FETCH} {__percent(_i + 1, tile_total)}%")
        # Render
        def __render(msg:str, geoconverter:_Callable[[_gpd.GeoDataFrame], _gpd.GeoDataFrame],\
                *plot_args, **plot_kwargs):
            global _INPUT_DIM, _OUTPUT_DIM
            nonlocal appinfo
            nonlocal tile_cols, tile_rows
            nonlocal rawgeos
            # Create output
            _SubProcessUtil.output_running(oqueue, message = msg)
            outputs:list[_gpd.GeoDataFrame] = []
            _i = 0
            for _rawgeo_offset, _rawgeo_data in rawgeos.items():
                # Convert
                _output = geoconverter(_rawgeo_data)
                # Translate and add
                outputs.append(_output.geometry.translate(\
                    xoff = (_rawgeo_offset % tile_cols) * _INPUT_DIM,\
                    yoff = (tile_rows - 1 - (_rawgeo_offset // tile_cols)) * _INPUT_DIM)) # type: ignore
                # Next
                _i += 1
                if __cancelled(): return
                _SubProcessUtil.output_running(oqueue, message = f"{msg} {__percent(_i, len(rawgeos))}%")
            output = _pd.concat(outputs)
            # Render output
            ax = output.plot(*plot_args, **plot_kwargs)
            ax.margins(0)
            ax.set_aspect('equal')
            ax.set_xlim(0, tile_cols * _INPUT_DIM)
            ax.set_ylim(0, tile_rows * _INPUT_DIM)
            _mplplt.axis('off') # Remove coordinates for a clean PNG
            fig = _mplplt.gcf() # Get current figure
            fig.set_size_inches(tile_cols, tile_rows)
            fig.subplots_adjust(left = 0, right = 1, bottom = 0, top = 1, wspace = 0, hspace = 0)
            buf = _io.BytesIO()
            fig.savefig(buf, format = 'png', dpi = _OUTPUT_DIM, pad_inches = 0.0, transparent = True)
            _mplplt.close(fig)
            return buf
        def __geo_outline(input:_gpd.GeoDataFrame):
            # Generate ALL boundaries (captures exterior paths AND interior continent holes)
            output = input.copy()
            output['geometry'] = output.boundary
            # Explode the resulting MultiLineStrings into individual LineString rows
            output = output.explode(index_parts = False)
            # Standardize the geometries to clean LineStrings
            output['geometry'] = [_shp_geo.LineString(_geom.coords) if _geom else None for _geom in output.geometry] # type: ignore
            # Get the absolute outer edges of the dataset frame
            xmin, ymin, xmax, ymax = output.total_bounds
            def __strip_canvas_borders(line):
                nonlocal xmin, ymin, xmax, ymax
                TOLERANCE = 0.1
                if not line: return None
                coords = list(line.coords)
                clean_segments = []
                # Evaluate every individual point-to-point segment
                for i in range(len(coords) - 1):
                    p1, p2 = coords[i], coords[i+1]
                    # Check if BOTH points sit on the exact same border wall
                    on_left   = abs(p1[0] - xmin) < TOLERANCE and abs(p2[0] - xmin) < TOLERANCE
                    on_right  = abs(p1[0] - xmax) < TOLERANCE and abs(p2[0] - xmax) < TOLERANCE
                    on_bottom = abs(p1[1] - ymin) < TOLERANCE and abs(p2[1] - ymin) < TOLERANCE
                    on_top    = abs(p1[1] - ymax) < TOLERANCE and abs(p2[1] - ymax) < TOLERANCE
                    # If the segment belongs to the outer frame, discard it
                    if on_left or on_right or on_bottom or on_top:
                        continue
                    clean_segments.append(_shp_geo.LineString([p1, p2]))
                if not clean_segments:
                    return None
                # Stitch the surviving non-border pieces back into a continuous line
                return _shp_ops.linemerge(clean_segments)
            # Apply the segment-level filter
            output['geometry'] = output.geometry.apply(__strip_canvas_borders) # type: ignore
            # Drop any lines that were completely made of border edges
            output = output[output.geometry.notnull()]
            output = output.explode(index_parts=False)
            # Return
            return output
        # Render outline
        outline_buf = __render(\
            "Rendering outline", __geo_outline,\
            edgecolor = 'black', linewidth = 0.3)
        if outline_buf is None: return
        with open(appinfo.cache_world_bg_path(config.region, False), 'wb') as _f:
            _f.write(outline_buf.getvalue())
        # Render fill
        fill_buf = __render(\
            "Rendering fill", lambda _input: _input,\
            color = 'blue')
        if fill_buf is None: return
        with _Image.open(fill_buf).convert("RGBA") as _rawimg:
            # Generate lookup table
            _COLOR_R = 16
            _COLOR_G = 120
            _COLOR_B = 64
            _table = [\
                _COLOR_R for i in range(256)] +\
                [_COLOR_G for i in range(256)] +\
                [_COLOR_B for i in range(256)] +\
                [i for i in range(255, -1, -1)]
            # Apply the point transformation
            _img = _rawimg.point(_table)
            _img.save(appinfo.cache_world_bg_path(config.region, True))
        # Success!!!
        _SubProcessUtil.output_finished(oqueue)
    except Exception as _e: return _SubProcessUtil.output_error(oqueue, _e)