from ast import arg
from asyncio.windows_events import NULL
from fileinput import filename
from turtle import back, circle, color
from unicodedata import name
from colorblind_6 import deleteDuplicates, setMinMax
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
        self.average = [0,0,0]
        self.maxRGB = [[1,1,1],[0,0,0]]
        self.minRGB = [[254,254,254],[255,255,255]]
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
        var = 5
        recurse = True
        #maxRGB, secondMaxRGB, minRGB, secondMinRGB = setMinMax(bgr, level)

        #TODO: remove variance or only have it be 1 or 2..?

        # go through all circles and put into data... 
        for i in range(self._circleAmounts[level]):
            tempColor = self.colorSpace[self._stages[level][i][1], self._stages[level][i][0]] # y,x
            # compare each element to those in data and if duplicate with another set duplicate to true
            for x in range(len(self.data)):
                if self.duplicateFound(tempColor, x, var):
                    foundDuplicate = True
                    recurse = False
                    break
            
            if (foundDuplicate == False):
                # color, duplicate T/F, index, amount, singleVariance
                self.data.append([tempColor, False, i ,1 ,0]) 
            else:
                foundDuplicate = False
            
            # self.setMinMaxRGB()

        if recurse:
            var -= 3
            self.setData(level)


    #TODO: re-write the function using maxRGB, min RGB defined above as max / second [[,,],[,,]]
    # setMinMax used in set data
    def setMinMaxRGB(self):
        maxRGB = [1,1,1]
        secondMaxRGB = [0,0,0]
        minRGB = [254,254,254]
        secondMinRGB = [255,255,255]

        for i in range(circleAmounts[level]):
            color1 = bgr[stages[level][i][1],stages[level][i][0]] # y, x
            for z in range(3):
                if (color1[z] > secondMaxRGB[z] and color1[z] != maxRGB[z]):
                    if (color1[z] > maxRGB[z]):
                        secondMaxRGB[z] = maxRGB[z]
                        maxRGB[z] = color1[z]
                    else:
                        secondMaxRGB[z] = color1[z]
                if (color1[z] < secondMinRGB[z] and color1[z] != minRGB[z]):
                    if (color1[z] < minRGB[z]):
                        secondMinRGB[z] = minRGB[z]
                        minRGB[z] = color1[z]
                    else:
                        secondMinRGB[z] = color1[z]

        return (maxRGB, secondMaxRGB, minRGB, secondMinRGB)

    def duplicateFound(self, tempColor, x, var):
        if ((tempColor[0] < self.data[x][0][0] + var) and (tempColor[0] > self.data[x][0][0] - var) and 
            (tempColor[1] < self.data[x][0][1] + var) and (tempColor[1] > self.data[x][0][1] - var) and
            (tempColor[2] < self.data[x][0][2] + var) and (tempColor[2] > self.data[x][0][2] - var)):
            self.data[x][1] = True
            self.data[x][3] += 1 # counter of number of duplicate elements
            return True

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

    # Post-condition: average is set based off of rgb of all values
    #                 duplicat data elements set to True are removed
    def deleteDuplicatesAndComputeAverageOfDuplicates(self):
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

        avg[0] = round(avg[0] / counter)
        avg[1] = round(avg[1] / counter)
        avg[2] = round(avg[2] / counter)

        self.average = avg

    #TODO: implement this function
    def setSingleVariance(self):
        

        print('maxRGB: ', maxRGB, 'secondMaxRGB: ', secondMaxRGB)
        print('minRGB: ', minRGB, 'secondMinRGB: ', secondMinRGB)

        for i in range(len(data)):
            for x in range(3):
                if (data[i][0][x] == maxRGB[x]):
                    temp = maxRGB[x] - secondMaxRGB[x]
                    #print(i, " : ", x, ": ", temp)
                    if temp > data[i][4]:
                        data[i][4] = temp
                if (data[i][0][x] == minRGB[x]):
                    temp = secondMinRGB[x] - minRGB[x]
                    #print(i, " : ", x, ": ", temp)
                    if temp > data[i][4]:
                        data[i][4] = temp

        print("---- left over data -----")
        printLeftOverData(data)

        return (data, backup)