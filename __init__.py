from numpy import uint8 as u8
from numpy import uint16 as u16
from numpy import uint32 as u32
from numpy import uint64 as u64


class bmp_file_header:
    signature:  u16
    filesize:   u32
    reserved:   u32
    offset:     u32

class bmp_info_header:
    size:               u32
    width:              u32
    height:             u32
    planes:             u16
    bits_per_pixel:     u16
    compression:        u32
    image_size:         u32
    hori_res:           u32
    vert_res:           u32
    colors_used:        u32
    important_colors:   u32

class bmp_color_table:
    class rgb:
        red:        u8
        green:      u8
        blue:       u8
        reserved:   u8
    
    color: None
    
class bmp_pixel_data:
    pixels: None



class bmp_file: 
    file_header: bmp_file_header
    info_header: bmp_info_header
    color_table: bmp_color_table
    pixel_data: bmp_pixel_data