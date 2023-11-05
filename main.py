import pygame
import numpy as np
import pandas as pd
import time
import sys
from FTO import FTO
from controls import Controls
import stats

# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
# pygame.key.set_repeat(400,1000)
size = 3
fto = FTO(size)
controls = Controls(fto)

run1 = stats.statis()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            try:
                controls.control(event)
            except:
                print("Invalid Move Mapping")

    controls.scrambling = False

    screen.fill("white")
    fto.display(screen)

    # #this is for the timer itself
    # stats.statis.timer(run1,0, screen)
    # #this is to keep the log of past times on the screen
    # stats.statis.print(run1,screen)


    pygame.display.flip()




pygame.quit()
