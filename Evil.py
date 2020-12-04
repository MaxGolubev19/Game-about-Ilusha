import pygame as pg


class Evil:
    def __init__(self, pos, field, screen):
        self.x, self.y = pos
        self.field = field
        self.screen = screen

        self.speed = 3
        self.distance = 200
        
    def draw(self, hPos, hDrawPos):
        hx, hy = hPos
        xSpace = hx - self.x
        ySpace = hy - self.y
        hx, hy = hDrawPos
        pos = hx - xSpace, hy - ySpace
        pg.draw.circle(self.screen, 'yellow', pos, 20)

    def moving(self, hPos):
        x, y = hPos
        if abs(self.x - x) <= self.distance or abs(self.y - y) <= self.distance:
            sx = x - self.x
            sy = y - self.y
            sx0, sy0 = abs(sx), abs(sy)
            if sx:
                xSign = sx // sx0
                self.x += self.speed * xSign
            if sy:
                ySign = sy // sy0
                self.y += self.speed * ySign
