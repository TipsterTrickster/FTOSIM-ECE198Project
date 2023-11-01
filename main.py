import pygame
import numpy as np
import pandas as pd
import time
import sys
from FTO import FTO
import controls
import stats
import scrambler


# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
fto = FTO(3)
run1 = stats.statis()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill("white")
    
    
    fto.display(screen)
#    fto.rRot()
    #this is for the timer itself
    stats.statis.timer(run1,screen)
    #this is to keep the log of past times on the screen
    stats.statis.print(run1,screen)
    #not sure how important this sleep is here, but it seems to make the timer not work as well because it doesn't loop as fast, so the responsiveness for noticing a press isn't there
    #without the sleep, the timer works relatively well besides instantly resetting the timer to zero after you finish a solve. 
    time.sleep(1)
    pygame.display.flip()




pygame.quit()
