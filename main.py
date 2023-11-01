import pygame
import numpy as np
import pandas as pd
import time
import sys
from FTO import FTO
from controls import Controls
import stats
import scrambler


# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
fto = FTO(3)
controls = Controls(fto)
baseLayer = 1

run1 = stats.statis()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if pygame.key.get_pressed()[pygame.K_i] and event.type == pygame.KEYDOWN:
            fto.rRot(baseLayer)

    print(fto.state)
    screen.fill("white")
    fto.display(screen)

    pygame.display.flip()
#    fto.rRot()
    #this is for the timer itself
    stats.statis.timer(run1,screen)
    #this is to keep the log of past times on the screen
    stats.statis.print(run1,screen)
    #not sure how important this sleep is here, but it seems to make the timer not work as well because it doesn't loop as fast, so the responsiveness for noticing a press isn't there
    time.sleep(1)
    pygame.display.flip()




pygame.quit()
