import ctypes as ct
from ctypes import c_uint8 as u8
from ctypes import c_uint16 as u16
from ctypes import c_uint32 as u32
from ctypes import c_uint64 as u64

from ctypes import Structure as struct
from ctypes import pointer as ptr


class bmp_file_header(struct):
    _pack_ = 1
    
    _fields_ = [
        ("signature",  u16),
        ("filesize",   u32),
        ("reserved",   u32),
        ("offset",     u32)
    ]
    # def __init__(bytes: by)

class bmp_info_header(struct):
    _pack_ = 1

    _fields_ = [
        ("size",                u32),
        ("width",               u32),
        ("height",              u32),
        ("planes",              u16),
        ("bits_per_pixel",      u16),
        ("compression",         u32),
        ("image_size",          u32),
        ("hori_res",            u32),
        ("vert_res",            u32),
        ("colors_used",         u32),
        ("important_colors",    u32)
    ]

class bmp_color_table(struct):
    class rgb(struct):
        _pack_ = 1

        _fields_ = [
            ("red",         u8),
            ("green",       u8),
            ("blue",        u8),
            ("reserved",    u8)
        ]

    _pack_ = 1
    
    _fields_ = [
        ("entry", rgb)
    ]

    def __init__(self, size: int):
        self.size = [self.rgb * size]
    
class bmp_pixel_data(struct):
    class pixel_1bit(struct):
        data: u8

    pixels: None 



class bmp_file(struct): 
    _pack_ = 1

    _fields_ = [
        ("file_header", bmp_file_header),
        ("info_header", bmp_info_header),
        ("color_table", bmp_color_table),
        ("pixel_data",  bmp_pixel_data)
    ]