# https://skillapp.co/blog/10-easy-ways-to-copy-text-to-clipboard-with-python-a-comprehensive-guide/

import ctypes
def copy_to_clipboard(text):
    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    contents = ctypes.c_wchar_p(text)
    c_wchar_pointer_size = ctypes.sizeof(contents)
    text_bytesize = (len(text) + 1) * ctypes.sizeof(ctypes.c_wchar)
    text_bytesize = len(text)*2+2
    data = ctypes.windll.kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, text_bytesize)
    pcontents = ctypes.windll.kernel32.GlobalLock(data)
    ctypes.windll.kernel32.RtlMoveMemory(pcontents, contents, text_bytesize)
    ctypes.windll.kernel32.GlobalUnlock(data)
    ctypes.windll.user32.SetClipboardData(CF_UNICODETEXT, data)
    ctypes.windll.user32.CloseClipboard()
copy_to_clipboard("Hello, Python!")


def bbb():
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText("Hello, Python!")
    win32clipboard.CloseClipboard()