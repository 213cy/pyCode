
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
        Image_info = GetObject(self.hBitmap_DH)
        self.Image_x = Image_info.bmWidth
        self.Image_y = Image_info.bmHeight
        self.HeroRank = 0

        # Register the Window class.
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_RBUTTONDOWN: self.OnMouseClick,
            win32con.WM_PAINT: self.OnPaint,
        }
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "ImageCarrier"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        wc.hCursor = LoadCursor(0, win32con.IDC_ARROW)
        # wc.hbrBackground = win32con.COLOR_WINDOW+1
        classAtom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_CHILD  # WS_CLIPCHILDREN
        style = win32con.WS_OVERLAPPED  # win32con.WS_OVERLAPPEDWINDOW
        style = win32con.WS_POPUP  # | win32con.WS_POPUP

        self.hParent = 0
        self.hwnd = CreateWindow(wc.lpszClassName, "Hero Profile", style,
                                 200, 200, self.Image_x * 3, self.Image_y * 3,
                                 self.hParent, 0, hinst, None)


        self.InitDrawIcon()
        self.InitStretchIcon()
        self.createMenu()

        hDC = GetDC(self.hwnd)
        self.hdcMem = CreateCompatibleDC(hDC)
        ReleaseDC(self.hwnd, hDC)
        # DeleteDC(self.hdcMem)
        # DeleteObject(self.hBitmap_DH)
        SelectObject(self.hdcMem, self.hBitmap_BM)

        ShowWindow(self.hwnd, win32con.SW_NORMAL)
        # UpdateWindow(self.hwnd)
        print("Please right-click on the window")

    def InitDrawIcon(self):
        ico_x = GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = LoadIcon(0, win32con.IDI_EXCLAMATION)

        # Add icon by converting via bitmap.
        hdcScreen = GetDC(self.hwnd)
        hdcMem = CreateCompatibleDC(hdcScreen)
        SetBkMode(hdcMem, win32con.TRANSPARENT)
        self.hbm_1 = CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        self.hbm_2 = CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        ReleaseDC(self.hwnd, hdcScreen)

        hbmOld = SelectObject(hdcMem, self.hbm_1)
        # Fill the background.
        # brush = GetSysColorBrush(win32con.COLOR_MENU)
        brush = CreateSolidBrush(RGB(150, 200, 0))
        FillRect(hdcMem, (0, 0, 12, 22), brush)
        # draw the icon
        DrawIconEx(hdcMem, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)

        SelectObject(hdcMem, self.hbm_2)
        # Fill the background.
        brush = GetSysColorBrush(win32con.COLOR_MENU)
        # brush = CreateSolidBrush(RGB(150,200,0))
        FillRect(hdcMem, (12, 0, 22, 22), brush)
        # draw the icon
        DrawIconEx(hdcMem, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)

        DestroyIcon(hicon)
        DeleteObject(brush)
        SelectObject(hdcMem, hbmOld)
        DeleteDC(hdcMem)

        self.ico_draw_1 = self.hbm_1.Detach()
        self.ico_draw_2 = self.hbm_2.Detach()

    def InitStretchIcon(self):
        ico_x = GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = GetSystemMetrics(win32con.SM_CYSMICON)

        # Add icon by converting via bitmap.
        hdcScreen = GetDC(self.hwnd)
        hdcMem = CreateCompatibleDC(hdcScreen)
        # SetStretchBltMode(hdcMem, win32con.COLORONCOLOR)
        SetStretchBltMode(hdcMem, win32con.HALFTONE)
        hdcMem_src = CreateCompatibleDC(hdcScreen)
        ReleaseDC(self.hwnd, hdcScreen)

        Image_info = GetObject(self.hBitmap_DH)
        x, y = Image_info.bmWidth, Image_info.bmHeight
        self.hbm_DH = CreateBitmap(ico_x, ico_y, Image_info.bmPlanes,
                              Image_info.bmBitsPixel, None)
        self.hbm_BM = CreateBitmap(ico_x, ico_y, Image_info.bmPlanes,
                              Image_info.bmBitsPixel, None)

        hbmOld_src = SelectObject(hdcMem_src, self.hBitmap_DH)
        hbmOld = SelectObject(hdcMem, self.hbm_DH)
        StretchBlt(hdcMem, 0, 0, ico_x, ico_y,
                   hdcMem_src, 0, 0, x, y,
                   win32con.SRCCOPY)

        SelectObject(hdcMem_src, self.hBitmap_BM)
        SelectObject(hdcMem, self.hbm_BM)
        StretchBlt(hdcMem, 0, 0, ico_x, ico_y,
                   hdcMem_src, 0, 0, x, y,
                   win32con.SRCCOPY)

        # SelectObject(self.hdcMem, self.hBitmap_BM)

        SelectObject(hdcMem, hbmOld)
        DeleteDC(hdcMem)
        SelectObject(hdcMem_src, hbmOld_src)
        DeleteDC(hdcMem_src)

        # self.icon_DH = self.hbm_DH.Detach()
        # self.icon_BM = self.hbm_BM.Detach()

    def createMenu(self):
        self.hmenu = menu = CreatePopupMenu()

        InsertMenu(menu, -1, win32con.MF_BYPOSITION,
                   win32con.MF_SEPARATOR, None)

        item, extras = PackMENUITEMINFO(text='(id:1001)parent=cmd',
                                hbmpItem=self.ico_draw_1,
                                wID=1001)
        InsertMenuItem(menu, 0, 1, item)

        item, extras = PackMENUITEMINFO(text='(id:1002)parent=notepad',
                                        hbmpItem=self.ico_draw_2,
                                        wID=1002)
        InsertMenuItem(menu, 0, 1, item)

        # Create our 'Exit' item with the standard, ugly 'close' icon.
        wID = 1000
        AppendMenu(menu, win32con.MF_STRING, wID, 'Exit xxxx')
        item, extras = PackMENUITEMINFO(hbmpItem=win32con.HBMMENU_MBAR_CLOSE)
        SetMenuItemInfo(menu, wID, False, item)
        # default option text use bold fonts.
        SetMenuDefaultItem(menu, wID, 0)


########################

        # Create a sub-menu, and put a few funky ones there.
        self.sub_menu = sub_menu = CreatePopupMenu()

        # Create a top-level menu with a bitmap
        item, extras = PackMENUITEMINFO(text="(id:1010)Demonhunter",
                                        hbmpItem=self.hbm_DH.Detach(),
                                        wID=1010)
        InsertMenuItem(sub_menu, 0, 1, item)

        item, extras = PackMENUITEMINFO(text="(id:1011)Blademaster",
                                        hbmpItem=self.hbm_BM.Detach(),
                                        wID=1011)
        InsertMenuItem(sub_menu, 0, 1, item)

        # And add the sub-menu to the top-level menu.
        item, extras = PackMENUITEMINFO(text="Sub-Menu",
                                        hSubMenu=sub_menu)
        InsertMenuItem(menu, 0, 1, item)

###############################################################################

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        print("Destroy.")
        PostQuitMessage(0)  # Terminate the app.

    def OnMouseClick(self, hwnd, msg, wparam, lparam):
        print("You right clicked me.")
        # display the menu at the cursor pos.
        pos = GetCursorPos()
        # SetForegroundWindow(self.hwnd)
        TrackPopupMenu(self.hmenu, win32con.TPM_LEFTALIGN,
                       pos[0], pos[1], 0, self.hwnd, None)
        # PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = LOWORD(wparam)

        buf, extras = EmptyMENUITEMINFO()
        GetMenuItemInfo(self.hmenu, id, False, buf)
        fType, fState, wID, hSubMenu, hbmpChecked, hbmpUnchecked, \
            dwItemData, text, hbmpItem = UnpackMENUITEMINFO(buf)
        print("activated menu item :", text)

        if id == 1000:
            print("Goodbye")
            DestroyWindow(self.hwnd)
        elif id == 1001:
            Cmd = FindWindow('ConsoleWindowClass',
                             'Administrator: C:\Windows\system32\cmd.exe')
            if Cmd:
                self.hParent = Cmd
                (left, top, right, bottom) = GetClientRect(self.hParent)
                # SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST,
                #     right - self.Image_x * 3, bottom - self.Image_x * 3, 100, 100,
                #     win32con.SWP_NOSIZE) #win32con.SWP_NOMOVE |
                SetParent(self.hwnd, Cmd)
                MoveWindow(self.hwnd, right - self.Image_x * 3,
                           bottom - self.Image_x * 3, 100, 100, True)
            else:
                print('not found cmd window')

        elif id == 1002:
            Notepad = FindWindow('Notepad', None)
            edit = FindWindowEx(Notepad, None, 'Edit', None)
            if Notepad:
                self.hParent = Notepad
                (left, top, right, bottom) = GetClientRect(self.hParent)
                MoveWindow(edit, 0, 0, int(right/2-50), bottom, True)
                SetParent(self.hwnd, self.hParent)
                SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST,
                             right - self.Image_x * 3, bottom - self.Image_x * 3, 0, 0,
                             win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED)  # win32con.SWP_NOMOVE |

            else:
                print('not found notepad window')
        elif id == 1010:
            self.HeroRank += 1
            SelectObject(self.hdcMem, self.hBitmap_DH)
            InvalidateRect(self.hwnd, None, True)
            # UpdateWindow(self.hwnd)
        elif id == 1011:
            self.HeroRank += 1
            SelectObject(self.hdcMem, self.hBitmap_BM)
            InvalidateRect(self.hwnd, None, True)
            # UpdateWindow(self.hwnd)
        else:
            print("OnCommand for ID", id)

    def OnPaint(self, hwnd, msg, wparam, lparam):
        # SetForegroundWindow(self.hwnd)
        # BringWindowToTop(hwnd)
        print('OnPaint')

        hDC, ps = BeginPaint(hwnd)

        BitBlt(hDC, 0, 0, self.Image_x, self.Image_y,
               self.hdcMem, 0, 0, win32con.SRCCOPY)

####################################

        # text and background colors to display text.
        crText = SetTextColor(hDC, RGB(255, 0, 0))
        crBkgnd = SetBkColor(hDC, GetSysColor(win32con.COLOR_HIGHLIGHT))
        # SetBkMode(hDC, win32con.TRANSPARENT)

        # # Select the font, draw it, and restore the previous font.
        # ft = GetStockObject(win32con.OEM_FIXED_FONT)
        # oldFont = SelectObject(hDC, ft)
        ExtTextOut(hDC, 46, 44, win32con.ETO_OPAQUE, None, str(self.HeroRank))
        # SelectObject(hDC, oldFont)

        # Return the text and background colors to their normal state
        # SetTextColor(hDC, crText)
        # SetBkColor(hDC, crBkgnd)

        EndPaint(hwnd, ps)


def main():
    w = MainWindow()
    PumpMessages()


if __name__ == '__main__':
    main()
