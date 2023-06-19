

import win32api
import win32con
import win32gui
import _thread
import time


def desktop_name_dlgproc(hwnd, msg, wparam, lparam):
    """ Handles messages from the dialog box """
    if msg == win32con.WM_CLOSE:
        print('WM_CLOSE')
        win32gui.DestroyWindow(hwnd)

    elif msg == win32con.WM_DESTROY:
        print('WM_DESTROY')
        win32api.PostQuitMessage(0)

    elif msg == win32con.WM_COMMAND:
        if wparam == win32con.IDOK:
            Dlg_text = win32gui.GetDlgItemText(hwnd, 72)
            print(f'text content({len(Dlg_text)}): ', Dlg_text)

        elif wparam == win32con.IDCANCEL:
            win32gui.SetDlgItemText(hwnd, 72, '')


""" Create a modeless dialog box  """
msgs = {win32con.WM_COMMAND: desktop_name_dlgproc,
        win32con.WM_CLOSE: desktop_name_dlgproc,
        win32con.WM_DESTROY: desktop_name_dlgproc}
# dlg item [type, caption, id, (x,y,cx,cy), style, ex style
# |win32con.DS_SYSMODAL
style = win32con.WS_BORDER | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU
h = win32gui.CreateDialogIndirect(
    win32api.GetModuleHandle(None),
    [['One ugly dialog box !', (100, 100, 200, 100), style, 0],
        ['Button', 'get text', win32con.IDOK, (10, 10, 30, 20), win32con.WS_VISIBLE |
         win32con.WS_TABSTOP | win32con.BS_HOLLOW | win32con.BS_DEFPUSHBUTTON],
        ['Button', 'clear text area', win32con.IDCANCEL,
            (45, 10, 50, 20), win32con.WS_VISIBLE | win32con.WS_TABSTOP | win32con.BS_HOLLOW],
        ['Static', 'input some text:', 71,
            (10, 40, 70, 10), win32con.WS_VISIBLE],
        ['Edit', '', 72, (75, 40, 90, 10), win32con.WS_VISIBLE]],
    None, msgs)  # parent_hwnd, msgs)

win32gui.EnableWindow(h, True)
hcontrol = win32gui.GetDlgItem(h, 72)
win32gui.EnableWindow(hcontrol, True)
win32gui.SetFocus(hcontrol)

th = _thread.start_new_thread(win32gui.PumpMessages, ())

# win32gui.PumpMessages()

while win32gui.IsWindow(h):
    win32gui.PumpWaitingMessages()


print('done!')
time.sleep(3)
