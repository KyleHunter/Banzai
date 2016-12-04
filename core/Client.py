import win32gui
from PIL import ImageGrab
import cv2
import numpy as np
import time


class Client:

    parent_handle, child_handle, bounds = None, None, None
    __child_handles = []

    def child_callback(self, hwnd, param):
        self.__child_handles.append(hwnd)

    def __init__(self):
        self.parent_handle = win32gui.FindWindow(None, "Old School RuneScape")
        win32gui.EnumChildWindows(self.parent_handle, self.child_callback, None)
        if self.parent_handle == 0:
            raise Exception("Unable to find RuneScape client")
        for i in self.__child_handles:
            rect = win32gui.GetWindowRect(i)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            if (width == 765) and (height == 503):
                self.child_handle = i
                self.bounds = rect

    def get_canvas(self, bounds=(0, 0, 765, 503)):
        s = bounds
        rect = win32gui.GetWindowRect(self.child_handle)
        rect = [rect[0] + s[0], rect[1] + s[1], rect[0] + s[2], rect[1] + s[3]]
        self.bounds = rect
        img = ImageGrab.grab(bbox=self.bounds)
        img_np = np.array(img)
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)


class RsClient:

    _active, _created, _img = False, False, None

    def __init__(self):
        self._active, self._created = True, time.time()
        self._update_img()

    def _update_img(self):
        self._active, self._created = True, time.time()
        self._img = Client().get_canvas()

    def _update(self):
        if time.time() - self._created > 0.1:
            self._update_img()

    def get_img(self):
        self._update()
        return self._img

rs = RsClient()

