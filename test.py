from PIL import Image, ImageGrab
import mouse
import time

def getPixel(px, x,y):
    mouse.move(x, y)
    pixel = px[x,y]
    time.sleep(0.1)
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
    color1 = getPixel(px, level[0][0], level[0][1])
    color2 = getPixel(px, level[1][0], level[1][1])
    color3 = getPixel(px, level[2][0], level[2][1])

    if   ((color3[0] <= (color1[0] + var) and color3[0] >= (color1[0] - var)) and
         (color3[1] <= (color1[1] + var) and color3[1] >= (color1[1] - var)) and
         (color3[2] <= (color1[2] + var) and color3[2] >= (color1[2] - var)) ):
        print("mismatch color 2 ", color1 , " : ", color2, " : ", color3)
        clickMouse(level[1][0], level[1][1])
        return (color2)

    if   ((color3[0] <= (color2[0] + var) and color3[0] >= (color2[0] - var)) and
         (color3[1] <= (color2[1] + var) and color3[1] >= (color2[1] - var)) and
         (color3[2] <= (color2[2] + var) and color3[2] >= (color2[2] - var)) ):
        print("mismatch color 1 ", color1 , " : ", color2, " : ", color3)
        clickMouse(level[0][0], level[0][1])
        
        return (color1)

def findMismatch(px, level, matchedColor, ranges):
    for j in range(3):
        varX = var
        for i in range(2,ranges):
            color1 = getPixel(px, level[i][0], level[i][1])

            if   not((color1[0] <= (matchedColor[0] + varX) and color1[0] >= (matchedColor[0] - varX)) and
            (color1[1] <= (matchedColor[1] + varX) and color1[1] >= (matchedColor[1] - varX)) and
            (color1[2] <= (matchedColor[2] + varX) and color1[2] >= (matchedColor[2] - varX)) ):
                print("found color at position ", i, "  ", color1, " : ", matchedColor)
                clickMouse(level[i][0], level[i][1])
                return (color1)
        varX -= 5
        
            

def checkRanges(level, ranges):
    for i in range(ranges[2]):
        screenshot = ImageGrab.grab()
        px = screenshot.load()
        mouse.move(level[i][0], level[i][1])
        color1 = getPixel(px, level[i][0], level[i][1])
        print(color1)
        time.sleep(0.5)
    

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
    

level1 = [(4600,600), (4800,600), (4600,900), (4800,900)]

level2 = [  (4500,550), (4650,550), (4900,550), 
            (4500,700), (4650,700), (4900,700),
            (4500,900), (4650,900), (4900,900),]

level3 = [  (4500,500), (4650,500), (4800,500), (4900,500),
            (4500,650), (4650,650), (4800,650), (4900,650),
            (4500,800), (4650,800), (4800,800), (4900,800),
            (4500,950), (4650,950), (4800,950), (4900,950)]

levels = [level1, level2, level3]



ranges = [5, 9, 16]
amounts = [4,16, 30]
var = 20

if __name__ == "__main__":
    # TODO: fix level 2
    runGame()
    #TODO: fix variance issue of sometimes 12 sometimes 15... just make it run multiple times?
    # checkRanges(level3, ranges)

    time.sleep(1)
    mouse.move(2000,500)

