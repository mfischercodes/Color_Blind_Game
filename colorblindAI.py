grab screenshot

print rgb values of each circle

var = 5
circleArray = []

if circle2 + var < circle1 and circle2 - var > circle1:
    #circle2 and circle1 have the same rgb values
    if not circle2 in circleArray:
        # if not duplicate in array then place in array
        circleArray.append(circle2)
else:
    circleArray.append(circle2)