import pygame
from FTO import FTO
import pygame


class Controls():
    def __init__(self, FTO):
        self.fto = FTO
    
    def control(self):
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_i] and event.type == pygame.KEYDOWN:
                self.fto.rRot(1)