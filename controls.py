import pygame
from FTO import FTO
import pygame


class Controls():
    def __init__(self, FTO):
        self.fto = FTO
        self.key_mapping = {}
        with open('key_binds.txt', 'r') as file:
            for line in file:
                move,  key = line.strip().split(': ')
                self.key_mapping[key] = move

    def control(self, event):
        for key_name, move in self.key_mapping.items():
            key_code = getattr(pygame, key_name)
            if event.key == key_code:
                if "," in move:
                    move, layers = move.split(", ")
                    getattr(self.fto, move)(int(layers))
                else:
                    getattr(self.fto, move)()