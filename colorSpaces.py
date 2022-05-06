from ast import arg
from asyncio.windows_events import NULL
from fileinput import filename
from turtle import back, circle, color
from unicodedata import name
import cv2 as cv
import pyautogui as gui
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageGrab
import pyscreenshot as ImageGrab

class colorSpaces:
    _ssRegion = (4300,325,5100,1125) # screen shot region upper_x, upper_y, lower_x, lower_y
    _ssDefault = 'Photos/screenshot'
    _ssExtention = '.png'

    def __init__(self, name = 'bgr', debugging = False):
        self.name = name
        self.debugging = debugging
        self.data = NULL
        self.colorSpace = NULL
        
        if name == 'bgr':
            self.colorSpace = self.convertBGR()
        elif name == 'hsv':
            self.colorSpace = self.convertHSV()
        else:
            self.colorSpace = cv.imread(self._ssDefault + self._ssExtention)

    #TODO: Delete as never used???
    def grabScreenShot(self):
        img = ImageGrab.grab(bbox=(self._ssRegion[0], 
                self._ssRegion[1], self._ssRegion[2], self._ssRegion[3])) #top_x,top_y, bot_x, bot_y
        img.save(self._ssDefault + self._ssExtention)
        return img
    # def saveScreenShot(self):
    #     self.image.save(self._ssDefault + self._ssExtention) 
    
    # Pre-requirement: new screenshot must be taken before set can be called
    def setColorSpace(self):
        if name == 'bgr':
            self.colorSpace = self.convertBGR()
        elif name == 'hsv':
            self.colorSpace = self.convertHSV()
        else:
            self.colorSpace = cv.imread(self._ssDefault + self._ssExtention)

    def convertBGR(self):
        img = cv.imread(self._ssDefault + self._ssExtention)
        colorSpace = cv.cvtColor(img, cv.COLOR_HSV2BGR)
        cv.imwrite(self._ssDefault + '_' + self.name+ self._ssExtention, colorSpace)

        if self.debugging:
            cv.imshow(self.name, colorSpace)
            cv.waitKey(2)

        return colorSpace

    def convertHSV(self):
        # TODO: 75 hue, 65 saturation helps , saturation not added to this yet
        img = cv.imread(self._ssDefault + self._ssExtention)
        bgr = img[:,:,0:3]

        hsv_temp = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
        h,s,v = cv.split(hsv_temp)

        purple = 200 # 0 to 360
        green = 60 # 0 to 360

        diff_color = green - purple

        hnew = np.mod(h + diff_color, 180).astype(np.uint8)
        hsv_new = cv.merge([hnew,s,v])
        colorSpace = cv.cvtColor(hsv_new, cv.COLOR_HSV2BGR)

        cv.imwrite(self._ssDefault + '_' + self.name + self._ssExtention, colorSpace)

        if self.debugging:
            cv.imshow("hsv", colorSpace)
            cv.waitKey(2)
        
        return colorSpace