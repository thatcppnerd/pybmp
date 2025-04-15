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



class BMPVersion(Enum):
    BITMAPCOREHEADER = 0
    BITMAPINFOHEADER = 1
    BITMAPV2INFOHEADER = 2
    BITMAPV3INFOHEADER = 3
    BITMAPV4INFOHEADER = 4
    BITMAPV5INFOHEADER = 5


'''
Translates the size of a .bmp file's info header to its version.
'''
def BMPGetVersionFromSize(size: int) -> BMPVersion:
    xlat_vals = (12, 40, 52, 56, 108, 124)

    for i in range(0, 6):
        if size == xlat_vals[i]:
            return BMPVersion(i)
        
    print("{__name__}: Size does not correlate to any known version.")
    exit(1)


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

    def __init__(self, version: int):
        v = self.BMPVersion

        fields = [
                    ("size", u32),
                ]

        if version >= v.BITMAPCOREHEADER.value: 
            fields += ("width",     u16)
            fields += ("height",    u16)
            fields += ("planes",    u16)
            fields += ("bpp",       u16)

        if version >= v.BITMAPINFOHEADER.value:
            # redefine stuff from version 1
            fields[1] = ("width",   u32)
            fields[2] = ("height",  u32)

            fields += ("compression",       u32)
            fields += ("image_size",        u32)
            fields += ("x_ppm",             u32)
            fields += ("y_ppm",             u32)
            fields += ("colors_used",       u32)
            fields += ("important_colors",  u32)

        if version >= v.BITMAPV2INFOHEADER.value:
            fields += ("red_mask",      u32)
            fields += ("green_mask",    u32)
            fields += ("blue_mask",     u32)

        if version >= v.BITMAPV3INFOHEADER.value:
            fields += ("alpha_mask",    u32)

        if version >= v.BITMAPV4INFOHEADER.value:
            fields += ("cs_type",       u32)
            fields += ("cs_endpoints",  [u32] * 9)
            fields += ("red_gamma",     u32)
            fields += ("green_gamma",   u32)
            fields += ("blue_gamma",    u32)

        if version == v.BITMAPV5INFOHEADER.value:
            fields += ("intent",            u32)
            fields += ("profile_offset",    u32)
            fields += ("profile_size",      u32)
            fields += ("reserved",          u32)

        setattr(
            self.__class__,
            "_fields_",
            fields
        )

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

    def __init__(self, num_entries: int):
        self.size = [self.RGB * num_entries]
    
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
    '''
    The constructor can only initialize the file header and the info header.
    
    This is because the format of the color table and the pixel data is determined by the parameters
    set in the info header.

    To initialize both, firstly fill the info header with the needed parameters, then run `init_CT` 
    FIRST to set up the color table, THEN run `init_PD` to initialize the pixel data. 
    '''
    def __init__(self, version: int):
        self.file_header = BMPFileHeader
        self.info_header = BMPInfoHeader(version)
        self.color_table: BMPColorTable
        self.pixel_data = BMPPixelData

    '''
    Initializes the color table based on the parameters set in `info_header`.
    '''
    def init_CT(self):
        if self.info_header.compression == BMPInfoHeader.CompressionValue.BI_RGB:
            self.color_table = BMPColorTable(self.info_header)
        
    
    '''
    Initializes the pixel data based on the parameters set in `info_header`.
    '''
    def init_PD():
        pass

