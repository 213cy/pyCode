import pygame as pg
from config import settings

BLOCK_LENGTH = L = settings.L
SCREENRECT = settings.SCREENRECT
XN = settings.XN
YN = settings.YN
CLIENTRECT = CR = settings.CLIENTRECT
COLOR = settings.COLOR


def window_module_constant_update():
    globals().update(vars(settings))


def window_module_constant_dump():
    tmp = {}
    ggg = globals()
    for k in vars(settings):
        tmp[k] = ggg.get(k, None)
    return tmp


# # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Window():

    @staticmethod
    def generate_background():

        # create the background, tile the bgd image
        background = pg.Surface(SCREENRECT.size)
        background.fill(COLOR['background'])
        for k in range(CR.x, CR.w+1, L):
            pg.draw.line(background, COLOR['backline'],
                            (k, CR.y), (k, CR.h), width=1)
        for k in range(CR.y, CR.h+1, L):
            pg.draw.line(background, COLOR['backline'],
                            (CR.x, k), (CR.w, k), width=1)
        
        # font = pg.font.Font(None, 16)
        font = pg.font.SysFont(settings.FontFileName, 16)

        ind = 0
        for ky in range(CR.y, CR.h, L):
            for kx in range(CR.x, CR.w, L):
                text = font.render(str(ind), False,  COLOR['backstring'])
                textpos = text.get_rect(center=(L/2, L/2))
                background.blit(text, textpos.move(kx, ky))
                ind += 1
        background = background.convert()

        return background

    def __init__(self):

        # decorate the game window
        pg.display.set_icon(pg.Surface((32, 32)))
        pg.display.set_caption("Tower Defense")
        # Set the display mode
        winstyle = 0 | pg.NOFRAME  # |pg.FULLSCREEN|pg.NOFRAME|pg.SCALED
        self.screen = pg.display.set_mode(SCREENRECT.size, winstyle)

        self.background = self.generate_background()
        self.back = self.background.copy()

    def screen_display(self):
        self.screen.blit(self.back, (0, 0))
        pg.display.flip()

    def door_update(self,  start_topleft, end_topleft ):
        tmp = self.background

        s1 = pg.Surface((L, L), pg.SRCALPHA)
        s1.fill((0, 0, 0, 0))
        a = 4
        pg.draw.lines(s1, COLOR['door'], True,
                      [(a, a), (a, L-a), (L-a, L-a), (L-a, a)], width=2)
        a = 9
        pg.draw.lines(s1, COLOR['door'], True,
                      [(a, a), (a, L-a), (L-a, L-a), (L-a, a)], width=2)
        tmp.blit(s1, start_topleft)


        s2 = pg.Surface((L, L), pg.SRCALPHA)
        s2.fill((0, 0, 0, 0))
        a = 5
        pg.draw.lines(s2, COLOR['door'], True,
                      [(L/2, a), (a, L/2), (L/2, L-a), (L-a, L/2)], width=3)
        a = 2
        pg.draw.line(s2, COLOR['door'], (a, a), (L-a, L-a), width=3)
        pg.draw.line(s2, COLOR['door'], (a, L-a), (L-a, a), width=3)
        # pg.draw.rect(s2, COLOR['door'], pg.Rect(a, a, L-a-a, L-a-a))
        tmp.blit(s2, end_topleft)

        self.back = tmp

    def road_update(self,line):
        tmp = self.background.copy()
        pg.draw.lines(tmp, 'yellow', False, line)
        self.back = tmp
