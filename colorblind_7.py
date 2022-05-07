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
    level = 0
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

    def __init__(self, debugging = False):
        self.debugging = debugging
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
    # Post-condition: ColorSpaces objects.data is set t
    def setData(self):
        self.rgb.setData(self.level)
        self.bgr.setData(self.level)
        self.hsv.setData(self.level)

        if self.debugging:
            self.rgb.printData()
            self.bgr.printData()
            self.hsv.printData()

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
        self.removeDuplicatesAndComputeAverageOfDuplicates()

        # average is used for comparing max variance from all rgb values
        # min, max rgb used for comparing single max variance across all rgb values

    def ClickMouse(self):
        mouse.move(self._stages[self.currentLevel][self.clickIndex][0] + self._mouseClickOffset[0], 
                   self._stages[self.currentLevel][self.clickIndex][1] + self._mouseClickOffset[1])
        time.sleep(self.clickDelay)
        if not self.debugging:
            mouse.click('left')

def setMinMax(bgr, level):
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

def setData(bgr, level, var):
    data = []
    foundDuplicate = False
    recurse = True
    maxRGB, secondMaxRGB, minRGB, secondMinRGB = setMinMax(bgr, level)
    #TODO: use different sorting algorithmn? Sorted array?
    #TODO: Organize functions... make into an OOP so i dont have to transfer data everywhere
    printCircles(bgr,level)

    for i in range(circleAmounts[level]):
        color1 = bgr[stages[level][i][1],stages[level][i][0]] # y, x

        for x in range(len(data)):
            # if duplicate in array, set it to true
            if ((color1[0] < data[x][0][0] + var) and (color1[0] > data[x][0][0] - var) and 
                (color1[1] < data[x][0][1] + var) and (color1[1] > data[x][0][1] - var) and
                (color1[2] < data[x][0][2] + var) and (color1[2] > data[x][0][2] - var)):
                data[x][1] = True
                data[x][3] += 1
                foundDuplicate = True
                break
        
        if (foundDuplicate == False):
            data.append([color1, False, i, 1, 0])
        else:
            foundDuplicate = False

    for i in range(len(data)):
        if data[i][1] == False and recurse == True:
            recurse = False

    # if all data true re-run setData with lower variance
    if recurse == True:
        print("---all data true, recurse")
        var -= 3
        return setData(bgr,level, var)
    else:
        print("---- all data -----")
        printData(data)

        backup = deleteDuplicates(data)

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

def computeSubVariance(data, i, baseColor):
    return  (   abs(int(data[i][0][0]) - int(baseColor[0])) \
            +   abs(int(data[i][0][1]) - int(baseColor[1])) \
            +   abs(int(data[i][0][2]) - int(baseColor[2])) )

def compareFirstThreeUseThree(bgr, data, level):
    maxSameVariance = 30
    baseColor1 = bgr[stages[level][0][1],stages[level][0][0]] # y, x

    var1v2 = computeSubVariance(data, 1, baseColor1)
    var1v3 = computeSubVariance(data, 2, baseColor1)

    if (var1v2 + var1v3 > maxSameVariance): # 2 mis match use # 3
        return True
    return False

def compareMaxVariance(bgr, data, level, backup): 
    
    baseColor = bgr[stages[level][0][1],stages[level][0][0]] # y, x
    if backup[0] != 0 or backup[1] != 0 or backup[2] != 0:
        print("ran back up")
        baseColor = backup
    # should never run now as recurse for true only data
    else: # if == 0 then no true valus in data use second backup element # 3
        print("ran back up 2")
        if compareFirstThreeUseThree(bgr, data, level):
            baseColor = bgr[stages[level][2][1],stages[level][2][0]] # y, x

    singleMaxVarMinimum = 2
    maxVariance = 0
    singleMaxVariance = 0
    index = 0
    singleIndex = 0

    for i in range(len(data)):
        if data[i][4] > singleMaxVariance:
            singleMaxVariance = data[i][4]
            singleIndex = data[i][2]
        subVariance = computeSubVariance(data, i, baseColor)

        print(subVariance)
        if (subVariance > maxVariance):
            maxVariance = subVariance
            index = data[i][2]

    #TODO: select all if not on next level yet
    #TODO: make screenshot and check for white pixel in the left side of the circle
    #TODO: if not then not next level pop data and select next one

    print('max:', maxVariance, "   singleMax: ", singleMaxVariance)
    print('index: ', index, 'singleVar: ', singleIndex)
    if (singleIndex != index and singleMaxVariance > singleMaxVarMinimum):
        print("single index chosen:", singleIndex, "other index:", index)
        return singleIndex
    else:
        print("index chosen:", index, "single index:", singleIndex)
        return index

def findMisMatch(bgr, level):
    var = 3
    data, backup = setData(bgr,level, var)
    index = compareMaxVariance(bgr, data, level, backup)
    return index

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
            cb = colorBlindAI(True)
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
        runGame()



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
