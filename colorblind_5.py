from turtle import color
from PIL import Image, ImageGrab
import mouse
import time
import sys

#TODO: Get to 100! Then done

def getPixel(px, x,y):
    mouse.move(x, y)
    pixel = px[x,y]
    return pixel

def computeSubVariance(data, i, baseColor):
    return  (   abs(int(data[i][0][0]) - int(baseColor[0])) \
            +   abs(int(data[i][0][1]) - int(baseColor[1])) \
            +   abs(int(data[i][0][2]) - int(baseColor[2])) )

def compareMaxVariance(px, data, level):
    baseColor = getPixel(px, level[0][0], level[0][1])
    maxVariance = 0
    index = 0
    subVariance = 0

    for i in range(len(data)):
        if data[i][2] == 0:
            secondColor = getPixel(px, level[1][0], level[1][1])
            subVariance = computeSubVariance(data, i, secondColor)
        else:
            subVariance = computeSubVariance(data, i, baseColor)

        print(subVariance)
        if (subVariance > maxVariance):
            maxVariance = subVariance
            index = data[i][2]

    print("index :", index, "\n")
    return index

def findMismatch(px, level, ranges):
    data = []
    # color, T/F, #
    # TODO: variance 2 as exactly center similar points being same rgb value
    # TODO: level 1,2,3 get middle coordinates
    # var = 6
    var = 6
    backupValue = 0
    backupIndex = 0

    foundDuplicate = False
    baseColor = getPixel(px, level[0][0], level[0][1])

    for i in range(ranges):
        color1 = getPixel(px, level[i][0], level[i][1])
        print (i, " : " , color1)
        for x in range(len(data)):
            # if duplicate in array, set it to true
            if ((color1[0] < data[x][0][0] + var) and (color1[0] > data[x][0][0] - var) and 
                (color1[1] < data[x][0][1] + var) and (color1[1] > data[x][0][1] - var) and
                (color1[2] < data[x][0][2] + var) and (color1[2] > data[x][0][2] - var)):
                data[x][1] = True
                foundDuplicate = True
                break
        
        if (foundDuplicate == False):
            data.append([color1, False, i])
        else:
            foundDuplicate = False
    
    if (len(data) >= 1):
        for i in range(len(data)):
            print(data[i])
            if abs(data[i][0][0] - baseColor[0]) > backupValue:
                backupIndex = data[i][2]
            if abs(data[i][0][1] - baseColor[1]) > backupValue:
                backupIndex = data[i][2]
            if abs(data[i][0][2] - baseColor[2]) > backupValue:
                backupIndex = data[i][2]

    for i in range(len(data) - 1,-1, -1):
        if (data[i][1] == True):
            data.pop(i)


    #computeSubVariance(data, i, baseColor)
    print()
    if (len(data) > 0):
        for i in range(len(data)):
            pass
            # print(data[i])
        
        # grab max variance here
        index = compareMaxVariance(px, data,level)
        #pos = data[index][2]
        mouse.move(level[index][0], level[index][1])
        mouse.click('left')
    else:
        print("backup!")
        mouse.move(level[backupIndex][0], level[backupIndex][1])
        mouse.click('left')
            
def checkRanges(level, ranges):
    screenshot = ImageGrab.grab()
    px = screenshot.load()
    for i in range(ranges):
        color1 = getPixel(px, level[i][0], level[i][1])
        print(i, color1)

def deepCheckRanges(level, ranges):
    screenshot = ImageGrab.grab()
    px = screenshot.load()
    for i in range(ranges):
        for x in range(82):
            color1 = getPixel(px, level[i][0] - x, level[i][1])
            print(i, color1, x)
        # print("~~~~~~~~")
        # for x in range(100):
        #     color1 = getPixel(px, level[i][0] - x, level[i][1] - x)
        #     print(i, color1, -x)
            # 140 127 1
            # 1 -> 3
            # 2 -> 
            # 3 -> -2

    
def runGame():
    for j in range(5):
        for i in range(amounts[j]):
            screenshot = ImageGrab.grab()
            px = screenshot.load()

            findMismatch(px, levels[j], ranges[j])

            time.sleep(1.25) # between rounds

    # time.sleep(1)
    # mouse.move(2000,500)
    
#region Variables

level1 = [(4600,600), (4800,600), (4600,900), (4800,900)]
level2 = [  (4500,550), (4700,550), (4900,550), 
            (4500,725), (4700,725), (4900,725),
            (4500,950), (4700,950), (4900,950),]
level3 = [  (4500,500), (4650,500), (4800,500), (4900,500),
            (4500,650), (4650,650), (4800,650), (4900,650),
            (4500,800), (4650,800), (4800,800), (4900,800),
            (4500,950), (4650,950), (4800,950), (4900,950)]
level4 = [  (4450,475), (4575,475), (4700,475), (4825,475), (4950,475),
            (4450,600), (4575,600), (4700,600), (4825,600), (4950,600),
            (4450,725), (4575,725), (4700,725), (4825,725), (4950,725),
            (4450,850), (4575,850), (4700,850), (4825,850), (4950,850),
            (4450,975), (4575,975), (4700,975), (4825,975), (4950,975)]
level5 = [  (4450,475), (4550,475), (4650,475), (4750,475), (4850,475), (4950,475),
            (4450,575), (4550,575), (4650,575), (4750,575), (4850,575), (4950,575),
            (4450,675), (4550,675), (4650,675), (4750,675), (4850,675), (4950,675),
            (4450,775), (4550,775), (4650,775), (4750,775), (4850,775), (4950,775),
            (4450,875), (4550,875), (4650,875), (4750,875), (4850,875), (4950,875),
            (4450,975), (4550,975), (4650,975), (4750,975), (4850,975), (4950,975)]

levels = [level1, level2, level3, level4, level5]

ranges = [4, 9, 16, 25, 36] # amount of circles
amounts = [4, 15, 15, 15, 25] #iterations
var = 8
#endregion

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        if (sys.argv[1] == "0"):
            deepCheckRanges(level1, ranges[0])
        elif (sys.argv[1] == "1"):
            checkRanges(level2, ranges[1])
        elif (sys.argv[1] == "2"):
            checkRanges(level3, ranges[2])
    elif (len(sys.argv) == 3):
        screenshot = ImageGrab.grab()
        px = screenshot.load()
        if (sys.argv[2] == "0"):
            findMismatch(px, level1, ranges[0])
        if (sys.argv[2] == "1"):
            findMismatch(px, level2 , ranges[1])
        elif (sys.argv[2] == "2"):
            findMismatch(px, level3 , ranges[2])
        elif (sys.argv[2] == "3"):
            findMismatch(px, level4 , ranges[3])
        elif (sys.argv[2] == "4"):
            findMismatch(px, level5 , ranges[4])
        elif (sys.argv[2] == "loc"):
            for i in range(36):
                mouse.move(level5[i][0], level5[i][1])
                time.sleep(0.5)
            time.sleep(0.5)
            mouse.move(2000,500)
    else:
        runGame()
    

    

