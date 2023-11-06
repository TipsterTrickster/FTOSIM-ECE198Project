import pygame
import sys
from FTO import FTO
from controls import Controls
from stats import statis

# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
size = 3
fto = FTO(size)

run1 = statis(fto)

controls = Controls(fto, run1)

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


    statis.timer(run1,fto.state, screen) #this is for the timer itself
    statis.print(run1,screen) #this is to keep the log of past times on the screen


    pygame.display.flip()




pygame.quit()
