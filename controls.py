import pygame
import random
from pathlib import Path
from stats import statis




class Controls():
    def __init__(self, FTO):
        self.fto = FTO
        self.key_mapping = {}
        self.scrambling = False

        p = Path(__file__).with_name("key_binds.txt")
        with p.open('r') as file:
            for line in file:
                move,  key = line.strip().split(': ')
                self.key_mapping[key] = move

    def scramble(self): # method to scramble the puzzle using random moves
        moves = ["R", "Rp", "U", "Up", "F", "Fp", "L", "Lp", "D", "Dp", "B", "Bp", "BL", "BLp", "BR", "BRp"]
        for i in range(self.fto.size * 20):
            getattr(self.fto, random.choice(moves))(random.randint(1, self.fto.size // 2))
            print(i)

    def control(self, event): # controls for puzzle
        for key_name, move in self.key_mapping.items():
            key_code = getattr(pygame, key_name)
            if event.key == key_code:
                if "," in move:
                    move, layers = move.split(", ")
                    getattr(self.fto, move)(int(layers))
                elif "scramble" in move:
                    if not self.scrambling:
                        self.scrambling = True
                        self.scramble()
                elif "increase_size" in move:
                    self.fto.size += 1
                elif "decrease_size" in move:
                    self.fto.size -= 1
                else:
                    getattr(self.fto, move)()
    

