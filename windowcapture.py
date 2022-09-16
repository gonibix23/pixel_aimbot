import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    xPosIn = 0
    yPosIn = 0
    hwnd = None

    def __init__(self, window_name = None, width = 0, height = 0, xPosIni = 0, yPosIni = 0):

        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
            #win32gui.MoveWindow(self.hwnd, -(xPosIni), -(yPosIni), width, height, True)
            self.w = width
            self.h = height
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window not found: {}".format(window_name))
            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.w = window_rect[2]
            self.h = window_rect[3]
        
        border_pixels = 0
        titlebar_pixels = 0
        
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.xPosIn = xPosIni
        self.yPosIn = yPosIni

        self.offset_x = xPosIni + self.cropped_x
        self.offset_y = yPosIni + self.cropped_y

    def get_screenshot(self):

        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.xPosIn, self.yPosIn), win32con.SRCCOPY)
        #Guarda la captura
        #dataBitMap.SaveBitmapFile(cDC, "debug.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype="uint8")
        img.shape = (self.h, self.w, 4)

        #Libera la memoria
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def list_window_names():
            def winEnumHandler(hwnd, ctx):
                if win32gui.IsWindowVisible(hwnd):
                    print(hex(hwnd), win32gui.GetWindowText(hwnd))
            win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
            return (pos[0] + self.offset_x, pos[1] + self.offset_y)