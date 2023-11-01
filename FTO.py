import pygame
from math import sin, cos, pi

class FTO():
    def __init__(self, size):
        self.puzzleSize = 150 / (size)
        self.size = size
        self.state = [[i] * self.size ** 2 for i in range(8)]
        # Color Scheme: U F R L B D BR BL
        self.colorScheme = ["#FFFFFF","#00FF2F","#FF0000","#FFFF00","#298FE8","#000000","#9D00FF","#FF7700"]


    # orientation, 0 -> U, 1 -> D, 2 -> R, 3 -> L where triangle starts at point and goes in orientation directon
    def triangle(self, surface, x, y, size, orientation, color): # general method for drawing triangles to screen
        width = 30 / self.size # triangle border width
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
      4 5 6 7 8
        1 2 3    
          0
    """
    def rRot(self, layers):
        size = self.size

        f1 = 0
        f2 = 1
        f3 = 6


        for n in range(layers * 2):    
            for j, k in zip(range((n + 1) // 2, size), range(size - 1, (n + 1) // 2 - 1, -1)):
                buff = self.state[f1][((j + 1) ** 2) - (n + 1)]
                self.state[f1][((j + 1) ** 2) - (n + 1)] = self.state[f2][k ** 2 + n]
                self.state[f2][k ** 2 + n] = self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * j - n]
                self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * j - n] = buff


        f4 = 3
        f5 = 5
        f6 = 4

        for j in range(0, layers):
            for i, k in zip(range(j + 1), range(j, -1, -1)):
                buff = self.state[f4][((j + 1) ** 2 - 1) - i * 2]
                self.state[f4][((j + 1) ** 2 - 1) - i * 2] = self.state[f5][(size - j + i) ** 2 - (2 * i + 1)]
                self.state[f5][(size - j + i) ** 2 - (2 * i + 1)] = self.state[f6][(size - 1 - j + i) ** 2 + 2 * i]
                self.state[f6][(size - 1 - j + i) ** 2 + 2 * i] = buff
                if i > 0 and j > 0:
                    buff = self.state[f4][((j + 1) ** 2 - 1) - i * 2 + 1]
                    self.state[f4][((j + 1) ** 2 - 1) - i * 2 + 1] = self.state[f5][(size - j + i) ** 2 - (2 * i + 1) + 1]
                    self.state[f5][(size - j + i) ** 2 - (2 * i + 1) + 1] = self.state[f6][(size - 1 - j + i) ** 2 + 2 * i - 1]
                    self.state[f6][(size - 1 - j + i) ** 2 + 2 * i - 1] = buff


        f1 = f2 = f3 = 2
        for n in range((size // 2) * 2):    
            for j, k in zip(range((n + 1) // 2, size), range(size - 1, (n + 1) // 2 - 1, -1)):
                buff = self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * k - n]
                self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * k - n] = self.state[f2][k ** 2 + n]
                self.state[f2][k ** 2 + n] = self.state[f1][((j + 1) ** 2) - (n + 1)]
                self.state[f1][((j + 1) ** 2) - (n + 1)] = buff
        
        if size % 2:
            buff = self.state[f1][(size // 2) ** 2]
            self.state[f1][(size // 2) ** 2] = self.state[f1][(size // 2 + 1) ** 2 - 1]
            self.state[f1][(size // 2 + 1) ** 2 - 1] = self.state[f1][(size - 1) ** 2 + (size - 1)]
            self.state[f1][(size - 1) ** 2 + (size - 1)] = buff

        else:
            buff = self.state[f1][(size // 2) ** 2 + 1]
            self.state[f1][(size // 2) ** 2 + 1] = self.state[f1][(size // 2 + 1) ** 2 - 2]
            self.state[f1][(size // 2 + 1) ** 2 - 2] = self.state[f1][(size - 1) ** 2 + (size - 1)]
            self.state[f1][(size - 1) ** 2 + (size - 1)] = buff

        if layers == size:
            f1 = f2 = f3 = 7
            for n in range((size // 2) * 2):    
                for j, k in zip(range((n + 1) // 2, size), range(size - 1, (n + 1) // 2 - 1, -1)):
                    buff = self.state[f1][((j + 1) ** 2) - (n + 1)]
                    self.state[f1][((j + 1) ** 2) - (n + 1)] = self.state[f2][k ** 2 + n]
                    self.state[f2][k ** 2 + n] = self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * k - n]
                    self.state[f3][((size - (n + 2) // 2) ** 2) + 2 * k - n] = buff
            
            if size % 2:
                buff = self.state[f1][(size - 1) ** 2 + (size - 1)]
                self.state[f1][(size - 1) ** 2 + (size - 1)] = self.state[f1][(size // 2 + 1) ** 2 - 1]
                self.state[f1][(size // 2 + 1) ** 2 - 1] = self.state[f1][(size // 2) ** 2]
                self.state[f1][(size // 2) ** 2] = buff

            else:
                buff = self.state[f1][(size - 1) ** 2 + (size - 1)]
                self.state[f1][(size - 1) ** 2 + (size - 1)] = self.state[f1][(size // 2 + 1) ** 2 - 2]
                self.state[f1][(size // 2 + 1) ** 2 - 2] = self.state[f1][(size // 2) ** 2 + 1]
                self.state[f1][(size // 2) ** 2 + 1] = buff

    def roRot(self):
        self.rRot(self.size)
    
    def tRot(self):
        for j in range(self.size):
            for i in range(j * 2 + 1):
                buff = self.state[0][(j ** 2) + i]
                self.state[0][(j ** 2) + i] = self.state[3][((j + 1) ** 2) - (i + 1)]
                self.state[3][((j + 1) ** 2) - (i + 1)] = self.state[1][(j ** 2) + i]
                self.state[1][(j ** 2) + i] = self.state[2][((j + 1) ** 2) - (i + 1)]
                self.state[2][((j + 1) ** 2) - (i + 1)] = buff

                buff = self.state[4][(j ** 2) + i]
                self.state[4][(j ** 2) + i] = self.state[7][((j + 1) ** 2) - (i + 1)]
                self.state[7][((j + 1) ** 2) - (i + 1)] = self.state[5][(j ** 2) + i]
                self.state[5][(j ** 2) + i] = self.state[6][((j + 1) ** 2) - (i + 1)]
                self.state[6][((j + 1) ** 2) - (i + 1)] = buff

    def uRot(self, layers):
        self.tRot()
        self.rRot(layers)
        self.tRot()
        self.tRot()
        self.tRot()
