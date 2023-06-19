# Demonstrates creating a taskbar icon

import win32api
import win32con
import win32gui
import traceback
import _thread
import time

############################################
PumpFlag = True


def icon_wndproc(hwnd, msg, wp, lp):
    """ Window proc for the tray icons """
    global PumpFlag
    if lp == win32con.WM_LBUTTONDOWN:
        print('WM_USER+20 :',msg,win32con.WM_USER+20)
        # popup menu won't disappear if you don't do this
        win32gui.SetForegroundWindow(hwnd)

        m = win32gui.CreatePopupMenu()
        # *don't* create an item 0
        win32gui.AppendMenu(m, win32con.MF_STRING |
                            win32con.MF_CHECKED, 1, 'CHECKED')
        win32gui.AppendMenu(m, win32con.MF_STRING |
                            win32con.MF_GRAYED, 2, 'GRAYED')
        win32gui.AppendMenu(m, win32con.MF_STRING |
                            win32con.MF_DISABLED, 3, 'DISABLED')
        win32gui.AppendMenu(m, win32con.MF_STRING, 4, 'Create new ...')
        win32gui.AppendMenu(m, win32con.MF_STRING, 5, 'Exit')

        x, y = win32gui.GetCursorPos()
        d = win32gui.TrackPopupMenu(m, win32con.TPM_LEFTBUTTON | win32con.TPM_RETURNCMD | win32con.TPM_NONOTIFY,
                                    x, y, 0, hwnd, None)
        print('selected', d)
        win32gui.PumpWaitingMessages()
        win32gui.DestroyMenu(m)

        if d == 1:
            print('Check Menu 1')
        elif d == 2:
            print('Check Menu 2')
        elif d == 3:
            print('Check Menu 3')
        elif d == 4:
            print('Check Create new')
        elif d == 5:
            win32gui.PostQuitMessage(0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, notify_info)
            PumpFlag = False
        return 0
    else:
        return win32gui.DefWindowProc(hwnd, msg, wp, lp)

############################################


hinst = win32api.GetModuleHandle(None)
windowclassname = 'PywinTrayIconClass'

wc = win32gui.WNDCLASS()
wc.hInstance = hinst
wc.lpszClassName = windowclassname
wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW | win32con.CS_GLOBALCLASS
wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
wc.hbrBackground = win32con.COLOR_WINDOW+1
wc.lpfnWndProc = icon_wndproc
windowclass = win32gui.RegisterClass(wc)

style = win32con.WS_SYSMENU
style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
hwnd = win32gui.CreateWindow(windowclass, 'StatusAreaTrayIcon', style,
                             0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                             0, 0, wc.hInstance, None)
win32gui.UpdateWindow(hwnd)

hicon = win32gui.LoadIcon(hinst, 1)
hicon = win32gui.LoadIcon(None, win32con.IDI_APPLICATION)
flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
notify_info = (hwnd, 1, flags, win32con.WM_USER+20,
               hicon, 'A tooltip text for tray icon')

##
tray_found = 0
while not tray_found:
    try:
        # "Shell_TrayWnd" is class of system tray window
        tray_found = win32gui.FindWindow("Shell_TrayWnd", None)
    except win32gui.error:
        traceback.print_exc
        time.sleep(.5)

# Sends an 'adds icon' message to the taskbar's status area.
win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, notify_info)

# win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)

# th=_thread.start_new_thread(win32gui.PumpMessages,())
win32gui.PumpMessages()
# while PumpFlag:
#     win32gui.PumpWaitingMessages()

# time.sleep(3)

print(PumpFlag)
