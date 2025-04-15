import ctypes as ct
from ctypes import c_uint8 as u8
from ctypes import c_uint16 as u16
from ctypes import c_uint32 as u32
from ctypes import c_uint64 as u64

from ctypes import Structure as struct
from ctypes import LittleEndianStructure as le_struct

from ctypes import Union as union

from ctypes import pointer as ptr

from enum import Enum


class BMPFileHeader(struct):
    _pack_ = 1
    
    _fields_ = [
        ("signature",  u16),
        ("filesize",   u32),
        ("reserved",   u32),
        ("offset",     u32)
    ]
    # def __init__(bytes: by)

class BMPInfoHeader(struct):
    class CompressionValue(Enum):
        BI_RGB = 0
        BI_RLE8 = 1
        BI_RLE4 = 2
        BI_BITFIELDS = 3
        BI_JPEG = 4
        BI_PNG = 5
        BI_ALPHABITFIELDS = 6
        BI_CMYK = 11
        BI_CMYKRLE8 = 12
        BI_CMYKRLE4 = 13

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

class BMPColorTable(struct):
    class RGB(le_struct):
        _pack_ = 1

        _fields_ = [
            ("red",         u8),
            ("green",       u8),
            ("blue",        u8),
            ("reserved",    u8)
        ]

    _pack_ = 1
    
    _fields_ = [
        ("entry", RGB)
    ]

    def __init__(self, size: int):
        self.size = [self.RGB * size]
    
class BMPPixelData(struct):
    _pack_ = 1

    class Pixel(union):
        _pack_ = 1

        class RGB555(struct):
            _pack_ = 1
            _fields_ = [
                ("r", u16, 5),
                ("g", u16, 5),
                ("b", u16, 5)
            ]

        class RGB888(struct):
            _pack_ = 1
            _fields_ = [
                ("r", u8),
                ("g", u8),
                ("b", u8)
            ]

        def __init__(self, bitwidth: int):
            # defs
            def Pixel_1bit_get(self, bit: int) -> int:
                    if 0 > bit or bit > 8:
                        print("get_bit(): `bit` must be between 0 and 7")
                        exit(1)
                    else:
                        return (self.data >> bit) & 1

            def Pixel_4bit_get(self, nibble: int) -> int:
                if nibble != 0 and nibble != 1 :
                    print("get_nibble(): `nibble` must be either 0 or 1")
                    exit(1)
                else:
                    return self.data >> (nibble * 4)
                
            def Pixel_8bit_get(self) -> int:
                return self.data
            
            def Pixel_16bit_get(self) -> int:
                return self.data
            
            def Pixel_24bit_get(self) -> int:
                return (self.rgb.b << 16) | (self.rgb.g << 8) | self.rgb.r


            # code starts here
            if bitwidth == 1:
                setattr
                (
                    self.__class__, 
                    "_fields_", 
                    [
                        ("data", u8)
                    ]
                )
                self.data = u8(0)
                self.get = self.Pixel_1bit_get
                
            elif bitwidth == 4:
                setattr
                (
                    self.__class__,
                    "_fields_",
                    [
                        ("data", u8)
                    ]
                )
                self.data = u8(0)
                self.get = self.Pixel_4bit_get

            elif bitwidth == 8:
                setattr
                (
                    self.__class__,
                    "_fields_",
                    [
                        ("data", u8)
                    ]
                )
                self.data = u8(0)
                self.get = self.Pixel_8bit_get

            elif bitwidth == 16:
                setattr
                (
                    self.__class__,
                    "_fields_",
                    [
                        ("data", u16),
                        ("rgb", self.RGB555)
                    ]
                )
                # self.data = 0
                self.get = self.Pixel_16bit_get

            elif bitwidth == 24:
                setattr
                (
                    self.__class__,
                    "_fields_",
                    [
                        ("rgb", self.RGB888)
                    ]
                )
            else:
                print("{__name__}: bitwidth is {bitwidth}, valid values are 1, 4, 8, 16, & 24")
                exit(0)

    
    def __init__(self, bitwidth: int, num_pixels: int):
        setattr
        (
            self.__class__,
            "_fields_",
            [
                ("pixels", [self.Pixel(bitwidth)] * num_pixels)
            ]
        )


class BMPFile:
    file_header: BMPFileHeader
    info_header: BMPInfoHeader
    color_table: BMPColorTable
    pixel_data:  BMPPixelData