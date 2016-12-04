import win32api
import win32con
import win32gui
import misc.Misc as Misc
import time


def left_click():
    _, _, (x, y) = win32gui.GetCursorInfo()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    Misc.sleep(20, 50)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def right_click():
    _, _, (x, y) = win32gui.GetCursorInfo()
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    Misc.sleep(20, 50)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def move(x=None, y=None, box=None, click_left=False, click_right=False, box_offset = 0):
    if box is not None:
        x, y = Misc.rand_box(box=box, offset=box_offset)
    xn, yn = Misc.get_local_coords(x, y)
    win32api.SetCursorPos((xn, yn))
    if click_left:
        time.sleep(Misc.random_range(30, 100) / 1000)
        left_click()
    if click_right:
        time.sleep(Misc.random_range(30, 100) / 1000)
        right_click()

