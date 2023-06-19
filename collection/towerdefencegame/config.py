import pygame as pg
import random
# import units
# import window
# import route


BLOCK_LENGTH = L = 38
w, h = (640, 480)

SCREENRECT = pg.Rect(0, 0, w, h)
XN = w//L - 1
YN = h//L - 1
xx = int((w-XN*L)/2)
yy = int((h-YN*L)/2)
ww = xx+XN*L
hh = yy+YN*L
CLIENTRECT = CR = pg.Rect(xx, yy, ww, hh)

COLOR = {'bullet': '#FFFF33',
         'bomb': '#AAEE33',
         'boom': '#FF9933',
         'enemyface': '#FF6666',
         'enemyedge_air': '#0099CC',
         'enemyedge_land': 'antiquewhite2',
         'towerface': '#66DD33',
         'playerface': '#66DD33',
         'toweredge': '#CCAA88',
         'playeredge': '#CCAA88',
         'backline': 'khaki3',
         'background': '#332211',
         'backstring': 'khaki1',
         'string': '#DDEEFF',
         'door': 'dodgerblue3'
         }

# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# dict(zip(COLOR.keys(),( pg.Color(k) for k in COLOR.values())))
for k, v in COLOR.items():
    COLOR[k] = pg.Color(v)


h = list(range(random.randint(-10, 10), 360, 30))
if h[0] < 0:
    h[0] = h[-1]
s = [30, 40, 50, 65, 85, 95]
v = [25, 40, 60, 85, 95, 100]
a = 100

COLOR['boom'].hsva = (h[1], s[-1], v[-1], a)

COLOR['enemyface'].hsva = (h[0], s[3], v[-2], a)
COLOR['towerface'].hsva = (h[3], s[3], v[-2], a)
COLOR['playerface'].hsva = (h[4], s[3], v[-2], a)

COLOR['enemyedge_land'].hsva = (h[1], s[-2], v[-3], a)
COLOR['enemyedge_air'].hsva = (h[7], s[-2], v[-3], a)
COLOR['toweredge'].hsva = (h[10], s[-2], v[-3], a)
COLOR['playeredge'].hsva = (h[11], s[-2], v[-3], a)

COLOR['bullet'].hsva = (h[2], s[-2], v[-2], a)
COLOR['bomb'].hsva = (h[3], s[-2], v[-2], a)

COLOR['string'].hsva = (h[5], s[1], v[-3], a)
COLOR['door'].hsva = (h[6], s[1], v[-3], a)

COLOR['backline'].hsva = (h[9], s[0], v[2], a)
COLOR['backstring'].hsva = (h[11], s[0], v[3], a)
COLOR['background'].hsva = (h[8], s[2], v[1], a)


# # # # # # # # # # # # # # # # # # # # # # # # # # # #


class globalvars():
    def __init__(self):
        self.BLOCK_LENGTH = L
        self.L = L
        self.SCREENRECT = SCREENRECT
        self.XN = XN
        self.YN = YN
        self.CLIENTRECT = CR
        self.CR = CR
        self.COLOR = COLOR
        self.enable = False
        self.FontFileName = 'verdana.ttf'
# self.ConstDict = {
#     'BLOCK_LENGTH': L,
#     'L': L,
#     'SCREENRECT': SCREENRECT,
#     'XN': XN,
#     'YN': YN,
#     'CLIENTRECT':  CR,
#     'CR': CR,
#     'COLOR': COLOR
#     'enable' : True
# }

    def update(self, block_len, wh):

        L = block_len
        w, h = wh

        self.BLOCK_LENGTH = self.L = L
        self.SCREENRECT = pg.Rect(0, 0, w, h)
        self.XN = (w-10)//L - 1
        self.YN = (h-10)//L - 1
        xx = int((w-self.XN*L)/2)
        yy = int((h-self.YN*L)/2)
        ww = xx+self.XN*L
        hh = yy+self.YN*L
        self.CLIENTRECT = self.CR = pg.Rect(xx, yy, ww, hh)

    def update_all_module_constant(self):
        # units.units_module_constant_update()
        # route.route_module_constant_update()
        # window.window_module_constant_update()
        ...

 # # # # # # # # # # # # # # # # # # # # # # # # # # # #


settings = globalvars()

# pg.display.list_modes()
# [(1680, 1050), (1600, 900), (1440, 900), (1400, 1050), (1366, 768),
#  (1360, 768), (1280, 1024), (1280, 960), (1280, 800), (1280, 768),
#  (1280, 720), (1280, 600), (1152, 864), (1024, 768), (800, 600),
#  (640, 480), (640, 400), (512, 384), (400, 300), (320, 240), (320, 200)]

# settings.update(40,(800, 600))

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #




#   #for debug:
# print(vars(settings))

# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# try:
#     # from matplotlib.colors import hsv_to_rgb
#     # print( matplotlib.colors.hsv_to_rgb((0.1, 0.1, 0.1)) )

#     from  PIL.ImageColor import getrgb
#     # ImageColor.getrgb("rgb(100%,0%,0%)")
#     # ImageColor.getrgb("hsv(0,100%,100%)")
#     # ImageColor.getrgb("hsl(0,100%,50%)")
#     # >>> (255, 0, 0)

#     h = list(range(random.randint(-10,10),360,30))
#     if h[0]<0:
#         h[0] = 360+h[0]
#     s = [20,35,50,65,80,70]
#     v = [20,35,50,65,80,100]
#     hsv = lambda h,s,v : getrgb(f"hsv({h},{s}%,{v}%)")
#     COLOR['boom'] = hsv(h[1],s[-1],v[-1])

#     COLOR['enemyface'] = hsv(h[0],s[-2],v[-2])
#     COLOR['towerface'] = hsv(h[4],s[-2],v[-2])
#     COLOR['playerface'] = hsv(h[8],s[-2],v[-2])

#     COLOR['enemyedge_land'] = hsv(h[1],s[2],v[-3])
#     COLOR['playeredge'] = hsv(h[4],s[2],v[-3])
#     COLOR['enemyedge_air'] = hsv(h[7],s[2],v[-3])
#     COLOR['toweredge'] = hsv(h[10],s[2],v[-3])

#     COLOR['bullet'] = hsv(h[2],s[-3],v[-2])
#     COLOR['bomb'] = hsv(h[3],s[-3],v[-2])

#     COLOR['string'] = hsv(h[5],s[1],v[-3])
#     COLOR['door'] = hsv(h[6],s[1],v[-3])

#     COLOR['backline'] = hsv(h[9],s[0],v[2])
#     COLOR['backstring'] = hsv(h[8],s[0],v[2])
#     COLOR['background'] = hsv(h[11],s[0],v[1])

# except Exception as e:
#     print("Without additional initialization for colors. ",f"(due to : {e})")
