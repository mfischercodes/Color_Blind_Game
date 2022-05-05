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
    data = []
    maxVariance = 0
    pos = 0

    for i in range(2,ranges):
        color1 = getPixel(px, level[i][0], level[i][1])
        if   not((color1[0] <= (matchedColor[0] + var) and color1[0] >= (matchedColor[0] - var)) and
        (color1[1] <= (matchedColor[1] + var) and color1[1] >= (matchedColor[1] - var)) and
        (color1[2] <= (matchedColor[2] + var) and color1[2] >= (matchedColor[2] - var)) ):
            for j in range(3):
                dif = abs(color1[j] - matchedColor[j])
                if dif > maxVariance:
                    maxVariance = dif
                    pos = i
            print(maxVariance)
            for x in range(len(data)):
                if maxVariance > data[x]:
                    data.insert(0, maxVariance)
                else:
                    data.append(maxVariance)
    
    for i in range(len(data)):
        print(data[i], end = "   ||  ")
    # Click all of them check if next level somehow....
    mouse.move(level[pos][0], level[pos][1])
    mouse.click('left')
    print()
    
    
            
def checkRanges(level, ranges):
    screenshot = ImageGrab.grab()
    px = screenshot.load()
    for i in range(ranges):
        color1 = getPixel(px, level[i][0], level[i][1])
        print(i, color1)
    
def checkCircle(level, ranges):
    for i in range(9):
        screenshot = ImageGrab.grab()
        px = screenshot.load()
        mouse.move(level[0 + i][0], level[0+i][1])
        color1 = getPixel(px, level[i][0], level[i][1])
        print(color1)
        time.sleep(0.5)

def getAllColors(level, ranges):
    screenshot = ImageGrab.grab()
    px = screenshot.load()

    data = []
    var = 5

    for i in range(ranges):
        mouse.move(level[0 + i][0], level[0+i][1])
        color1 = getPixel(px, level[i][0], level[i][1])
        print(color1)
        
        time.sleep(0.1)

        data.append(color1)

    print ("data")

    for i in range(len(data)):
        print(data[i], end = "   ||    ")


def runGame():
    for j in range(3):
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
    

level1 = [(4600,600), (4800,600), (4600,900), (4800,900)]

level2 = [  (4500,550), (4700,550), (4900,550), 
            (4500,725), (4700,725), (4900,725),
            (4500,950), (4700,950), (4900,950),]

level3 = [  (4500,500), (4650,500), (4800,500), (4900,500),
            (4500,650), (4650,650), (4800,650), (4900,650),
            (4500,800), (4650,800), (4800,800), (4900,800),
            (4500,950), (4650,950), (4800,950), (4900,950)]

levels = [level1, level2, level3]

ranges = [4, 9, 16]
amounts = [4,16, 30]
var = 10

if __name__ == "__main__":
    # TODO: fix level 2
    if len(sys.argv) == 2:
        if (sys.argv[1] == "1"):
            checkRanges(level2, ranges[1])
        elif (sys.argv[1] == "2"):
            checkRanges(level3, ranges[2])
    else:
        runGame()
    

    

