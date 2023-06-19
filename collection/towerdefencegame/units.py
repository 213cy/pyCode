import random
import pygame as pg
from config import settings

BLOCK_LENGTH = L = settings.L
SCREENRECT = settings.SCREENRECT
XN = settings.XN
YN = settings.YN
CLIENTRECT = CR = settings.CLIENTRECT
COLOR = settings.COLOR


def units_module_constant_update():
    globals().update(vars(settings))


def units_module_constant_dump():
    tmp = {}
    ggg = globals()
    for k in vars(settings):
        tmp[k] = ggg.get(k, None)
    return tmp

# print(units_module_constant_dump())
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


class Tower(pg.sprite.Sprite):
    """Tower..."""
    defaultReloading = 12

    Len = L-2
    Rad = int(L/2-1)
    Cent = (Rad, Rad)  # proto.get_rect().center

    facecolor = COLOR['towerface']
    edgecolor = COLOR['toweredge']
    proto = pg.Surface((Len, Len), pg.SRCALPHA)
    proto.fill((0, 0, 0, 0))
    pg.draw.circle(proto, edgecolor, Cent, Rad-5)
    pg.draw.circle(proto, facecolor, Cent, Rad-8)
    cannon = pg.Surface((Len, Len), pg.SRCALPHA)
    cannon.fill((0, 0, 0, 0))
    pg.draw.line(cannon, edgecolor, (Rad+4, Rad), (Len-2, Rad), 5)


    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.reloading = self.defaultReloading
        self.facing = 90

        aaa = self.proto.copy()
        bbb = pg.transform.rotate(self.cannon, self.facing)
        aaa.blit(bbb, bbb.get_rect(center=self.Cent))
        self.image = aaa

        self.rect = self.image.get_rect(center=pos)
        self.radius = self.Rad-4

    def update(self):
        self.reloading = self.reloading - 1
        if not self.reloading:
            self.reloading = self.defaultReloading
            Shot(self)

    def set_target(self, cannonFacing):
        self.facing = cannonFacing

        aaa = self.proto.copy()
        bbb = pg.transform.rotate(self.cannon, self.facing)
        # print(aaa.get_rect(center=bbb.get_rect().center))
        aaa.blit(bbb, bbb.get_rect(center=self.Cent))
        # self.subRect.center = bbb.get_rect().center
        # bbb.subsurface(self.subRect)
        self.image = aaa


class Player(Tower):

    speed = 8
    Max_Bomb = 3

    Len = Tower.Len
    Cent = Tower.Cent
    Rad = Tower.Rad
    
    facecolor = COLOR['playerface']
    edgecolor = COLOR['playeredge']
    proto = pg.Surface((Len, Len), pg.SRCALPHA)
    proto.fill((0, 0, 0, 0))
    pg.draw.circle(proto, edgecolor, Cent, Rad-5)
    pg.draw.circle(proto, facecolor, Cent, Rad-8)
    cannon = pg.Surface((Len, Len), pg.SRCALPHA)
    cannon.fill((0, 0, 0, 0))
    pg.draw.line(cannon, edgecolor, (Rad+4, Rad), (Len-2, Rad), 5)

    def __init__(self, posIndex=157):
        posIndex = XN*YN-int(XN/2)-1
        q, r = divmod(posIndex, XN)
        super().__init__((CR.x+r*L + L/2, CR.y+q*L + L/2))

    def update(self):
        super().update()
        keystate = pg.key.get_pressed()
        cx = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
        cy = keystate[pg.K_DOWN] - keystate[pg.K_UP]
        self.rect.move_ip(cx * self.speed, cy * self.speed)
        self.rect = self.rect.clamp(SCREENRECT)

        if keystate[pg.K_SPACE]:
            Bomb(self)


class Shot(pg.sprite.Sprite):
    """a bullet the Player sprite fires...."""
    speedScale = 5
    offset = L/2
    defaultTimedLife = 30

    proto = pg.Surface((4, 1), pg.SRCALPHA)
    r,g,b,a = pg.Color( COLOR['bullet'] )
    proto.set_at((0, 0), (r, g, b, 0x66,) )
    proto.set_at((1, 0), (r, g, b, 0x99,) )
    proto.set_at((2, 0), (r, g, b, 0xCC,) )
    proto.set_at((3, 0), (r, g, b, 0xFF,) )
    #size = proto.get_size()
    #size = (size[0] * 4, size[1] * 4)
    proto = pg.transform.scale2x(proto)
    proto = pg.transform.scale2x(proto)
    #proto = pg.transform.scale(proto, size)

    def __init__(self, shooter):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.life = self.defaultTimedLife
        x, y = pg.math.Vector2(1, 0).rotate(shooter.facing)
        self.speed = (self.speedScale*x, -self.speedScale*y)

        tmp = self.proto.copy()
        # print(tmp.get_at((0,0)),tmp.get_at((4,1)),tmp.get_at((8,2)),tmp.get_at((12,3)))
        self.image = pg.transform.rotate(tmp, shooter.facing)
        self.rect = self.image.get_rect(
            center=shooter.rect.center).move(L/2*x, -L/2*y)

    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()
        else:
            self.rect.move_ip(self.speed[0], self.speed[1])


class Bomb(pg.sprite.Sprite):
    """A bomb player drop..."""
    Rad = 20
    proto = pg.Surface((2*Rad, 2*Rad))
    proto.set_colorkey(proto.get_at((0, 0)), pg.RLEACCEL)  # (0,0,0)
    pg.draw.circle(proto, COLOR['bomb'], (Rad, Rad), int(Rad/2))

    speed = 6
    bomb_sprite = None
    reloading = None

    def __new__(cls, *args, **kwargs):
        if cls.bomb_sprite is None:
            cls.bomb_sprite = super().__new__(cls)

        return cls.bomb_sprite

    def __init__(self, shooter):
        if self.reloading is None:
            pg.sprite.Sprite.__init__(self, self.containers)
        elif self.reloading > 0:
            if not self.bomb_sprite.alive():
                self.bomb_sprite.add(self.containers)
        else:
            return

        self.reloading = -20
        self.image = self.proto.copy()
        self.rect = self.image.get_rect(midbottom=shooter.rect.midtop)

    def update(self):
        if self.bomb_sprite.alive():
            self.reloading = self.reloading + 1
            if self.rect.top <= 0 and self.reloading > 0:
                self.kill()
            else:
                self.rect.move_ip(0, -self.speed)

# # # # # # # # # # # # # # # # # # # # # # # # # # # #

class AirForce(pg.sprite.Sprite):
    """An alien space ship..."""
    Len = L-2
    Rad = int(L/2-1)
    Cent = (Rad, Rad)
    Pad = 3
    High = Len - 2*Pad

    proto = pg.Surface((Len, Len), pg.SRCALPHA)
    proto.fill((0, 0, 0, 0))
    pg.draw.circle(proto, COLOR['enemyface'], Cent, Rad - Pad )

    bornBlock = None
    defaultHeathPoints = 5
    edge_color = COLOR['enemyedge_air']

    def __init__(self, color = edge_color ):
        pg.sprite.Sprite.__init__(self, self.containers)

        tmp = self.proto.copy()
        pg.draw.circle(tmp, color, self.Cent, self.Rad, self.Pad)
        self.image = tmp
        self.rect = self.image.get_rect(center=self.bornBlock.rect.center)
        self.edge_color = color

        self.radius = self.Rad

        self.lifeMarker = 0
        self.lifeMax = self.defaultHeathPoints
        self.life = self.lifeMax

        self.speed = (random.randint(-5, 5), random.randint(-5, 5))

    def update(self):
        self.rect.move_ip(self.speed[0], self.speed[1])
        if not SCREENRECT.contains(self.rect) or self.speed[0] == self.speed[1] == 0:
            self.speed = (random.randint(-5, 5), random.randint(-5, 5))
            self.rect = self.rect.clamp(SCREENRECT)

    def been_hit(self, hp=1):
        self.life = self.life - hp
        if self.life <= 0:
            Explosion(self)
            AirForce.defaultHeathPoints = AirForce.defaultHeathPoints+1
            self.kill()
        else:
            aaa = int(self.High * (self.lifeMax-self.life) / self.lifeMax)
            if aaa > self.lifeMarker + 3:
                self.lifeMarker = aaa

                tmp = self.proto.copy()
                tmp.fill((0, 0, 0, 0), pg.Rect(
                    0, 0, self.Len, self.Pad + self.lifeMarker))
                #tmp.fill((255,255,255,0) , pg.Rect(0,0 ,L, int(L-self.live*2.2)) , pg.BLEND_RGBA_MIN )
                pg.draw.circle(tmp, self.edge_color,
                               self.Cent, self.Rad, self.Pad)
                self.image = tmp


class LandForce(AirForce):
    speedScale = 5
    blockDistance = L
    edge_color = COLOR['enemyedge_land']

    def __init__(self, color = edge_color):
        super().__init__(color)

        self.fromBlock = self.bornBlock
        self.toBlock = self.bornBlock.parent[0]

        Vspeed = self.toBlock.Vpos - self.fromBlock.Vpos
        self.speed = (self.speedScale * Vspeed.x, self.speedScale * Vspeed.y)

        self.residue = self.blockDistance

    def update(self):
        self.residue = self.residue - self.speedScale
        if self.residue > 0:
            self.rect.move_ip(self.speed[0], self.speed[1])
        else:

            if len(self.toBlock.parent) > 0:

                self.fromBlock = self.toBlock
                self.toBlock = self.fromBlock.parent[0]

                Vaim = pg.Vector2(self.fromBlock.rect.center)
                Vspeed = self.toBlock.Vpos - self.fromBlock.Vpos
                Vtmp = Vaim - self.residue * Vspeed
                self.rect.center = Vtmp.xy

                self.speed = (self.speedScale * Vspeed.x,
                              self.speedScale * Vspeed.y)
                self.residue = self.residue + self.blockDistance

            else:  # 到达终点,或是被围起来没有通路了(没有通路时 parent会被清空)
                # 让其起飞,转变为一个空军单位
                self.speed = (random.randint(-5, 5), random.randint(-5, 5))
                self.edge_color = COLOR['enemyedge_air']
                self.__class__ = AirForce
                pg.draw.circle(self.image, self.edge_color,
                               self.Cent, self.Rad, self.Pad)
                # super().update
                # LandForce.update = AirForce.update
                # self.update = AirForce.update

# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# StringInfo 和 Explosion都继承自TimedHint 
# 实际上他们都只继承了TimedHint的一个属性:containers
# (继承似乎意义不大)
class TimedHint(pg.sprite.Sprite):
    """StringInfo..."""
    lifetime = 50
    Len = L-2

    def __init__(self, face_color,pos_center):
        pg.sprite.Sprite.__init__(self, self.containers)

        tmp = pg.Surface((self.Len, self.Len), pg.SRCALPHA)
        tmp.fill(face_color)

        self.image = tmp
        self.rect = self.image.get_rect(center=pos_center)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

            
class StringInfo(TimedHint):
    """StringInfo..."""
    lifetime = 150
    slotIndex = 0

    def __init__(self, message=None, pos=None):
        pg.sprite.Sprite.__init__(self, self.containers)

        # self.font = pg.font.Font(None, 26)
        self.font = pg.font.SysFont(settings.FontFileName, 24)

        if pos is None:
            self.index = self.slotIndex
            type(self).slotIndex = self.index + 1
            x, y = 50, 7+20*self.index
        else:
            self.index = -1
            x, y = pos
        self.image = self.font.render(message, True, COLOR['string'])
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            if self.index == 0:
                type(self).slotIndex = 0
            self.kill()


class Explosion(TimedHint):
    """Explosion..."""
    lifetime = 60
    statcycle = int(lifetime/10)

    proto = pg.Surface((L-1, L-1), pg.SRCALPHA)
    proto.fill((0, 0, 0, 0))

    def __init__(self, actor):
        pg.sprite.Sprite.__init__(self, self.containers)

        tmp = self.proto.copy()
        pg.draw.arc(tmp, COLOR['boom'], tmp.get_rect(), 0, 6.28, 15)
        self.image = tmp
        self.rect = self.image.get_rect(center=actor.rect.center)


    def update(self):
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()
        else:
            k = self.lifetime // self.statcycle % 9
            tmp = self.proto.copy()
            pg.draw.arc(tmp, COLOR['boom'], tmp.get_rect(), 0, k*6.28/8, 15)
            self.image = tmp

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
