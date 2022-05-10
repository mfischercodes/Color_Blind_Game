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
import mouse
import time
import sys
from colorSpaces import colorSpaces

#TODO: refactor
#TODO: make color Object of just plain BGR and compare to that one too
#TODO: make a main program instead of having main run in init 
#       so I can loop for next level
#TODO: set data, etc in ColorSpaces
#TODO: do bgr2hsv color space?
# colorSpace = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#TODO: compare all color modes and find most common matching one?
#TODO: Make some color modes selection null if it is close to black or white

class colorBlindAI:
    clickDelay = 1
    clickIndex = 0
    _ssDefault = 'Photos/screenshot'
    _ssExtention = '.png'
    
    _ssRegion = (4300,325,5100,1125) # screen shot region upper_x, upper_y, lower_x, lower_y
    _circleAmounts = [4, 9, 16, 25, 36] # amount of circles per level
    _levelAmounts = [4, 15, 15, 15, 25] # amount of levels with same grid pattern
    _mouseClickOffset = (4280,320)

    #region stages
    _stage2x2 = [(250,250), (550,250),
                 (250,550), (550,550)]
    _stage3x3 = [(200,200), (400,200), (600,200),
                (200,400), (400,400), (600,400),
                (200,600), (400,600), (600,600)]
    _stage4x4 = [(180,200), (325,200), (465,200), (600,200),
                (180,335), (325,335), (465,335), (600,335),
                (180,480), (325,480), (465,480), (600,480),
                (180,620), (325,620), (465,620), (600,620)]
    _stage5x5 = [(140,155), (265,155), (395,155), (520,155), (650,155), 
                (140,280), (265,280), (395,280), (520,280), (650,280), 
                (140,410), (265,410), (395,410), (520,410), (650,410), 
                (140,535), (265,535), (395,535), (520,535), (650,535), 
                (140,660), (265,660), (395,660), (520,660), (650,660)]
    _stage6x6 = [(147,165), (245,165), (345,165), (445,165), (540,165), (640,165), 
                (147,265), (245,265), (345,265), (445,265), (540,265), (640,265), 
                (147,360), (245,360), (345,360), (445,360), (540,360), (640,360), 
                (147,455), (245,455), (345,455), (445,455), (540,455), (640,455), 
                (147,555), (245,555), (345,555), (445,555), (540,555), (640,555), 
                (147,655), (245,655), (345,655), (445,655), (540,655), (640,655)]
    #endregion

    _stages = [_stage2x2, _stage3x3, _stage4x4, _stage5x5, _stage6x6]

    def __init__(self, debugging = False, level = 0):
        self.debugging = debugging
        self.level = level
        self.subLevels = 1
        self.indexCounter = []
        self.image = NULL
        self.rgb = NULL
        self.bgr = NULL
        self.hsv = NULL
        
    # Description: prints the rgb values of all 3 ColorSpace objects circles
    def printCircles(self):
        if self.debugging:
            self.rgb.printCirclesRGB(self.level)
            self.bgr.printCirclesRGB(self.level)
            self.hsv.printCirclesRGB(self.level)

    # Description: Grabs a screenshot from the given coordinates in _ssRegion
    # Post-condition: sets self.image
    def setImage(self):
        self.image = ImageGrab.grab(bbox=(self._ssRegion[0], 
                self._ssRegion[1], self._ssRegion[2], self._ssRegion[3])) #top_x,top_y, bot_x, bot_y
        self.image.save(self._ssDefault + self._ssExtention)

    # Description: set 3 ColorSpace objects with different color modes
    def setColorSpaces(self):
        self.rgb = colorSpaces('rgb')
        self.bgr = colorSpaces('bgr')
        self.hsv = colorSpaces('hsv')

    # Description: adds to obj.data [rgb color, duplicate T/F, index, amount, max variance]
    # Post-condition: ColorSpaces obj.data is changed
    #                 ColorSpaces obj.maxRGB and obj.minRGB is changed
    def setData(self):
        self.rgb.setData(self.level)
        self.bgr.setData(self.level)
        self.hsv.setData(self.level)

        if self.debugging:
            self.rgb.printData()
            self.bgr.printData()
            self.hsv.printData()

    def setMaxVariances(self):
        self.rgb.setMaxVariance()
        self.bgr.setMaxVariance()
        self.hsv.setMaxVariance()

        if self.debugging:
            self.rgb.printData()
            self.bgr.printData()
            self.hsv.printData()

    def setIndexCounter(self, objectName):
        indexObjectM = 0
        indexObjectS = 0
        ranOnceM = False
        ranOnceS = False

        if objectName == 'rgb':
            indexObjectM = self.rgb.multipleIndex
            indexObjectS = self.rgb.singleIndex
        elif objectName == 'bgr':
            if self.bgr.isBlack:
                return
            indexObjectM = self.bgr.multipleIndex
            indexObjectS = self.bgr.singleIndex
        else:
            indexObjectM = self.hsv.multipleIndex
            indexObjectS = self.hsv.singleIndex
        
        for i in range(len(self.indexCounter)):
            if indexObjectM == self.indexCounter[i][0]:
                self.indexCounter[i][1] += 1
                ranOnceM = True
        if not ranOnceM:
            self.indexCounter.append([indexObjectM, 1, 'M'])

        for i in range(len(self.indexCounter)):
            if indexObjectS == self.indexCounter[i][0]:
                self.indexCounter[i][1] += 1
                ranOnceS = True
        if not ranOnceS:
            self.indexCounter.append([indexObjectS, 1, 'S'])

        

    def setMisMatchIndex(self):
        self.setIndexCounter(self.rgb.name)
        self.setIndexCounter(self.bgr.name)
        self.setIndexCounter(self.hsv.name)

        max = 0
        single = False
        index = 0

        for i in range(len(self.indexCounter)):
            if self.indexCounter[i][1] > max:
                max = self.indexCounter[i][1]
                index = self.indexCounter[i][0]
                if self.indexCounter[i][2] == 'S':
                    single = True
                else:
                    single = False
            if self.indexCounter[i][1] == max:
                if single == False and self.indexCounter[i][2] == 'S':
                    max = self.indexCounter[i][1]
                    index = self.indexCounter[i][0]
                    single = True

        self.clickIndex = index

        if self.debugging:
            print("index counter: ", self.indexCounter)
            print('max: ', max, '   index: ', index)
            print('bgr is black: ', self.bgr.isBlack)
            print()
        

        if self.debugging:
            print(self.rgb.name, " multipleIndex: ", self.rgb.multipleIndex, "   singleIndex: ", self.rgb.singleIndex)
            print(self.bgr.name, " multipleIndex: ", self.bgr.multipleIndex, "   singleIndex: ", self.bgr.singleIndex)
            print(self.hsv.name, " multipleIndex: ", self.hsv.multipleIndex, "   singleIndex: ", self.hsv.singleIndex)
        

    # Description: computes the average of all the true obj.data and deletes duplicates
    # Post-condition: removes all duplicates from ColorSpaces obj.data
    #                 sets obj.average 
    def removeDuplicatesAndComputeAverageOfDuplicates(self):
        self.rgb.deleteDuplicatesAndComputeAverageOfDuplicates()
        self.bgr.deleteDuplicatesAndComputeAverageOfDuplicates()
        self.hsv.deleteDuplicatesAndComputeAverageOfDuplicates()

    # Description: grabs, screenshot, sets 3 color objects, cleans data, finds mismatch
    def nextLevel(self):
        self.setImage()
        self.setColorSpaces()
        self.printCircles()
        self.setData()
        # self.removeDuplicatesAndComputeAverageOfDuplicates()
        self.bgr.setBlack()
        self.setMaxVariances()
        self.setMisMatchIndex()
        self.ClickMouse()
        if self.subLevels == self._levelAmounts[self.level]:
            self.level += 1
            self.subLevels = 0
        self.subLevels += 1
        self.indexCounter = []
        #TODO: remove variance and fix recurse with setting average to average of 3
        #TODO: record audio for youtube video


    def ClickMouse(self):
        mouse.move(self._stages[self.level][self.clickIndex][0] + self._mouseClickOffset[0], 
                   self._stages[self.level][self.clickIndex][1] + self._mouseClickOffset[1])
        time.sleep(self.clickDelay)
        if not self.debugging:
            mouse.click('left')


def runGame():
    for j in range(len(stages)):
        for i in range(levelAmounts[j]):
            grabImage(4300,325,5100,1125) # 800, 800
            bgr = convertBGR(False, j)
            index = findMisMatch(bgr,j)
            clickMouse(index, j, True)
            time.sleep(1) # between rounds 

if __name__ == "__main__":
    if len(sys.argv) == 3:
        if(sys.argv[1] == "l"):
            i = int(sys.argv[2]) - 2
            for j in range(levelAmounts[i]):
                grabImage(4300,325,5100,1125) # 800, 800
                bgr = convertBGR(False, i)
                index = findMisMatch(bgr,i)
                print(index)
                clickMouse(index, i, True)
                
                time.sleep(1.25) # between rounds   

        elif(sys.argv[1] == "p"):
            level = int(sys.argv[2]) - 2
            cb = colorBlindAI(True, level)
            cb.nextLevel()
            # cb.printCirclesRGB()
            
            # grabImage(4300,325,5100,1125) # 800, 800
            # i = int(sys.argv[2]) - 2
            # # print(i)
            # bgr = convertBGR(True, i)
            # index = findMisMatch(bgr,i)
            # print(index)
            # clickMouse(index, i, False)
            #TODO: put click mouse into findMisMatch and check for white circle on left

        elif(sys.argv[1] == "s"):
            grabImage(4300,325,5100,1125) # 800, 800
            print('screenshot')

        else:
            print('use arguments:\nl2   \np2   \nss')

    else:
        cb = colorBlindAI(True)
        for i in range(500):
            cb.nextLevel()
            time.sleep(1)
        #runGame()



#region cvtColor
#BGR to Grayscale
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow("Gray", gray)

#BGR to HSV
# hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# cv.imshow("HSV", hsv)

# #BGR to RGB
# rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# cv.imshow("RGB", rgb)

#BGR to hls
# hls = cv.cvtColor(img, cv.COLOR_BGR2HLS)
# cv.imshow("GB", hls)

# #BGR to LAb
# lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
# cv.imshow("LAB", lab)


# https://www.youtube.com/watch?v=oXlwWbU8l2o
# time 1:23:25 for color channel splitting may work bettwe than 
#endregion
