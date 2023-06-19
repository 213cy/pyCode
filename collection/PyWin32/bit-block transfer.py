
# Try and use XP features, so we get alpha-blending etc.
try:
    from winxpgui import *
except ImportError:
    from win32gui import *
import win32con
import sys
import os


class MainWindow:
    def __init__(self):
        this_dir = os.path.split(sys.argv[0])[0]
        load_bmp_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        # | win32con.LR_CREATEDIBSECTION
#######################

        self.hBitmap_hum = LoadImage(0, os.path.join(this_dir, "human.bmp"),
                                     win32con.IMAGE_BITMAP, 0, 0, load_bmp_flags)
        self.hBitmap_mask = LoadImage(0, os.path.join(this_dir, "mask.bmp"),
                                      win32con.IMAGE_BITMAP, 0, 0, load_bmp_flags)
        Image_info = GetObject(self.hBitmap_hum)
        self.cx = Image_info.bmWidth
        self.cy = Image_info.bmHeight
        self.hBitmap_desk = CreateBitmap(self.cx, self.cy, Image_info.bmPlanes,
                                         Image_info.bmBitsPixel, None)

#######################
        self.hBitmap_DH = LoadImage(0, os.path.join(this_dir, "demonhunter.bmp"),
                                    win32con.IMAGE_BITMAP, 0, 0, load_bmp_flags)

        Image_info = GetObject(self.hBitmap_DH)
        self.cx_DH = Image_info.bmWidth
        self.cy_DH = Image_info.bmHeight
        hbm_DH = CreateBitmap(self.cx_DH, self.cy_DH, Image_info.bmPlanes,
                              Image_info.bmBitsPixel, None)


#######################

        hwnd_desk = GetDesktopWindow()
        (left, top, right, bottom) = GetWindowRect(hwnd_desk)
        self.x0 = int(right/2)
        self.y0 = int(bottom/2)

        self.hdcScreen = GetDC(hwnd_desk)
        self.hdcMem = CreateCompatibleDC(self.hdcScreen)
        # SetBkMode(self.hdcMem, win32con.TRANSPARENT)
        SetStretchBltMode(self.hdcMem, win32con.COLORONCOLOR)
        # SetStretchBltMode(self.hdcMem, win32con.HALFTONE)
        # self.hBitmap_desk = CreateCompatibleBitmap(self.hdcMem, self.cx, self.cy)
        hbmOld = SelectObject(self.hdcMem, self.hBitmap_desk)

        self.isDrawSmallIcon = True
        self.hdcMem_DH = CreateCompatibleDC(self.hdcScreen)
        hbmOld = SelectObject(self.hdcMem_DH, self.hBitmap_DH)
        
        self.hdcMem_src = CreateCompatibleDC(self.hdcScreen)

        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcScreen, self.x0, self.y0, win32con.SRCCOPY)
        hbmOld_src = SelectObject(self.hdcMem_src, self.hBitmap_mask)
        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcMem_src, 0, 0, win32con.SRCAND)
        SelectObject(self.hdcMem_src, self.hBitmap_hum)
        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcMem_src, 0, 0, win32con.SRCPAINT)
        StretchBlt(self.hdcMem, 50, 50, 30, 30,
                self.hdcMem_DH, 0, 0, self.cx_DH, self.cy_DH,
                win32con.SRCCOPY)

        DeleteObject(hbmOld)
        DeleteObject(hbmOld_src)
        # SelectObject(self.hdcMem, hbmOld)
        # ReleaseDC(hwnd_desk, self.hdcScreen)
        # DeleteDC(self.hdcMem)
#####################################################################
        # Register the Window class.
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_MOUSEMOVE: self.OnMouseMove,
            win32con.WM_MOVE: self.OnMove,
            win32con.WM_LBUTTONDOWN: self.OnLButtonDown,
            win32con.WM_RBUTTONDOWN: self.OnRButtonDown,
            win32con.WM_PAINT: self.OnPaint,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "XXXXXXXXXXXXXXXXX"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        # 指定cursor 不然鼠标会转圈
        wc.hCursor = LoadCursor(0, win32con.IDC_ARROW)
        # wc.hbrBackground = win32con.COLOR_WINDOW
        # wc.hbrBackground = CreateSolidBrush(RGB(255, 255, 255)).Detach()
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_OVERLAPPEDWINDOW
        style = win32con.WS_POPUP
        self.hwnd = CreateWindow(wc.lpszClassName, "bit-block transfer demo", style,
                                 self.x0, self.y0, self.cx, self.cy,
                                 0, 0, hinst, None)

        ShowWindow(self.hwnd, win32con.SW_NORMAL)
        # UpdateWindow(self.hwnd)
        print("Please drag or left click the seal")

###############################################################################
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        print("Destroy.")
        PostQuitMessage(0)  # Terminate the app.

    def OnRButtonDown(self, hwnd, msg, wparam, lparam):
        # print('RRRRRRR')
        self.isDrawSmallIcon = not self.isDrawSmallIcon
        InvalidateRect(self.hwnd, None, True)


    def OnLButtonDown(self, hwnd, msg, wparam, lparam):
        # self.ox = LOWORD(lparam)
        # self.oy = HIWORD(lparam)
        (self.left, self.top, self.right, self.bottom) = GetWindowRect(hwnd)
        self.ox, self.oy = GetCursorPos()

    def OnMouseMove(self, hwnd, msg, wparam, lparam):
        # print(wparam,lparam)
        if wparam == win32con.MK_LBUTTON:
            # x,y = LOWORD(lparam),HIWORD(lparam)
            x, y = GetCursorPos()
            self.x0, self.y0 = self.left - self.ox + x, self.top - self.oy + y

            # MoveWindow(hwnd, self.left - self.ox + x,
            #            self.top - self.oy + y,
            #            self.cx, self.cy, True)
            SetWindowPos(hwnd, win32con.HWND_TOP, self.x0, self.y0, 0, 0,
                         win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)  # win32con.SWP_NOMOVE |

    def OnMove(self, hwnd, msg, wparam, lparam):


        InvalidateRect(self.hwnd, None, True)
        # UpdateWindow(self.hwnd)

    def OnPaint(self, hwnd, msg, wparam, lparam):
        # BringWindowToTop(hwnd)
        # SetForegroundWindow(hwnd)
        print('OnPaint')

        hDC, ps = BeginPaint(hwnd)

        ####################################        
        # ShowWindow(hwnd, win32con.SW_HIDE)
        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcScreen, self.x0, self.y0, win32con.SRCCOPY)
        # ShowWindow(hwnd, win32con.SW_NORMAL)
        SelectObject(self.hdcMem_src, self.hBitmap_mask)
        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcMem_src, 0, 0, win32con.SRCAND)
        SelectObject(self.hdcMem_src, self.hBitmap_hum)
        BitBlt(self.hdcMem, 0, 0, self.cx, self.cy,
               self.hdcMem_src, 0, 0, win32con.SRCPAINT)
        if self.isDrawSmallIcon:
            StretchBlt(self.hdcMem, 50, 50, 30, 30,
                       self.hdcMem_DH, 0, 0, self.cx_DH, self.cy_DH,
                       win32con.SRCCOPY)

        BitBlt(hDC, 0, 0, self.cx, self.cy,
               self.hdcMem, 0, 0, win32con.SRCCOPY)

        ####################################

        EndPaint(hwnd, ps)


def main():
    w = MainWindow()
    PumpMessages()


if __name__ == '__main__':
    main()
