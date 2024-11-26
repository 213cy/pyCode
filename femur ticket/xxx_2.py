import win32gui
import win32api
import win32con
import time


hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', 'Send - Syntax & Usage | AutoHotkey v2 - Google Chrome')
print(hex(hwnd) )
win32gui.SetForegroundWindow(hwnd)

win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)

time.sleep(4)
key = 'v'
win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
win32api.keybd_event(ord(key), 0, 0, 0)
win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)
win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP,
                        0)

#################################

# win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN,
#                             win32con.VK_CONTROL, 1)
# win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F7, 1)
# # time.sleep(0.02)
# win32gui.PostMessage(hwnd, win32con.WM_KEYUP,  win32con.VK_F7, 0xc0000001 )
# win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL,
#                              0xc0000001 )