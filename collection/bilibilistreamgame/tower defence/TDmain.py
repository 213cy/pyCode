
from win32api import *
# Try and use XP features, so we get alpha-blending etc.
try:
    from winxpgui import *
except ImportError:
    from win32gui import *
from win32gui_struct import *
import win32con

import threading
import time
import sys
# from danmu_client import danmu_send_test as danmu_send
from danmu_client import danmu_send as danmu_send

COL = 30
ROW = 19
StartCMD = 'cmd@rp3'
RequestList_Lock = threading.Lock()
RequestList = []


class CommandEntry():

    @staticmethod
    def min_and_diff(a, b):
        if a > b:
            return b, min(a+1-b, 9)
        else:
            return a, min(b+1-a, 9)

    def __init__(self, p1, p2, tail):
        x1, y1 = p1
        x2, y2 = p2
        # -----------------------------------
        if (x1 == x2) ^ (y1 == y2):
            if x1 == x2:
                self.x = x1
                self.y, self.len = self.min_and_diff(y1, y2)
                self.mid = 'y'+str(self.len)
            else:  # y1 == y2:
                self.y = y1
                self.x, self.len = self.min_and_diff(x1, x2)
                self.mid = 'x'+str(self.len)
        else:
            self.x = x1
            self.y = y1
            self.len = 0
            self.mid = ''
        # -----------------------------------
        self.ind = COL*self.y + self.x + 1
        self.danmu = str(self.ind) + self.mid + tail
        # -----------------------------------
        self.note = ''
        self.Stime = 0

        # print(f'{self.danmu: <8}  ---   {x1,y1},{x2,y2}')

class loopMNG():
    PreviousAndNext = ((2,1),(0,2),(1,0))
    def __init__(self):
        self.CmdList = [None, None, None]
        self.IndList = [0, 0, 0]
        self.WaitList = [4.0, 4.0, 4.0]
        self.Entries = 0

        self.p = 0

    def append(self, cmd: CommandEntry):
        # print(cmd.ind,self.IndList,cmd.ind in self.IndList)
        if cmd.ind in self.IndList:
            self.WaitList = [3.5, 3.5, 3.5]
            self.WaitList[self.IndList.index(cmd.ind)] = 4.5
        elif self.Entries == 3:
            self.__init__()
            # cmd.Stime = 0
            self.CmdList[self.Entries] = cmd
            self.IndList[self.Entries] = cmd.ind
            self.Entries = self.Entries + 1
        else:
            # cmd.Stime = -50*self.Entries
            self.CmdList[self.Entries] = cmd
            self.IndList[self.Entries] = cmd.ind
            self.Entries = self.Entries + 1

    def reset(self):
        self.__init__()

########################


class APP:
    def create_output_window(self):
        # Register the Window class.
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_LBUTTONDOWN: self.OnWinPlaceChange,
            win32con.WM_PAINT: self.OnPaint,
        }
        #####################################
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "XXXXXXXXXXXXXX"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        # 指定cursor 不然鼠标会转圈
        wc.hCursor = LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = CreateSolidBrush(RGB(255, 255, 255)).Detach()
        # wc.hbrBackground = win32con.COLOR_WINDOW + 1
        classAtom = RegisterClass(wc)
        #####################################
        # Create the Window.
        exstyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED
        style = win32con.WS_OVERLAPPEDWINDOW
        # | win32con.WS_OVERLAPPED | win32con.WS_VISIBLE
        hwnd = CreateWindowEx(exstyle, wc.lpszClassName, "Output", style,
                              0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                              0, 0, hinst, None)
        SetLayeredWindowAttributes(hwnd, RGB(255, 255, 255),
                                   0, win32con.LWA_COLORKEY)

        ShowWindow(hwnd, win32con.SW_NORMAL)

        return hwnd

    def create_input_window(self):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_RBUTTONDOWN: self.OnRButtonDown,
            win32con.WM_LBUTTONDOWN: self.OnLButtonDown,
            win32con.WM_KEYDOWN: self.OnKeyDown, }
        #####################################
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "YYYYYYYYYY"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        # 指定cursor 不然鼠标会转圈
        wc.hCursor = LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = CreateSolidBrush(RGB(155, 255, 155)).Detach()
        #wc.hbrBackground = CreateSolidBrush(RGB(33,64,108)).Detach()
        # wc.hbrBackground = win32con.COLOR_WINDOW + 1
        classAtom = RegisterClass(wc)
        #####################################
        # # Create the Window.
        exstyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED
        style = win32con.WS_POPUPWINDOW  # | win32con.WS_POPUP
        hwnd = CreateWindowEx(exstyle, classAtom, "Input", style,
                              0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                              None, 0, hinst, None)
        SetLayeredWindowAttributes(hwnd, 0, 15, win32con.LWA_ALPHA)

        # ShowWindow(hwnd, win32con.SW_NORMAL)

        return hwnd

    def __init__(self):

        self.hwnd_in = self.create_input_window()
        self.hwnd_out = self.create_output_window()
        self.WlStyle = GetWindowLong(self.hwnd_out, win32con.GWL_STYLE)
        #####################################

        lf = LOGFONT()
        lf.lfHeight = 30
        lf.lfWidth = 15
        # ft = GetStockObject(win32con.OEM_FIXED_FONT)
        self.Ft = CreateFontIndirect(lf)

        # self.Brush = CreateSolidBrush(RGB(0, 0, 0))
        self.Brush = GetStockObject(win32con.NULL_BRUSH)
        self.Pen = CreatePen(win32con.PS_SOLID, 2, RGB(255, 0, 0))
        self.Pen2 = CreatePen(win32con.PS_SOLID, 2, RGB(0, 255, 0))
        # DeleteObject(hPen)
        # DeleteObject(hbrush)

        #####################################

        self.TowerType = 2
        self.AddTailFlag = True
        self.ResidentTime = 6.0
        self.isDispalyInfo = False
        self.PrePoint = [-1, -1]
        self.MapRect = [12, 39, 1142-12+1, 755-39+1]
        # a = ROW//3
        # b = ROW-a
        # h = b*38+a*39
        # t = 35
        # a = COL//3
        # b = COL - a
        # w = b*38 + a * 39
        # l = 21
        # self.MapRect = [l, t, w+2, h+2]
        self.LoopManager = loopMNG()

    ###########################################################################

    def OnPaint(self, hwnd, msg, wparam, lparam):
        # BringWindowToTop(hwnd)
        # SetForegroundWindow(hwnd)
        # print('OnPaint')

        hDC, ps = BeginPaint(hwnd)

        ####################################
        ####################################
        hPenOld = SelectObject(hDC, self.Pen)
        hbrushOld = SelectObject(hDC, self.Brush)

        l, t, w, h = self.MapRect
        pad = 5

        for k in RequestList:
            if len(k.mid) == 0:
                x = l+round(k.x * w/COL)+pad+3
                y = t+round(k.y * h/ROW)+pad+3
                xl = l+round((k.x+1) * w/COL)-pad-1
                yl = t+round((k.y+1) * h/ROW)-pad-1
            elif k.mid[0] == 'x':
                x = l+round(k.x * w/COL)+pad
                y = t+round(k.y * h/ROW)+pad
                xl = l+round((k.x+k.len) * w/COL)-pad+2
                yl = t+round((k.y+1) * h/ROW)-pad+2
            elif k.mid[0] == 'y':
                x = l+round(k.x * w/COL)+pad
                y = t+round(k.y * h/ROW)+pad
                xl = l+round((k.x+1) * w/COL)-pad+2
                yl = t+round((k.y+k.len) * h/ROW)-pad+2
            else:
                print('error!')

            if k.Stime == 0:
                SelectObject(hDC, self.Pen2)
            else:
                SelectObject(hDC, self.Pen)

            Rectangle(hDC, x, y, xl, yl)

        SelectObject(hDC, hPenOld)
        SelectObject(hDC, hbrushOld)

        ####################################

        # text and background colors to display text.
        crText = SetTextColor(hDC, RGB(107, 151, 100))
        # crBkgnd = SetBkColor(hDC, GetSysColor(win32con.COLOR_HIGHLIGHT))
        crBkgnd = SetBkColor(hDC, RGB(243, 212, 119))
        # SetBkMode(hDC, win32con.TRANSPARENT)
        oldFont = SelectObject(hDC, self.Ft)

        ''' cmds : O,C,up,down,0-9'''
        if IsWindowVisible(self.hwnd_in):
            ExtTextOut(hDC, 20, 10, win32con.ETO_OPAQUE, None,
                       "<maximize> |  normal  ")
        else:
            ExtTextOut(hDC, 20, 10, win32con.ETO_OPAQUE, None,
                       " maximize  | <normal> ")

        if self.isDispalyInfo:
            k = 130
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       f'tower type:<{self.TowerType}>')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       f'danmu nums:<{len(RequestList)}>')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       f'delay time:<{self.ResidentTime}>')
            k = k + 30
            key, alpha, flags = GetLayeredWindowAttributes(self.hwnd_in)
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       f'window alpha:<{alpha}>')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       f'loop entries:<{self.LoopManager.Entries}>')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                    f'loop index:{self.LoopManager.IndList}')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                    f'loop time:{self.LoopManager.WaitList}')
            k = k + 30
            ExtTextOut(hDC, 500, k, win32con.ETO_OPAQUE, None,
                       'cmds:<H,O,C,R,up,down,left,right,0-9>')

        for k in range(len(RequestList)):
            ExtTextOut(hDC, 1110, 10+30+30*k, win32con.ETO_OPAQUE, None,
                       RequestList[k].danmu + RequestList[k].note)

        SelectObject(hDC, oldFont)
        SetTextColor(hDC, crText)
        SetBkColor(hDC, crBkgnd)

        ####################################
        ####################################

        EndPaint(hwnd, ps)

    def OnWinPlaceChange(self, hwnd, msg, wparam, lparam):
        # print(wparam, win32con.MK_SHIFT)
        if wparam & win32con.MK_SHIFT:
            l, t, r, b = win32gui.GetClientRect(hwnd)
            l, t = ClientToScreen(hwnd, (0, 0))
            r, b = ClientToScreen(hwnd, (r, b))
            self.MapRect = [l, t, r-l+1, b-t+1]

        x, y = LOWORD(lparam), HIWORD(lparam)
        # print(f'output window clicked at ({x},{y})')
        if x < 340 and y < 46:
            Style = GetWindowLong(hwnd, win32con.GWL_STYLE)
            if Style == self.WlStyle:
                SetWindowLong(hwnd, win32con.GWL_STYLE,
                              self.WlStyle ^ win32con.WS_CAPTION)
                ShowWindow(hwnd, win32con.SW_MAXIMIZE)

                l, t, w, h = self.MapRect
                SetWindowPos(self.hwnd_in, win32con.HWND_TOPMOST, l, t, w, h,
                             win32con.SWP_FRAMECHANGED)
                ShowWindow(self.hwnd_in, win32con.SW_NORMAL)
            else:
                SetWindowLong(hwnd, win32con.GWL_STYLE, self.WlStyle)
                SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 700, 500,
                             win32con.SWP_FRAMECHANGED)
                # win32con.SWP_NOMOVE | win32con.SWP_NOSIZE |

                ShowWindow(self.hwnd_in, win32con.SW_HIDE)

            InvalidateRect(hwnd, None, True)
            # UpdateWindow(self.hwnd)
        else:
            print('list size: ', sys.getsizeof(RequestList),
                  '---', RequestList.__sizeof__())
            # print(GetWindowPlacement(hwnd))

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        DestroyWindow(self.hwnd_in)
        # DestroyWindow(self.hwnd_out)
        PostQuitMessage(0)  # Terminate the message loop.

    ###########################################################################

    def OnRButtonDown(self, hwnd, msg, wparam, lparam):
        x, y = LOWORD(lparam), HIWORD(lparam)
        l, t, w, h = self.MapRect
        xx, yy = int(x/w*COL), int(y/h*ROW)
        self.PrePoint = [xx, yy]
        # print(f'clicked right button at ({x},{y}) [{xx},{yy}].')
        # print(wparam, win32con.MK_SHIFT)
        if wparam & win32con.MK_SHIFT:
            cmd = CommandEntry(self.PrePoint, [-1, -1], '')
            self.LoopManager.append(cmd)

    def OnLButtonDown(self, hwnd, msg, wparam, lparam):
        x, y = LOWORD(lparam), HIWORD(lparam)
        l, t, w, h = self.MapRect
        xx, yy = int(x/w*COL), int(y/h*ROW)
        Point = [xx, yy]
        # print(f'clicked left button at ({x},{y}) [{xx},{yy}].')

        tail = ''
        if self.AddTailFlag:
            tail = ' '+str(self.TowerType)
            self.AddTailFlag = False

        cmd = CommandEntry(Point, self.PrePoint, tail)
        if all(map(lambda x: x.danmu != cmd.danmu, RequestList)):
            RequestList_Lock.acquire()
            RequestList.append(cmd)
            RequestList_Lock.release()

        else:
            print('already added to queue!')

        self.PrePoint = [-1, -1]

        InvalidateRect(self.hwnd_out, None, True)
        # UpdateWindow(hwnd)

    def OnKeyDown(self, hwnd, msg, wparam, lparam):
        if lparam >> 30 : # keyup
            return

        print(f'vk={wparam}={chr(wparam)} ')
              

        if wparam == ord('C'):
            RequestList.clear()
        elif wparam == ord('R'):
            self.LoopManager.reset()
        elif wparam == ord('H'):
            self.isDispalyInfo = ~self.isDispalyInfo

        elif wparam == ord('O'):
            s = danmu_send(StartCMD)
            print(f'start! <{s}>')
            print( 5*'-', time.asctime() ,5*'-')
            time.sleep(2)
            for k in range(1,5,2):
                RequestList.append(CommandEntry([k, k-1], [k+8, k-1], ' 2'))
                RequestList.append(CommandEntry([COL-k-1, k-1], [COL-k-9, k-1], ''))
                RequestList.append(CommandEntry([k, ROW-k], [k+8, ROW-k], ''))
                RequestList.append(CommandEntry([COL-k-1, ROW-k], [COL-k-9, ROW-k], ''))

                RequestList.append(CommandEntry([k-1, k], [k-1, k+8], ''))
                RequestList.append(CommandEntry([COL-k, k], [COL-k, k+8], ''))


            # RequestList.append(CommandEntry([2, 1], [10, 1], ' 2'))
            # RequestList.append(CommandEntry([COL-11, 1], [COL, 1], ' 2'))
            # RequestList.append(CommandEntry([4, 3], [12, 3], ''))
            # RequestList.append(CommandEntry([COL-13, 3], [COL, 3], ''))
            for k in range(4,15,2):
                RequestList.append(CommandEntry([5, k], [COL, k], ''))
                RequestList.append(CommandEntry([15, k], [COL, k], ''))

            # RequestList.append(CommandEntry([4, 14], [12, 14], ''))
            # RequestList.append(CommandEntry([COL-13, 14], [COL, 14], ''))
            # RequestList.append(CommandEntry([2, 16], [10, 16], ''))
            # RequestList.append(CommandEntry([COL-11, 16], [COL, 16], ''))

            # RequestList.append(CommandEntry([1, 2], [1, 13], ''))
            # RequestList.append(CommandEntry([3, 4], [3, 13], ''))
            # RequestList.append(CommandEntry([COL-4, 4], [COL-4, 13], ''))
            # RequestList.append(CommandEntry([COL-2, 2], [COL-2, 13], ''))

        elif wparam == win32con.VK_DOWN:  # ==40
            key, alpha, flags = GetLayeredWindowAttributes(hwnd)
            alpha = max(1, alpha - 10)
            SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)
        elif wparam == win32con.VK_UP:  # ==38
            key, alpha, flags = GetLayeredWindowAttributes(hwnd)
            alpha = min(255, alpha + 10)
            SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)

        elif wparam == win32con.VK_LEFT:  # ==
            self.ResidentTime = max(4, self.ResidentTime - 0.5)
        elif wparam == win32con.VK_RIGHT:  # ==
            self.ResidentTime = min(9, self.ResidentTime + 0.5)

        else:
            a = wparam - ord('0')
            b = wparam - win32con.VK_NUMPAD0
            if -1 < a < 10:
                self.TowerType = a
                self.AddTailFlag = True
            elif -1 < b < 10:
                self.TowerType = a
                self.AddTailFlag = True
            else:
                print(f'vk={ord("0")}=0   vk={win32con.VK_NUMPAD0}=pad0')


        InvalidateRect(self.hwnd_out, None, True)

###################################################


def send_request(RequestList, app :APP):
    while IsWindow(app.hwnd_out):

        t = time.time()
        if len(RequestList) > 0:
            if app.ResidentTime < t - RequestList[0].Stime < 99:
                RequestList.pop(0)
                if len(RequestList) > 0:
                    if app.ResidentTime < t - RequestList[0].Stime < 99:
                        RequestList.pop(0)

        IsSent = False
        if app.LoopManager.Entries == 3:
            lm = app.LoopManager
            c = lm.p
            p,n = lm.PreviousAndNext[c]
            cmd = lm.CmdList[c]
            if t - lm.CmdList[p].Stime > lm.WaitList[p] :
                IsSent = True
                scode = danmu_send(cmd.danmu)
                if scode == 200:
                    lm.p=n
                    cmd.Stime = time.time()
                    # print(cmd.ind, cmd.Stime)
                    dummy = CommandEntry([cmd.x,cmd.y], [-1, -1], '')
                    dummy.Stime = cmd.Stime
                    dummy.note = ' ==='
                    index = -1
                    for k,v in enumerate(RequestList):
                        if v.Stime == 0:
                            index = k
                            break
                    if index == -1:
                        RequestList_Lock.acquire()
                        RequestList.append(dummy)
                        RequestList_Lock.release()
                    else:
                        RequestList_Lock.acquire()
                        RequestList.insert(index,dummy)
                        RequestList_Lock.release()
                else :
                    print('insert send failed ! ')

        if not IsSent:
            for cmd in RequestList:
                if cmd.Stime == 0:
                    scode = danmu_send(cmd.danmu)
                    if scode == 200:
                        cmd.Stime = time.time()
                        cmd.note = ' >200'
                    elif cmd in RequestList: 
                    # ensure cmd is in the list,for asynchronous command 'c'
                        RequestList.remove(cmd)
                        RequestList_Lock.acquire()
                        RequestList.append(cmd)
                        RequestList_Lock.release()
                        cmd.note = f' >{scode}'
                    break

        InvalidateRect(app.hwnd_out, None, True)

        time.sleep(1.4)


############################################################
# if __name__ == '__main__':
MouseDanmu = APP()

thread = threading.Thread(target=send_request,
                          args=(RequestList, MouseDanmu))
thread.start()

PumpMessages()

# thread2 = threading.Thread(target=PumpMessages)
# thread2.start()
