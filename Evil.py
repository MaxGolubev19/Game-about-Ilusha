import pygame as pg


class Evil:
    def __init__(self, pos, field, screen):
        self.x, self.y = pos
        self.field = field
        self.screen = screen

        self.speed = 3
        self.disRun = 500
        self.disFight = 60
        self.color = 'blue'

        self.fight = False
        
    def draw(self, hPos, hDrawPos):
        hx, hy = hPos
        xSpace = hx - self.x
        ySpace = hy - self.y
        hx, hy = hDrawPos
        pos = self.field.w // 2 + xSpace, self.field.h // 2 + ySpace
        pg.draw.circle(self.screen, self.color, pos, 20)

    def moving(self, hPos):
        move, fight = self.check(hPos)
        if fight:
            self.startFight()
        else:
            self.endFight()
        if move:
            x, y = hPos
            sx = x - self.x
            sy = y - self.y
            sx0, sy0 = abs(sx), abs(sy)
            if sx:
                xSign = sx // sx0
                self.x += self.speed * xSign
            if sy:
                ySign = sy // sy0
                self.y += self.speed * ySign

    def check(self, hPos):
        x, y = hPos
        return (self.disFight < abs(self.x - x) <= self.disRun or
                self.disFight < abs(self.y - y) <= self.disRun,
                self.disFight >= abs(self.x - x) and
                self.disFight >= abs(self.y - y))

    def startFight(self):
        self.fight = True
        self.color = 'red'

    def endFight(self):
        self.fight = False
        self.color = 'blue'

    
