import pygame as pg
import random


class Field:
    def __init__(self, size, maxSize, cellSize, screen):
        self.screen = screen
        self.w, self.h = size
        self.left = -maxSize
        self.top = -maxSize
        self.cellSize = cellSize

    def render(self):
        self.screen.fill('green')
        x0 = -(abs(self.left) % self.cellSize)
        y0 = -(abs(self.top) % self.cellSize)
        for y in range(y0, self.h, self.cellSize):
            for x in range(x0, self.w, self.cellSize):
                self.drawCell(x, y)
                
    def drawCell(self, x, y):
        size = self.cellSize
        pg.draw.rect(self.screen, 'black', (x, y, size, size), 1)
