import win32gui
import win32api
import win32con
import time
from win32clipboard import *
import winsound
from PIL import ImageGrab

code = '000099'
price = '10.00'
amount = '100'
dotype = 'sell'

PPP = {
    'buy': (100, 160),
    'sell': (100, 205),
    'code': (350, 128),
    'price': (350, 196),
    'amount': (350, 275),
    'do': (350, 370)
}


def isready(typ=None):
    # a=ImageGrab.grab()
    y0 = 300
    im = ImageGrab.grab(bbox=(350, y0, 351, y0 + 100))
    # im.show()
    imdata = list(im.getdata())
    # print(imdata)
    if typ == 'sell':
        k = (63, 151, 240)
    else:
        k = (226, 35, 36)

    assert imdata.count(k) > 16
    y = y0 + imdata.index(k)
    # y=350

    PPP.update({
        'code': (350, y - 222),
        'price': (350, y - 154),
        'amount': (350, y - 25),
        'do': (350, y + 20)
    })
    return y


def click(typ, isd=False):

    x, y = PPP[typ]
    if True:
        # handle = win32gui.WindowFromPoint(pos)
        # client_pos = win32gui.ScreenToClient(handle, (x,y))
        # tmp = win32api.MAKELONG(client_pos[0], client_pos[1])

        lParam = (y << 16) + x
        lParam = win32api.MAKELONG(x, y)
        # win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                             lParam)
    else:
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

    if isd:
        click(typ)

    # print('click')
    # time.sleep(1)


def send_key(typ):
    if typ == 'tab':
        k = win32con.VK_TAB
    elif typ == 'enter':
        k = win32con.VK_RETURN
    else:
        raise Exception
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, k, 0)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, k, 0)
    # win32api.keybd_event(k,0,0,0)
    # 发送回车


def ctrl_key(key):
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    if True:
        a = {'A': 0x1e, 'X': 0x2d, 'C': 0x2e, 'V': 0x2f}
        scancode = a[key]
        lParam = win32api.MAKELONG(1, scancode)
        # key=key.upper()
        c = win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN,
                                 win32con.VK_CONTROL, 0x1d0001)
        c = win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, ord(key), lParam)
        # time.sleep(0.02)
        c = win32gui.PostMessage(hwnd, win32con.WM_KEYUP, ord(key),
                                 hex(lParam + 0xc0000000))
        c = win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL,
                                 0xc01d0001)

    else:
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(ord(key), 0, 0, 0)
        win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP,
                             0)
    # print(f'contrl + {key}' )
    time.sleep(1)


def setform(context):

    OpenClipboard()
    EmptyClipboard()
    CloseClipboard()

    ctrl_key('A')
    ctrl_key('X')

    OpenClipboard()
    if IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
        got = GetClipboardData(win32con.CF_UNICODETEXT)
    else:
        got = None
    SetClipboardData(win32con.CF_UNICODETEXT, context)
    CloseClipboard()

    ctrl_key('V')

    return got


################################################

hwnd = win32gui.FindWindow('Notepad', None)
# b=win32gui.SetForegroundWindow(hwnd)
#    hwnd = win32gui.FindWindow("Notepad", None)
#    i=win32gui.IsIconic(hwnd)  #检查窗口是否最小化
hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '广发操盘手')

###########################################
# win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  #最大化指定的窗口。nCmdShow=3
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  #最小化指定的窗口。nCmdShow=6
# win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  #激活,恢复并显示窗口。nCmdShow=9
# win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)  #
# win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)  #激活窗口并将其最大化。nCmdShow=3
# a=win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

h = win32gui.GetForegroundWindow()
win32gui.SetForegroundWindow(hwnd)
# win32gui.BringWindowToTop(hwnd)
# win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
# win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
h2 = win32gui.GetForegroundWindow()
print(hwnd, h, h2)

#########################################

click(dotype)

time.sleep(3)
print(isready(dotype))

###################################

click('code')
time.sleep(1)
got = setform(code)
print(got)

# click('price')
send_key('tab')
got = setform(price)
print(got)

send_key('tab')
got = setform(amount)
print(got)

##########################################################

# send_key('enter')
# c=win32gui.SendMessage(hwnd, win32con.WM_CHAR, 0x16, 0x2f0001)
