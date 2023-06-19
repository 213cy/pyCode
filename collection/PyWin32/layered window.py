
from win32api import *
# Try and use XP features, so we get alpha-blending etc.
try:
    from winxpgui import *
except ImportError:
    from win32gui import *
from win32gui_struct import *
import win32con
import sys
import os


class MainWindow:
    def __init__(self):
        this_dir = os.path.split(sys.argv[0])[0]
        load_bmp_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE 
        # | win32con.LR_CREATEDIBSECTION
        self.hBitmap_DH = LoadImage(0, os.path.join(this_dir, "demonhunter.bmp"),
                                    win32con.IMAGE_BITMAP, 0, 0, load_bmp_flags)
        self.hBitmap_BM = LoadImage(0, os.path.join(this_dir, "blademaster.bmp"),
                                    win32con.IMAGE_BITMAP, 0, 0, load_bmp_flags)
        self.Image_info = GetObject(self.hBitmap_DH)
        self.Image_x = self.Image_info.bmWidth
        self.Image_y = self.Image_info.bmHeight

########################

        # Register the Window class.
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_RBUTTONDOWN: self.OnRButtonDown,
            win32con.WM_LBUTTONDOWN: self.OnLButtonDown,
            win32con.WM_PAINT: self.OnPaint,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "XXXXXXXXXXXXXX"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        # 指定cursor 不然鼠标会转圈
        wc.hCursor = LoadCursor(0, win32con.IDC_ARROW)
        # wc.hbrBackground = win32con.COLOR_WINDOW
        wc.hbrBackground = CreateSolidBrush(RGB(255, 255, 255)).Detach()
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW  
        #| win32con.WS_EX_TRANSPARENT # win32con.WS_OVERLAPPED
        exstyle = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED
        self.hwnd = CreateWindowEx(exstyle, wc.lpszClassName, "Hero Profile", style,
                                   0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                   0, 0, hinst, None)

        self.WlStyle = GetWindowLong(self.hwnd, win32con.GWL_STYLE)
        self.WlExStyle = GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)

        # SetLayeredWindowAttributes(self.hwnd, 0, 175, win32con.LWA_ALPHA)
        SetLayeredWindowAttributes(self.hwnd, RGB(255, 255, 255),
                                   0, win32con.LWA_COLORKEY)

        hDC = GetDC(self.hwnd)
        self.hdcMem = CreateCompatibleDC(hDC)
        ReleaseDC(self.hwnd, hDC)

        # DeleteDC(self.hdcMem)
        # DeleteObject(self.hBitmap)

        ShowWindow(self.hwnd, win32con.SW_NORMAL)
        # UpdateWindow(self.hwnd)
        print("Please click on the hero's head")

###############################################################################
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        print("Destroy.")
        PostQuitMessage(0)  # Terminate the app.

    def OnRButtonDown(self, hwnd, msg, wparam, lparam):
        print("You clicked right button.")
        print('x:',LOWORD(lparam),'  y:', HIWORD(lparam) )
        
        addStyle = ~win32con.WS_CAPTION
        SetWindowLong(hwnd, win32con.GWL_STYLE, self.WlStyle & addStyle)
        # SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        #              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)
        ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

        # print(hex(self.WlExStyle))
        # print(hex(GetWindowLong(self.hwnd,win32con.GWL_EXSTYLE)))

        InvalidateRect(self.hwnd, None, True)
        # UpdateWindow(self.hwnd)

        
    def OnLButtonDown(self, hwnd, msg, wparam, lparam):
        print("You clicked left button.")
        print('x:',LOWORD(lparam),'  y:', HIWORD(lparam) )
        
        SetWindowLong(hwnd, win32con.GWL_STYLE, self.WlStyle)
        SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 700, 500,
                      win32con.SWP_FRAMECHANGED) #win32con.SWP_NOMOVE | win32con.SWP_NOSIZE |
        # ShowWindow(self.hwnd, win32con.SW_SHOWDEFAULT)
        ShowWindow(self.hwnd, win32con.SW_RESTORE)

        InvalidateRect(self.hwnd, None, True)
        # UpdateWindow(self.hwnd)

    def OnPaint(self, hwnd, msg, wparam, lparam):
        # BringWindowToTop(hwnd)
        # SetForegroundWindow(hwnd)
        print('OnPaint')
        (left, top, right, bottom) = GetClientRect(self.hwnd)
        pad = 20
        hDC, ps = BeginPaint(hwnd)

        ####################################
        SelectObject(self.hdcMem, self.hBitmap_DH)
        BitBlt(hDC, pad, pad, self.Image_x, self.Image_y,
               self.hdcMem, 0, 0, win32con.SRCCOPY)

        SelectObject(self.hdcMem, self.hBitmap_BM)
        BitBlt(hDC, right-self.Image_x-pad, pad, self.Image_x, self.Image_y,
               self.hdcMem, 0, 0, win32con.SRCCOPY)
        
        ####################################

        # text and background colors to display text.
        crText = SetTextColor(hDC, RGB(107, 151, 100))
        crBkgnd = SetBkColor(hDC, GetSysColor(win32con.COLOR_HIGHLIGHT))
        crBkgnd = SetBkColor(hDC, RGB(243, 212, 119))
        # SetBkMode(hDC, win32con.TRANSPARENT)

        # # Select the font, draw it, and restore the previous font.
        # ft = GetStockObject(win32con.OEM_FIXED_FONT)
        lf = LOGFONT()
        lf.lfHeight=30
        lf.lfWidth=15
        ft = CreateFontIndirect( lf )
        oldFont = SelectObject(hDC, ft)
        text = "right or left click the hero's head"
        ExtTextOut(hDC, pad, self.Image_y+pad+pad,
                   win32con.ETO_OPAQUE, None, text)
        SelectObject(hDC, oldFont)
        DeleteObject(ft)
        # Return the text and background colors to their
        # normal state
        SetTextColor(hDC, crText)
        SetBkColor(hDC, crBkgnd)
        ####################################
        
        EndPaint(hwnd, ps)


def main():
    w = MainWindow()
    PumpMessages()


if __name__ == '__main__':
    main()
