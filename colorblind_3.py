from turtle import color
from PIL import Image, ImageGrab
import mouse
import time
import sys

def getPixel(px, x,y):
    mouse.move(x, y)
    pixel = px[x,y]
    time.sleep(0.05)
    return pixel

def clickMouse(x,y):
    mouse.move(x,y)
    mouse.click('left')

def matchingFirstTwo(px, level):
    color1 = getPixel(px, level[0][0], level[0][1])
    color2 = getPixel(px, level[1][0], level[1][1])

    if   ((color2[0] < (color1[0] + 10) and color2[0] > (color1[0] - 10)) and
         (color2[1] < (color1[1] + 10) and color2[1] > (color1[1] - 10)) and
         (color2[2] < (color1[2] + 10) and color2[2] > (color1[2] - 10)) ):
        return (color1)

    return (500,500,500)

def colorInThree(px, level):
    # TODO: Compare like in findmismatch here

    color1 = getPixel(px, level[0][0], level[0][1])
    color2 = getPixel(px, level[1][0], level[1][1])
    color3 = getPixel(px, level[2][0], level[2][1])

    if   ((color3[0] <= (color1[0] + var) and color3[0] >= (color1[0] - var)) and
         (color3[1] <= (color1[1] + var) and color3[1] >= (color1[1] - var)) and
         (color3[2] <= (color1[2] + var) and color3[2] >= (color1[2] - var)) ):
        clickMouse(level[1][0], level[1][1])
        return (color2)

    if   ((color3[0] <= (color2[0] + var) and color3[0] >= (color2[0] - var)) and
         (color3[1] <= (color2[1] + var) and color3[1] >= (color2[1] - var)) and
         (color3[2] <= (color2[2] + var) and color3[2] >= (color2[2] - var)) ):
        clickMouse(level[0][0], level[0][1])
        
        return (color1)

def findMismatch(px, level, matchedColor, ranges):
    data = [[matchedColor, False, 0]]
    var = 6
    print(1, " : ", matchedColor)

    foundDuplicate = False

    for i in range(2,ranges):
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
            print("append: ", i)
            data.append([color1, False, i])
        else:
            foundDuplicate = False
    
    print("with duplicated\n")
    for i in range(len(data)):
        print(data[i])
    
    for i in range(len(data) - 1,-1, -1):
        if (data[i][1] == True):
            data.pop(i)
    print("\nafter pops\n")
    for i in range(len(data)):
        print(data[i])
    
    pos = data[0][2]
    mouse.move(level[pos][0], level[pos][1])
    mouse.click('left')
            
def checkRanges(level, ranges):
    screenshot = ImageGrab.grab()
    px = screenshot.load()
    for i in range(ranges):
        color1 = getPixel(px, level[i][0], level[i][1])
        print(i, color1)
    
def runGame():
    for j in range(4):
        for i in range(amounts[j]):
            screenshot = ImageGrab.grab()
            px = screenshot.load()

            matchedColor = matchingFirstTwo(px, levels[j])

            if (matchedColor == (500,500,500)):
                colorInThree(px, levels[j])
            else:
                findMismatch(px, levels[j], matchedColor, ranges[j])

            time.sleep(1)
    time.sleep(1)
    mouse.move(2000,500)
    
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
levels = [level1, level2, level3, level4]

ranges = [4, 9, 16, 25] # amount of circles
amounts = [4, 15, 15] #iterations
#endregion

if __name__ == "__main__":
    # TODO: fix level 2
    
    if len(sys.argv) == 2:
        if (sys.argv[1] == "1"):
            checkRanges(level2, ranges[1])
        elif (sys.argv[1] == "2"):
            checkRanges(level3, ranges[2])
    elif (len(sys.argv) == 3):
        screenshot = ImageGrab.grab()
        px = screenshot.load()
        if (sys.argv[2] == "0"):
            matchedColor = matchingFirstTwo(px, level1)
            findMismatch(px, level1, matchedColor, ranges[0])
        if (sys.argv[2] == "1"):
            matchedColor = matchingFirstTwo(px, level2)
            findMismatch(px, level2, matchedColor, ranges[1])
        elif (sys.argv[2] == "2"):
            matchedColor = matchingFirstTwo(px, level3)
            findMismatch(px, level3, matchedColor, ranges[2])
        elif (sys.argv[2] == "3"):
            matchedColor = matchingFirstTwo(px, level4)
            findMismatch(px, level4, matchedColor, ranges[3])
        elif (sys.argv[2] == "loc"):
            for i in range(25):
                mouse.move(level4[i][0], level4[i][1])
                time.sleep(0.5)
            time.sleep(0.5)
            mouse.move(2000,500)
            # matchedColor = matchingFirstTwo(px, level4)
            # findMismatch(px, level4, matchedColor, ranges[3])
    else:
        runGame()
    

    

