import pygame as pg
import random


class Board:
    def __init__(self, w, h, maxSize, cellSize, screen):
        self.screen = screen
        self.w, self.h = w, h
        self.left = -maxSize
        self.top = -maxSize
        self.cellSize = cellSize

    def render(self):
        x0 = -(abs(self.left) % self.cellSize)
        y0 = -(abs(self.top) % self.cellSize)
        for y in range(y0, self.h, self.cellSize):
            for x in range(x0, self.w, self.cellSize):
                self.drawCell(x, y)
                
    def drawCell(self, x, y):
        size = self.cellSize
        pg.draw.rect(self.screen, 'black', (x, y, size, size), 1)

    def getClick(self, newPos, myPos):
        x, y = newPos
        x0, y0 = myPos 
