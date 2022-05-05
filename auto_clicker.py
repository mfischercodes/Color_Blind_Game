from time import *
from tracemalloc import start
import mouse
import keyboard
import time

GLOBAL_X = 2600

start_cords = (2300, 1250)
exit_cords = [(1950,350),(2400,200),(1750, 500)]
upgrade_cords = [(2000,300),(2000,500)]
# 1 archer, 2 knight, 3
hero_skills = (580,730,880)
hero_skills_y = 750

def start_battle():
    mouse.move(GLOBAL_X + exit_cords[0][0], exit_cords[0][1])
    mouse.click('left')
    time.sleep(0.05)
    mouse.move(GLOBAL_X + exit_cords[1][0], exit_cords[1][1])
    mouse.click('left')
    time.sleep(0.05)
    upgrade()
    mouse.move(GLOBAL_X + start_cords[0], start_cords[1])
    mouse.click('left')
    time.sleep(0.25)
    mouse.move(GLOBAL_X + exit_cords[2][0], exit_cords[2][1])
    mouse.click('left')
    time.sleep(1)

def upgrade():
    for i in range(0,10,1):
        mouse.move(GLOBAL_X + upgrade_cords[0][0], upgrade_cords[0][1])
        mouse.click('left')
        mouse.move(GLOBAL_X + upgrade_cords[1][0], upgrade_cords[1][1])
        mouse.click('left')
        time.sleep(0.05)

def heros():
    for i in range(3):
        mouse.move(GLOBAL_X + hero_skills[i], hero_skills_y)
        mouse.click('left')
        time.sleep(0.05)



# time.sleep(1)

# mouse.move(GLOBAL_X - 1000, 1000)



# start_battle()

while True:
    if keyboard.is_pressed(']'): break
    start_battle()
    heros()
    
        






    
