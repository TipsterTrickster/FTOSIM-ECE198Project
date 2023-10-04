import pygame
import numpy as np
import pandas as pd
import sys
from FTO import FTO
import controls
import stats
import scrambler


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.fill("white")
    FTO.display(screen)


    pygame.display.flip()




pygame.quit()