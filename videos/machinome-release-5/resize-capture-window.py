"""Size one Firefox window on the capture's private Xvfb display."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import ctypes
import re
import sys

display_name, window_id, width, height = sys.argv[1:]
assert re.fullmatch(r":\d+", display_name)
assert re.fullmatch(r"0x[0-9a-fA-F]+", window_id)
assert 0 < int(width) <= 7680 and 0 < int(height) <= 4320
x11 = ctypes.CDLL("libX11.so.6")
x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XMoveResizeWindow.argtypes = [ctypes.c_void_p, ctypes.c_ulong,
                                ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
x11.XRaiseWindow.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
x11.XSync.argtypes = [ctypes.c_void_p, ctypes.c_int]
x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
display = x11.XOpenDisplay(display_name.encode())
assert display, "The private capture display is unavailable"
try:
    window = int(window_id, 16)
    x11.XMoveResizeWindow(display, window, 0, 0, int(width), int(height))
    x11.XRaiseWindow(display, window)
    x11.XSync(display, 0)
finally:
    x11.XCloseDisplay(display)
