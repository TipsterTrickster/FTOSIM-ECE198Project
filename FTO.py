import pygame

class FTO():
    def __init__(self):
        self.size = 3
        self.state = []
        self.colorScheme = ["#FFFFFF","#00FF2F","#FF0000","#FFFF00","#298FE8","#000000","#9D00FF","#FF7700"]
        

    def display(surface):
        pygame.draw.polygon(surface, "black", [(500,500), (250,250), (250, 500)])
    