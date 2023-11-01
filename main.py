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

    screen.fill("white")
    fto.display(screen)

#    fto.rRot()
    #this is for the timer itself
    stats.statis.timer(run1,0, screen)
    #this is to keep the log of past times on the screen
    stats.statis.print(run1,screen)


    pygame.display.flip()




pygame.quit()
