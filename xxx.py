import win32gui
import win32api
import win32con
import time


# df = pd.read_csv(fileA,sep='\t',header=1,encoding='gb2312')

# temp=df.columns
# t=[datetime.strptime(k,'%m/%d/%Y') for k in df[temp[0]]]
# print( b'\xc8\xd5\xc6\xda'.decode('gb2312').encode('gb2312') )

hwnd = win32gui.FindWindow('Chrome_WidgetWin_1','广发操盘手')
x,y=100,200
win32api.SetCursorPos([x, y])
win32api.mouse_event( win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
time.sleep(0.1)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP , x, y, 0, 0)
time.sleep(5)
raise SystemExit

hwnd = win32gui.FindWindow('Notepad',None)
##a=win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32cno.SC_MAXIMIZE, 0)
a=win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)

win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500,
                             win32con.SWP_FRAMECHANGED)

x,y=100,200
lParam = (y<<16)+x
win32gui.SendMessage(hwnd, win32con.WM_PARENTNOTIFY, win32con.WM_LBUTTONDOWN, lParam)
time.sleep(5)
