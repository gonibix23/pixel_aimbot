import cv2 as cv
import numpy as np
from time import time
from PIL import ImageGrab
from windowcapture import WindowCapture
from pynput.keyboard import Key, Controller
from vision import Vision
import tkinter
import win32api, win32gui, win32con
import pyautogui

keyboard = Controller()

#WindowCapture.list_window_names()

cascade_enemies = cv.CascadeClassifier("cascade/cascade.xml")
#vision_enemies = Vision()

def startWatching():
    cv.setUseOptimized(True)
    toggle = 1
    loop_time = time()
    #wincap = WindowCapture(None, int(2*(win32api.GetSystemMetrics(0)/10)), int(2*(win32api.GetSystemMetrics(1)/10)), int(4*(win32api.GetSystemMetrics(0)/10)), int(4*(win32api.GetSystemMetrics(1)/10)))
    wincap = WindowCapture("Counter-Strike: Global Offensive - Direct3D 9")
    while(True):
        xPos, yPos = pyautogui.position()
        if toggle:
            screenshot = wincap.get_screenshot()
            rectangles = cascade_enemies.detectMultiScale(screenshot)
            #detection_image = vision_enemies.draw_rectangles(screenshot, rectangles)
            for rect in rectangles:
                xPos, yPos = pyautogui.position()
                xObj = int(rect[0]+(rect[2]/2))
                yObj = int(rect[1]+(rect[3]/2))
                xCoe = (xObj-xPos)/100
                yCoe = (yObj-yPos)/100
                sensibilidad = 4.0
                mov = 20*sensibilidad
                if(xObj>3*win32api.GetSystemMetrics(0)/10 and yObj>3*win32api.GetSystemMetrics(1)/10 and xObj<7*win32api.GetSystemMetrics(0)/10 and yObj<7*win32api.GetSystemMetrics(1)/10):
                    #print("Inicial: x="+str(xPos)+", y="+str(yPos) + " Objetivo: x="+str(xObj)+", y="+str(yObj) + " Coeficiente: x="+str(xCoe)+", y="+str(yCoe))
                    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, int(xCoe*mov), int(yCoe*mov))
                    xPos, yPos = pyautogui.position()
                    break            
        #cv.imshow("Paint", detection_image)
        print("FPS {}".format(1/ (time() - loop_time)))
        loop_time = time()

startWatching()
'''
ventana = tkinter.Tk()
ventana.geometry("400x200")
ventana.title("Paint 3D")
botonStart = tkinter.Button(ventana, text="START", bd=2 , command = startWatching)
botonStart.pack(pady=30)

ventana.mainloop()
'''