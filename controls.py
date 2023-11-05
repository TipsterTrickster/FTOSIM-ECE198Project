import pygame
import random
from pathlib import Path




class Controls():
    def __init__(self, FTO, Stats):
        self.fto = FTO
        self.stats = Stats
        self.key_mapping = {}
        self.scrambling = False

        p = Path(__file__).with_name("key_binds.txt")
        with p.open('r') as file:
            for line in file:
                move,  key = line.strip().split(': ')
                self.key_mapping[key] = move

    def scramble(self): # method to scramble the puzzle using random moves
        self.stats.scramble = []
        self.stats.solution = []
        moves = ["R", "Rp", "U", "Up", "F", "Fp", "L", "Lp", "D", "Dp", "B", "Bp", "BL", "BLp", "BR", "BRp"]
        for i in range(self.fto.size * 20):
            move = random.choice(moves)
            layers = random.randint(1, self.fto.size // 2)
            getattr(self.fto, move)(layers)
            self.stats.scramble.append(move + str(layers))
        self.fto.scrambled = True

    def control(self, event): # controls for puzzle
        for key_name, move in self.key_mapping.items():
            if event.unicode == key_name:
                if "," in move:
                    move, layers = move.split(", ")
                    getattr(self.fto, move)(int(layers))
                    self.stats.movecount += 1
                    self.stats.solution.append(move + str(layers))
                    if self.fto.scrambled == True:
                        self.stats.started = 1
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
                    self.stats.solution.append(move)
    

