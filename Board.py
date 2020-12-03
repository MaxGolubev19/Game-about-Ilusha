import pygame as pg


class Board:
    def __init__(self, w, h, screen):
        self.w, self.h = w, h
        self.screen = screen
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.h):
            for x in range(self.w):
                self.drawCell(x, y)

    def get_click(self, mouse_pos):
        pass

    def drawCell(self, x, y):
        size = self.cell_size
        x = self.left + x * size
        y = self.top + y * size
        pg.draw.rect(self.screen, 'white', (x, y, size, size), 1)

    def get_cell(self, pos):
        x, y = pos
        x = (x - self.left) // self.cell_size
        y = (y - self.top) // self.cell_size
        if 0 > x or x + 1 > self.w or 0 > y or y + 1 > self.h:
            return None
        return (x, y)
