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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if pygame.key.get_pressed()[pygame.K_i] and event.type == pygame.KEYDOWN:
            fto.rRot(baseLayer)

    print(fto.state)
    screen.fill("white")
    fto.display(screen)

    pygame.display.flip()