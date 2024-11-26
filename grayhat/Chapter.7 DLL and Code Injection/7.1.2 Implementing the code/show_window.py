import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

# Define the EnumWindows callback function type
EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

# Define the EnumWindows function signature
EnumWindows = user32.EnumWindows
# EnumWindows.argtypes = [EnumWindowsProc, wintypes.LPARAM]
# EnumWindows.restype = ctypes.c_bool


def get_window_handles_by_pid(window_pid):
    # List to store window handles
    window_handles = []

    # Define a callback function to be called for each window
    def foreach_window(hwnd, lParam):

        length = user32.GetWindowTextLengthW(hwnd) + 1
        buf = ctypes.create_unicode_buffer(length)
        user32.GetWindowTextW(hwnd, buf, length)

        # Get the process ID that owns the window
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        if pid.value == lParam:
            print(f"Window title: {buf.value}, Process ID: {pid.value}")
            # If the process ID matches the one we're looking for, add the window handle to the list
            window_handles.append(hwnd)
            return False
        else:
            return True  # Continue enumeration

    # Call EnumWindows with the callback function
    EnumWindows(EnumWindowsProc(foreach_window), window_pid)

    return window_handles


process_pid = 0xfbc
window_handles = get_window_handles_by_pid(process_pid)
hwindow = window_handles[0]

print(f"={hwindow}======={type(hwindow)}======")
fl = user32.IsWindowVisible(hwindow)
print(f"IsWindowVisible = {fl}")

GWL_STYLE = -16
WS_VISIBLE = 0x10000000
bVisible = user32.GetWindowLongA(hwindow, GWL_STYLE) & WS_VISIBLE
print(f"{bVisible:x}")


# SW_HIDE = 0
# user32.ShowWindow(hwindow, SW_HIDE)

SW_SHOW = 5
user32.ShowWindow(hwindow, SW_SHOW)
