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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill("white")
    
    
    fto.display(screen)
#    fto.rRot()

    time.sleep(1)
    pygame.display.flip()




pygame.quit()