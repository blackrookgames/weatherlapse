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

from .c_SubJobUtil import SubJobUtil as _SubJobUtil

_LAYERS_EXTREMA = [ (0, 116), (0, 230), (0, 0), (0, 153), (0, 0) ]
_LAYERS_FCOLOR = [ (16, 120, 64), (16, 120, 64), (4, 4, 16), (16, 120, 64), (4, 4, 16) ]

def _convert(in_min:float, in_max:float, out_min:float, out_max:float, value:float):
    if in_min == in_max or out_min == out_max: return out_max
    return out_min + ((value - in_min) / (in_max - in_min)) * (out_max - out_min)

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

def _process(appinfodata:bytes,\
        output:_Path, options_landbg:bool, options_landout:bool, options_alpha:bool,\
        iqueue:_mp.Queue, oqueue:_mp.Queue):
    global _LAYERS_EXTREMA, _LAYERS_FCOLOR
    try:
        appinfo = _info.init_from_pickle(appinfodata)
        config = _objtypes.Config()
        config.load_from_xml_file(str(appinfo.config_path))
        # Compute output directory
        output_dir = _help.PathUtil.absolute(output, config.output)
        if not output_dir.is_dir(): _os.mkdir(output_dir)
        # Grab files
        input_files = [_f for _f in config.output.iterdir() if _f.is_file() and _f.name.endswith(".bin")]
        output_files = [output_dir.joinpath(_f.name[:-4] + ".png") for _f in input_files]
        for _i in range(len(input_files)):
            _input_file = input_files[_i]
            _output_file = output_files[_i]
            try:
                # Open input file
                _input_data = _objtypes.BinaryData()
                _input_data.load(_input_file)
                # Open input metadata
                _input_meta = _objtypes.RenderMeta()
                _input_meta.load(_io.BytesIO(_input_data[_misc.NAME_META]))
                # Open input image
                with _Image.open(_io.BytesIO(_input_data[_misc.NAME_IMAGE])) as _input_image:
                    _input_image.load()
                # Create image
                _output_image = _Image.new('RGBA', _input_image.size)
                _output_image_w, _output_image_h = _output_image.size
                # Paste background land (if requested)
                if options_landbg:
                    _fcolor = _LAYERS_FCOLOR[_input_meta.layer.value - 1]
                    with _Image.open(_io.BytesIO(_input_data[_misc.NAME_LAND_F])) as _image:
                        _min_w = min(_image.size[0], _output_image_w)
                        _min_h = min(_image.size[1], _output_image_h)
                        for _y in range(_min_h):
                            for _x in range(_min_w):
                                _rawcolor_0 = (_fcolor[0], _fcolor[1], _fcolor[2], _image.getpixel((_x, _y))[3]) # type: ignore
                                _rawcolor_1 = _output_image.getpixel((_x, _y))
                                _color = _blendColors(_rawcolor_0, _rawcolor_1) # type: ignore
                                _output_image.putpixel((_x, _y), _color)
                # Paste input image
                _extrema_min, _extrema_max = _LAYERS_EXTREMA[_input_meta.layer.value - 1]
                for _y in range(_output_image_h):
                    for _x in range(_output_image_w):
                        _rawcolor_0 = _input_image.getpixel((_x, _y))
                        _rawcolor_1 = _output_image.getpixel((_x, _y))
                        # Normalize alpha (if requested)
                        assert isinstance(_rawcolor_0, tuple)
                        if options_alpha: _rawcolor_0 = (_rawcolor_0[0], _rawcolor_0[1], _rawcolor_0[2],\
                            255 if (_extrema_min == _extrema_max)\
                            else max(0, min(255, round(_convert(_extrema_min, _extrema_max, 0, 255, _rawcolor_0[3])))))
                        # Paste
                        _color = _blendColors(_rawcolor_0, _rawcolor_1) # type: ignore
                        _output_image.putpixel((_x, _y), _color)
                # Paste background land (if requested)
                if options_landout:
                    with _Image.open(_io.BytesIO(_input_data[_misc.NAME_LAND_O])) as _image:
                        _min_w = min(_image.size[0], _output_image_w)
                        _min_h = min(_image.size[1], _output_image_h)
                        for _y in range(_min_h):
                            for _x in range(_min_w):
                                _rawcolor_0 = _image.getpixel((_x, _y))
                                _rawcolor_1 = _output_image.getpixel((_x, _y))
                                _color = _blendColors(_rawcolor_0, _rawcolor_1) # type: ignore
                                _output_image.putpixel((_x, _y), _color)
                # Save image
                _output_image.save(_output_file)
                # Next
                _SubJobUtil.output_running(oqueue, main_prog = 100 * ((_i + 1) / len(input_files)))
                if not _SubJobUtil.user_cancelled(iqueue): continue
                _SubJobUtil.output_cancelled(oqueue)
                return
            except Exception as _e: _ex = Exception(f"{_input_file.name} {_e}")
            raise _ex
        # Success!!!
        _SubJobUtil.output_finished(oqueue, _num.Pickle.pickle_I32_l(len(input_files)))
    except Exception as _e: return _SubJobUtil.output_error(oqueue, _e)