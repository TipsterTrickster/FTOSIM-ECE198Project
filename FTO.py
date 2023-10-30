import pygame
from math import sin, cos, pi

class FTO():
    def __init__(self, size):
        self.puzzleSize = 50
        self.size = size
        self.state = [[i] * self.size ** 2 for i in range(8)]
        # Color Scheme: U F R L B D BR BL
        self.colorScheme = ["#FFFFFF","#00FF2F","#FF0000","#FFFF00","#298FE8","#000000","#9D00FF","#FF7700"]

    # orientation, 0 -> U, 1 -> D, 2 -> R, 3 -> L where triangle starts at point and goes in orientation directon
    def triangle(self, surface, x, y, size, orientation, color): # general method for drawing triangles to screen
        width = 10 # triangle border width
        sizex = size - width*cos((22.5 * pi) / 180) # sizes for triangle color
        sizey = size - width*sin((22.5 * pi) / 180)

        if orientation == 0:
            pygame.draw.polygon(surface, "Black", [(x, y), (x - size, y - size), (x + size, y - size)])
            pygame.draw.polygon(surface, color, [(x, y - width/2), (x - sizex, y - sizey), (x + sizex, y - sizey)])
        elif orientation == 1:
            pygame.draw.polygon(surface, "Black", [(x, y), (x + size, y + size), (x - size, y + size)])
            pygame.draw.polygon(surface, color, [(x, y + width/2), (x + sizex, y + sizey), (x - sizex, y + sizey)])
        elif orientation == 2:
            pygame.draw.polygon(surface, "Black", [(x, y), (x + size, y - size), (x + size, y + size)])
            pygame.draw.polygon(surface, color, [(x + width/2, y), (x + sizey, y - sizex), (x + sizey, y + sizex)])
        elif orientation == 3:
            pygame.draw.polygon(surface, "Black", [(x, y), (x - size, y + size), (x - size, y - size)])
            pygame.draw.polygon(surface, color, [(x - width/2, y), (x - sizey, y + sizex), (x - sizey, y - sizex)])
        else:
            raise "Invalid orientation"

    def display(self, surface):
        x = surface.get_width() // 2
        y = surface.get_height() // 2
        size = self.puzzleSize

        for w in range(2):
            face = 0
            n = 0
            for j in range(self.size):
                for i, k in zip(range(-j, j + 1), range(j * 2 + 1)):
                    self.triangle(surface, x + i * size, y - j * size - size * (k % 2) + size * self.size * w * 2, size, k % 2, self.colorScheme[self.state[face + w * 5][n]])
                    n += 1

            face = 1
            n = 0
            for j in range(self.size):
                for i, k in zip(range(j, -j - 1, -1), range(j * 2 + 1)):
                    self.triangle(surface, x + i * size, y + j * size + size * (k % 2) - size * self.size * w * 2, size, not(k % 2), self.colorScheme[self.state[face + w * 3][n]])
                    n += 1

            face = 2
            n = 0
            for j in range(self.size):
                for i, k in zip(range(-j, j + 1), range(j * 2 + 1)):
                    self.triangle(surface, x + j * size + size * (k % 2) - size * self.size * w * 2, y - i * size, size, 2 + k % 2, self.colorScheme[self.state[face + w * 5][n]])
                    n += 1

            face = 3
            n = 0
            for j in range(self.size):
                for i, k in zip(range(j, -j - 1, -1), range(j * 2 + 1)):
                    self.triangle(surface, x - j * size - size * (k % 2) + size * self.size * w * 2, y - i * size, size, 3 if k % 2 == 0 else 2, self.colorScheme[self.state[face + w * 3][n]])
                    n += 1

    # MOVES BELOW

    # 0 1 2 3 4 5  6 7
    # U F R L B D BR BL
    """
    T / flip over to get to other faces
      5 6 7 8 9
        2 3 4    
          1
    """
    def rRot(self):
        size = self.size
        c2 = (size - 1) ** 2
        c3 = (size ** 2) - 1

        f1 = 0
        f2 = 1
        f3 = 6
        
        for j, k in zip(range(0, self.size), range(self.size - 1, -1, -1)):
            buff = self.state[f1][((j + 1) ** 2) - 1]
            self.state[f1][((j + 1) ** 2) - 1] = self.state[f2][k ** 2]
            self.state[f2][k ** 2] = self.state[f3][c2 + 2 * k]
            self.state[f3][c2 + 2 * k] = buff
        
        for j, k in zip(range(1, self.size), range(self.size - 1, 0, -1)):
            buff = self.state[f1][((j + 1) ** 2) - 2]
            self.state[f1][((j + 1) ** 2) - 2] = self.state[f2][(k ** 2) + 1]
            self.state[f2][(k ** 2) + 1] = self.state[f3][c2 + 2 * k - 1]
            self.state[f3][c2 + 2 * k - 1] = buff
        
        buff = self.state[3][0]
        self.state[3][0] = self.state[5][c3]
        self.state[5][c3] = self.state[4][c2]
        self.state[4][c2] = buff

        for j, k in zip(range(0, self.size), range(self.size - 1, -1, -1)):
            buff = self.state[f1][((j + 1) ** 2) - 1]
            self.state[f1][((j + 1) ** 2) - 1] = self.state[f2][k ** 2]
            self.state[f2][k ** 2] = self.state[f3][c2 + 2 * k]
            self.state[f3][c2 + 2 * k] = buff
        
        for j, k in zip(range(1, self.size), range(self.size - 1, 0, -1)):
            buff = self.state[f1][((j + 1) ** 2) - 2]
            self.state[f1][((j + 1) ** 2) - 2] = self.state[f2][(k ** 2) + 1]
            self.state[f2][(k ** 2) + 1] = self.state[f3][c2 + 2 * k - 1]
            self.state[f3][c2 + 2 * k - 1] = buff


        # 0 4 8
        # 0 9 15 # corner
        # 0 16 24
        
        # 1 6 3 
        # 1 11 8 # edge
        # 4 13 3

        # 1 18 15
        # 4 20 8
        # 9 22 3

        # 2 5 7
        # 2 10 14 # triangle
        # 5 12 7

        # 2 17 30
        # 5 19 14
        # 10 21 7

        # 6
        # 12
        # 6 11 13