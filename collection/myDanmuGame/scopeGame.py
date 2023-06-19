import win32gui
import time
import math
import asyncio

class ScopeGame():
    # hwin = win32gui.FindWindow('TkTopLevel',None)
    # hwin = win32gui.FindWindow('Notepad',None)
    # hwin =win32gui.GetForegroundWindow()
    hwin = win32gui.GetDesktopWindow()

    # print(hex(hwin))
    # print('window title: ', win32gui.GetWindowText(hwin))
    # print('set window title: ', win32gui.SetWindowText(hwin, 'aaab'))

    # hdc = win32gui.GetDC(hwin)
    hdc = win32gui.GetDC(None)
    hp = win32gui.CreatePen(0, 4, int('00ff00', 16))
    PS_SOLID = 0
    hpen = win32gui.CreatePen(PS_SOLID, 1, int('0000ff', 16))
    BLACK_BRUSH = 4
    hbrush = win32gui.GetStockObject(BLACK_BRUSH)
    hpen_Old = win32gui.SelectObject(hdc, hpen)
    hbrush_Old = win32gui.SelectObject(hdc, hbrush)
    

    def __init__(self, ControlSet={'dx': 0.0011, 'dy': 0.002}):
        self.zx = 0
        self.zy = 0
        self.loopFlag = True
        self.CS = ControlSet
        self.segmentCount = 20
        self.segmentLength = 16
        self.lineX = [ self.segmentLength*[500] for k in range(self.segmentCount)]
        self.lineY = [ self.segmentLength*[300] for k in range(self.segmentCount)]

    async def gameARun(self):
        a = 0
        cls = ScopeGame
        mod = self.segmentCount
        while self.loopFlag:
            for k in range(self.segmentLength):
                self.lineX[a][k] = round(
                    200*math.cos(self.zx+k*self.CS['dx']) + 300)
                self.lineY[a][k] = round(
                    200*math.sin(self.zy+k*self.CS['dy']) + 300)
            self.zx += (k+1)*self.CS['dx']
            self.zy += (k+1)*self.CS['dy']
            a = (a+1) % mod

            win32gui.SelectObject(cls.hdc, cls.hpen)
            win32gui.Rectangle(cls.hdc, 90, 90, 510, 510)

            b = (a+1) % mod
            win32gui.MoveToEx(cls.hdc, self.lineX[b][0], self.lineY[b][0])

            win32gui.SelectObject(cls.hdc, cls.hp)
            for k in range(mod-1):
                for x, y in zip(self.lineX[(b+k) % mod], self.lineY[(b+k) % mod]):
                    win32gui.LineTo(cls.hdc, x, y)

            # WM_PAINT = 0x0F
            # WM_NCPAINT = 0x85
            # WM_SYNCPAINT = 0x88
            # WM_ERASEBKGND = 0x14
            # win32gui.SendMessage(0, WM_PAINT, 0, 0)
            # win32gui.SendMessage(hwin, WM_PAINT, 0, 0)

            await asyncio.sleep(0.02)
            # time.sleep(0.02)
        self.releaseResource()
        print('game done!')

    def gameRun(self):
        asyncio.run( self.gameARun() )

    def stopLoop(self):
        self.loopFlag = False

    @classmethod
    def releaseResource(cls):
        win32gui.SelectObject(cls.hdc, cls.hpen_Old)
        win32gui.SelectObject(cls.hdc, cls.hbrush_Old)

        win32gui.DeleteObject(cls.hp)
        win32gui.DeleteObject(cls.hpen)
        win32gui.DeleteObject(cls.hbrush)
        # win32gui.ReleaseDC(cls.hwin, cls.hdc)
        # win32gui.DeleteDC(cls.hdc)


if __name__ == '__main__':
    g = ScopeGame()
    g.gameRun()
