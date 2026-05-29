import io as _io
import multiprocessing as _mp
import os as _os

from pathlib import Path as _Path
from PIL import Image as _Image

import code.app.info as _info
import code.app.misc as _misc
import code.engine.help as _help
import code.engine.num as _num
import code.engine.objtypes as _objtypes

from .c_SubExportSettings import SubExportSettings as _SubExportSettings
from .c_SubJobUtil import SubJobUtil as _SubJobUtil
    
def _fill(value, length:int):
    return [value for _ in range(length)]

def _extrema_table(extrema:tuple[int, int]):
    _min, _max = extrema
    if _min == _max: return _fill(255, 256)
    _relmax = _max - _min
    return [max(0, min(255, round(255 * ((_i - _min) / _relmax)))) for _i in range(256)]

_LAYERS_NORMALS_EXTREMA = [ (0, 116), (0, 230), (0, 0), (0, 153), (0, 0) ]
_LAYERS_NORMALS = [\
    ([_i % 256 for _i in range(256 * 3)] + _extrema_table(_extrema))\
    for _extrema in _LAYERS_NORMALS_EXTREMA]

_LAYERS_COLORS_FCOLOR = [ (16, 120, 64), (16, 120, 64), (4, 4, 16), (16, 120, 64), (4, 4, 16) ]
_LAYERS_COLORS = [\
    (_fill(_fcolor[0], 256) + _fill(_fcolor[1], 256) + _fill(_fcolor[2], 256) + [_i for _i in range(256)])\
    for _fcolor in _LAYERS_COLORS_FCOLOR]

def _blendColors(fg:tuple[int, int, int, int], bg:tuple[int, int, int, int]):
    if bg[3] == 0: return fg
    r0 = fg[0] / 255
    g0 = fg[1] / 255
    b0 = fg[2] / 255
    a0 = fg[3] / 255
    r1 = bg[0] / 255
    g1 = bg[1] / 255
    b1 = bg[2] / 255
    a1 = bg[3] / 255
    aa = (1 - a0) * a1 + a0
    a01 = round(aa * 255)
    r01 = round((((1 - a0) * a1 * r1 + a0 * r0) / aa) * 255)
    g01 = round((((1 - a0) * a1 * g1 + a0 * g0) / aa) * 255)
    b01 = round((((1 - a0) * a1 * b1 + a0 * b0) / aa) * 255)
    return (r01, g01, b01, a01)

def _verify_image_size(img:_Image.Image, target_size:tuple[int, int]):
    if img.size == target_size: return img
    return img.resize(target_size, _Image.Resampling.NEAREST)

def _process(_appinfo:bytes, _settings:bytes, iqueue:_mp.Queue, oqueue:_mp.Queue):
    global _LAYERS_NORMALS, _LAYERS_COLORS
    try:
        appinfo = _info.Info.unpickle(_appinfo)
        settings = _SubExportSettings.unpickle(_settings)
        config = _objtypes.Config()
        config.load_from_xml_file(str(appinfo.config_path))
        # Input/output
        _inou_info = _SubJobUtil.RunInfo()
        def _inou():
            nonlocal iqueue, oqueue
            nonlocal _inou_info
            # Show progress
            _SubJobUtil.output_running2(oqueue, _inou_info)
            # Shall we continue?
            if not _SubJobUtil.user_cancelled(iqueue): return True
            _SubJobUtil.output_cancelled(oqueue)
            return False
        # Compute output directory
        output_dir = _help.PathUtil.absolute(settings.output, config.output)
        if not output_dir.is_dir(): _os.mkdir(output_dir)
        # Grab files
        input_files = [_f for _f in config.output.iterdir() if _f.is_file() and _f.name.endswith(".bin")]
        output_files = [output_dir.joinpath(_f.name[:-4] + ".png") for _f in input_files]
        _inou_info.main_prog.maxx = len(input_files)
        for _i in range(len(input_files)):
            _input_file = input_files[_i]
            _output_file = output_files[_i]
            try:
                _inou_info.main_prog.value = _i
                _inou_info.sub_desc = _output_file.name
                _inou_info.sub_prog.value = 0
                _inou_info.sub_prog.maxx = 0
                if not _inou(): return
                # Open input file
                _input_data = _objtypes.BinaryData()
                _input_data.load(_input_file)
                # Open input metadata
                _input_meta = _objtypes.RenderMeta()
                _input_meta.load(_io.BytesIO(_input_data[_misc.NAME_META]))
                _input_layer_index = _input_meta.layer.value - 1
                # Open input image
                _input_image = _Image.open(_io.BytesIO(_input_data[_misc.NAME_IMAGE])).convert('RGBA')
                if settings.options_alpha:
                    _input_image = _input_image.point(_LAYERS_NORMALS[_input_layer_index])
                # Create image
                _output_image = _Image.new('RGBA', _input_image.size)
                _output_image_w, _output_image_h = _output_image.size
                # Get image layers
                _imagelayers:list[_Image.Image] = []
                if settings.options_landbg:
                    _image = _Image.open(_io.BytesIO(_input_data[_misc.NAME_LAND_F])).convert('RGBA')
                    _image = _verify_image_size(_image, _output_image.size)
                    _imagelayers.append(_image.point(_LAYERS_COLORS[_input_layer_index]))
                _imagelayers.append(_input_image)
                if settings.options_landout:
                    _image = _Image.open(_io.BytesIO(_input_data[_misc.NAME_LAND_O])).convert('RGBA')
                    _image = _verify_image_size(_image, _output_image.size)
                    _imagelayers.append(_image)
                # Create final render
                _inou_info.sub_prog.maxx = _output_image_h
                for _y in range(_output_image_h):
                    _inou_info.sub_prog.value = _y
                    for _x in range(_output_image_w):
                        _color = (0, 0, 0, 0)
                        _pos = (_x, _y)
                        for _imagelayer in _imagelayers:
                            _color = _blendColors(_imagelayer.getpixel(_pos), _color) # type: ignore
                        _output_image.putpixel((_x, _y), _color)
                    if not _inou(): return
                _inou_info.sub_prog.value = _inou_info.sub_prog.maxx
                # Save final render
                _output_image.save(_output_file)
                # Next
                continue
            except Exception as _e: _ex = Exception(f"{_input_file.name} {_e}")
            raise _ex
        _inou_info.main_prog.value = _inou_info.main_prog.maxx
        _inou_info.sub_desc = ""
        if not _inou(): return
        # Success!!!
        _SubJobUtil.output_finished(oqueue, _num.Pickle.pickle_I32_l(len(input_files)))
    except Exception as _e: return _SubJobUtil.output_error(oqueue, _e)