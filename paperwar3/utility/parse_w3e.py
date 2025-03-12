# from OpenGL.GL import *
from struct import unpack, iter_unpack, Struct
import numpy as np


class TileCorner:
    def __init__(self, tilepoint):

        # https://867380699.github.io/blog/2019/05/09/W3X_Files_Format#war3mapw3e
        self.ground_height = tilepoint[0]
        self.map_boundary_flag = tilepoint[1] & 0xC000 > 0
        self.water_height = tilepoint[1] & 0x3FFF
        self.camera_boundary_flag = tilepoint[2] & 0x80 > 0
        self.water_flag = tilepoint[2] & 0x40 > 0
        self.blight_flag = tilepoint[2] & 0x20 > 0
        self.ramp_flag = tilepoint[2] & 0x10 > 0
        self.tileset_type = tilepoint[2] & 0xf
        self.tile_var = tilepoint[3] & 0x1f
        self.cliff_var = tilepoint[3] >> 5
        self.cliff_type = tilepoint[4] >> 4
        self.layer_level = tilepoint[4] & 0xf

w3eFilepath="E:\Documents\pyCode\paperwar3\Assets/111.w3m/war3map.w3e"

texture_vari_record = ''
loop = ''
while loop != "q":
    with open(w3eFilepath, 'rb') as file:
        data = file.read()
    # print(len(data))

    # https://867380699.github.io/blog/2019/05/09/W3X_Files_Format#war3mapw3e
    head0 = Struct("=4sIcI")
    file_id, version, tileset_id, custom_tilesets = head0.unpack(
        data[0:head0.size])

    p = head0.size
    ground_tileset_ids_count = unpack("I", data[p:p+4])[0]
    p = p+4
    ground_tileset_ids = iter_unpack(
        "4s", data[p:p+4*ground_tileset_ids_count])
    p = p+4*ground_tileset_ids_count
    cliff_tileset_ids_count = unpack("I", data[p:p+4])[0]
    p = p+4
    cliff_tileset_ids = iter_unpack(
        "4s", data[p:p+4*cliff_tileset_ids_count])
    p = p+4*cliff_tileset_ids_count

    head_end = Struct("IIff")
    width, height, center_offset_x, center_offset_y = head_end.unpack(
        data[p:p+head_end.size])

    p = p+head_end.size
    # print(len(data[p:]))
    # corner_list_bin = data[p:]
    corner_list_raw = list(iter_unpack("HHBBB", data[p:]))
    # return list(iter_unpack("HHBBB", data[p:]))
    corner_list = [TileCorner(k) for k in corner_list_raw]

#######################################################################

    # print(texture_index)
    # print([k[3]>>5 for k in TilePoint_array])
    # a={}
    # for k in texture_vari:
    #     a.update([(k,a.get(k,0)+1)]) 
    # print(sum(a.values()))
    # # print(sorted(a.keys()))
    # # print(sorted(a.values()))
    # print(sorted(a.items()))
    # b=sorted(zip(a.values(),a.keys()))
    # print(b)
    t=16
    # c= [f"{k.tile_var:02x}" for k in corner_list[99:99+t]]
    # print(c)
    # c= [f"{k.tile_var:02x}" for k in corner_list[66:66+t]]
    # print(c)
    c= [f"{k.tileset_type:02x}" for k in corner_list[33:33+t]]
    print(c)
    c= [f"{k.tileset_type:02x}" for k in corner_list[:t]]
    print(c)


    # c= [f"{k[3]:02x}" for k in corner_list_raw[99:99+t]]
    # print(c)
    # c= [f"{k[3]:02x}" for k in corner_list_raw[66:66+t]]
    # print(c)
    c= [f"{k[3]:02x}" for k in corner_list_raw[33:33+t]]
    print(c)
    c= [f"{k[3]:02x}" for k in corner_list_raw[:t]]
    print(c)
    
    # if texture_vari_record :
    #     for k in range(len(texture_vari)):
    #         b = texture_vari[k]
    #         a = texture_vari_record[k]
    #         if a != b:
    #             print(k,a,'->',b)


    # texture_vari_record = texture_vari
    pass
    loop = input('type q to quit : ') 


def aaa():
       # ------------- final ground height ------------------
    x = [k * 128 + center_offset_x for k in range(width)]
    y = [k * 128 + center_offset_y for k in range(height)]
    # ground_height = k[0] , 0x2000 is the "ground zero"
    z1 = [(k[0] - 0x2000)/4 for k in TilePoint_array]
    # layer_level = k[4]  & 0xf , 2 is the "layer zero"
    z2 = [((k[4] & 0xf)-2)*0x80 for k in TilePoint_array]
    # ramp_flag = k[2] & 0x10 
    z3 = [0x40 if k[2] & 0x10 else 0 for k in TilePoint_array ]
    z = [a+b+c for a, b, c in zip(z1, z2, z3)]
    xx, yy = np.meshgrid(x, y)
    xyz = np.dstack((xx.ravel(), yy.ravel(), z)).ravel()

    vertices = xyz.astype(np.float32)

    # ------------- water ------------------
    water_level = [((k[1] & 0x3FFF) - 0x2000)/4 - 89.6 for k in TilePoint_array]
    water_flag = [1 if k[2] & 0x40 else 0 for k in TilePoint_array]

    # ------------- tilesets ------------------
    tileset_type = [k[2] & 0xf for k in TilePoint_array]
    texture_vari = [k[3]>>3 for k in TilePoint_array]
    texture_vari = [k[3] for k in TilePoint_array]

    cliff_type = [k[4]>>4 for k in TilePoint_array]
    cliff_vari = [k[3]& 0x7 for k in TilePoint_array]