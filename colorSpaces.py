from ast import arg
from asyncio.windows_events import NULL
from fileinput import filename
from turtle import back, circle, color
from unicodedata import name
from colorblind_6 import compareFirstThreeUseThree, deleteDuplicates, setMinMax
import cv2 as cv
import pyautogui as gui
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageGrab
import pyscreenshot as ImageGrab

class colorSpaces:
    _ssDefault = 'Photos/screenshot'
    _ssExtention = '.png'

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

    _circleAmounts = [4, 9, 16, 25, 36] # amount of circles per level
    _stages = [_stage2x2, _stage3x3, _stage4x4, _stage5x5, _stage6x6]

    def __init__(self, name = 'bgr', debugging = False):
        self.name = name
        self.debugging = debugging
        self.data = []
        self.singleIndex = 0
        self.isBlack = False
        self.singleMaxVariance = 0 # may not need this as a variable
        self.multipleIndex = 0
        self.multipleMaxVariance = 0
        self.average = [0,0,0]
        self.maxRGB = [[1,1,1],[0,0,0]] # max, second max
        self.minRGB = [[254,254,254],[255,255,255]] # min, second min
        self.colorSpace = NULL
        
        if name == 'bgr':
            self.colorSpace = self.convertBGR()
        elif name == 'hsv':
            self.colorSpace = self.convertHSV()
        else:
            self.colorSpace = cv.imread(self._ssDefault + self._ssExtention)

    # Pre-requirement: new screenshot must be taken before set can be called
    def setColorSpace(self):
        if name == 'bgr':
            self.colorSpace = self.convertBGR()
        elif name == 'hsv':
            self.colorSpace = self.convertHSV()
        else:
            self.colorSpace = cv.imread(self._ssDefault + self._ssExtention)

    def setData(self, level):
        foundDuplicate = False

        # go through all circles and put into data... 
        for i in range(self._circleAmounts[level]):
            tempColor = self.colorSpace[self._stages[level][i][1], self._stages[level][i][0]] # y,x
            self.setMinMaxRGB(i, tempColor)
            
            # compare each element to those in data and if duplicate with another set duplicate to true
            for x in range(len(self.data)):
                if self.duplicateFound(tempColor, x):
                    foundDuplicate = True
                    # recurse = False
                    break
            
            if (foundDuplicate == False):
                # color, duplicate T/F, index, amount, singleVariance
                self.data.append([tempColor, False, i ,1 ,0]) 
            else:
                foundDuplicate = False

    def setMinMaxRGB(self, i, tempColor):
        for z in range(3):
            if (tempColor[z] > self.maxRGB[1][z] and tempColor[z] != self.maxRGB[0][z]):
                if (tempColor[z] > self.maxRGB[0][z]):
                    self.maxRGB[1][z] = self.maxRGB[0][z]
                    self.maxRGB[0][z] = tempColor[z]
                else:
                    self.maxRGB[1][z] = tempColor[z]
            if (tempColor[z] < self.minRGB[1][z] and tempColor[z] != self.minRGB[0][z]):
                if (tempColor[z] < self.minRGB[0][z]):
                    self.minRGB[1][z] = self.minRGB[0][z]
                    self.minRGB[0][z] = tempColor[z]
                else:
                    self.minRGB[1][z] = tempColor[z]

    def setSingleVarianceAndIndex(self, tempVar, i):
        if tempVar > self.singleMaxVariance:
            self.singleMaxVariance = tempVar
            self.singleIndex = self.data[i][2]

    def setMultipleVarianceAndIndex(self, i):
        subVariance = self.computeSubVariance(i)
        if (subVariance > self.multipleMaxVariance):
            self.multipleMaxVariance = subVariance
            self.multipleIndex = self.data[i][2]

    def setBlack(self):
        var = 50
        if  ((self.data[0][0][0] < var and self.data[0][0][1] < var and self.data[0][0][2] < var) and 
             (self.data[1][0][0] < var and self.data[1][0][1] < var and self.data[1][0][2] < var)):
                self.isBlack = True

    def setMaxVariance(self):
        tempVar = 0
        for i in range(len(self.data)):
            self.setMultipleVarianceAndIndex(i)

            for x in range(3):
                if (self.data[i][0][x] == self.maxRGB[0][x]):
                    tempVar = self.maxRGB[0][x] - self.maxRGB[1][x]
                    if tempVar > self.data[i][4]:
                        self.data[i][4] = tempVar
                if (self.data[i][0][x] == self.minRGB[0][x]):
                    tempVar = self.minRGB[1][x] - self.minRGB[0][x]
                    if tempVar > self.data[i][4]:
                        self.data[i][4] = tempVar

                self.setSingleVarianceAndIndex(tempVar, i)

    def setMultipleIndex(self):
        maxVariance = 0
        index = 0
        for i in range(len(self.data)):
            subVariance = self.computeSubVariance(i)
            if (subVariance > maxVariance):
                maxVariance = subVariance
                index = self.data[i][2]
        return index

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

    def printCirclesRGB(self, level):
        print(self.name)
        for i in range(self._circleAmounts[level]):
            px = self.colorSpace[self._stages[level][i][1],self._stages[level][i][0]] # y, x
            print(i, ": ", px)
        print()

    def printData(self):
        print(self.name)
        for i in range(len(self.data)):
            print(self.data[i])
        print()

    def duplicateFound(self, tempColor, x):
        if ((tempColor[0] == self.data[x][0][0]) and 
            (tempColor[1] == self.data[x][0][1]) and
            (tempColor[2] == self.data[x][0][2]) ):
            self.data[x][1] = True
            self.data[x][3] += 1 # counter of number of duplicate elements
            return True

    # Post-condition: average is set based off of rgb of all values
    #                 duplicate data elements set to True are removed
    def deleteDuplicatesAndComputeAverageOfDuplicates(self, level):
        avg = [0,0,0]
        counter = 0
        for i in range(len(self.data) - 1,-1, -1):
            if (self.data[i][1] == True):
                for x in range(self.data[i][3]):
                    avg[0] += self.data[i][0][0]
                    avg[1] += self.data[i][0][1]
                    avg[2] += self.data[i][0][2]
                    counter += 1
                self.data.pop(i)

        if self.isBlack:
            self.average = [1,1,1]
            return

        if avg == [0,0,0]:
            self.average = self.compareFirstThree(level)
            return

        avg[0] = round(avg[0] / counter)
        avg[1] = round(avg[1] / counter)
        avg[2] = round(avg[2] / counter)

        self.average = avg

    def computeSubVariance(self, i):
        return  (   abs(int(self.data[i][0][0]) - int(self.average[0])) \
                +   abs(int(self.data[i][0][1]) - int(self.average[1])) \
                +   abs(int(self.data[i][0][2]) - int(self.average[2])) )

    def compare2Circles(self, i, baseColor):
        return  (   abs(int(self.data[i][0][0]) - int(baseColor[0])) \
                +   abs(int(self.data[i][0][1]) - int(baseColor[1])) \
                +   abs(int(self.data[i][0][2]) - int(baseColor[2])) )

    def compareFirstThree(self, level):
        maxSameVariance = 30
        baseColor1 = self.colorSpace[self._stages[level][0][1],self._stages[level][0][0]] # y, x
        baseColor3 = self.colorSpace[self._stages[level][2][1],self._stages[level][2][0]] # y, x

        if (self.compare2Circles(1, baseColor1) > maxSameVariance):
            return baseColor1
        return baseColor3

    