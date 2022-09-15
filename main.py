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

vision_item = Vision("albion_cabbage7.jpg")

#vision_item.init_control_gui()
def startWatching():
    toggle = 1
    loop_time = time()
    while(True):
        xPos, yPos = pyautogui.position()
        if toggle:
            wincap = WindowCapture("Counter-Strike: Global Offensive - Direct3D 9")
            screenshot = wincap.get_screenshot()

            #processed_image = vision_item.apply_hsv_filter(screenshot)

            rectangles = vision_item.find(screenshot, 0.70, 0, 0)
            for rect in rectangles:
                xPos, yPos = pyautogui.position()
                xObj = int(rect[0]+(rect[2]/2))
                yObj = int(rect[1]+(rect[3]/2))
                xCoe = (xObj-xPos)/100
                yCoe = (yObj-yPos)/100
                sensibilidad = 4.0
                mov = 22*sensibilidad
                print("Inicial: x="+str(xPos)+", y="+str(yPos) + " Objetivo: x="+str(xObj)+", y="+str(yObj) + " Coeficiente: x="+str(xCoe)+", y="+str(yCoe))
                print()
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, int(xCoe*mov), int(yCoe*mov))
                xPos, yPos = pyautogui.position()
                break
            output_image = vision_item.draw_rectangles(screenshot, rectangles)

            cv.imshow("Paint", output_image)
            #cv.imshow("Processed", processed_image)


            '''print("FPS {}".format(1/ (time() - loop_time)))'''
            loop_time = time()
        if cv.waitKey(1) & 0xFF == ord('n'):
            toggle = 1
        if cv.waitKey(1) & 0xFF == ord('m'):
            toggle = 0

ventana = tkinter.Tk()
ventana.geometry("400x200")
ventana.title("Paint 3D")
botonStart = tkinter.Button(ventana, text="START", bd=2 , command = startWatching)
botonStart.pack(pady=30)

ventana.mainloop()