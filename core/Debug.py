from core.Client import *
import core.Globals as Globals
from operator import methodcaller
import misc.Misc as Misc
import core.Inventory as Inventory
from PIL import Image

class Debug:

    loc, exit, clicked = None, None, None

    def callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_RBUTTON:
            self.exit = True
        if event == cv2.EVENT_FLAG_LBUTTON:
            self.clicked = True
            self.loc = x, y

    def __init__(self):
        pass

    def general(self):
        bgr = Client().get_canvas()
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        cv2.imshow("image", hsv)
        cv2.setMouseCallback("image", self.callback)
        while True:
            bgr = Client().get_canvas()
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            cv2.imshow("image", bgr)
            cv2.waitKey(500)
            if self.clicked:
                print("Mouse Coords ->", self.loc, "HSV Color ->", hsv[self.loc[1], self.loc[0]])
                self.clicked = False
            if self.exit:
                cv2.destroyAllWindows()
                break

    def test(self):
            bgr = Client().get_canvas()
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            for i in range(0, 28):
                print(Inventory.item_size(i))

    def new(self):
        import win32gui
        import win32ui
        import win32con
        hwnd = Client().child_handle
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 761, 499)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(761, 499) , dcObj, (0,0), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(cDC, "test.png")

        Image.open(dataBitMap)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


