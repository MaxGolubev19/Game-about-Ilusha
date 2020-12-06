import pygame as pg


class Hero:
    def __init__(self, pos, field, screen):
        self.drawPos = pos
        self.x, self.y = 0, 0
        self.field = field
        self.screen = screen
        
        self.speed = 5
        self.cSpeed = 1
        self.color = 'yellow'
        
        self.endMoving()

    def getPos(self):
        return (self.x, self.y)

    def draw(self):
        pg.draw.circle(self.screen, self.color, self.drawPos, 20)        

    def moving(self, pressed):
        self.edMove(pressed)
        step = self.speed * self.cSpeed
        if pressed[pg.K_w] or pressed[pg.K_UP]:
            self.moveUp(step)
        elif pressed[pg.K_s] or pressed[pg.K_DOWN]:
            self.moveDown(step)
        elif pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.moveLeft(step)
        elif pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.moveRight(step)
        if self.auto:
            self.autoMoving()

    def moveUp(self, step):
        self.field.top += step
        self.y -= step
        self.endMoving()

    def moveDown(self, step):
        self.field.top -= step
        self.y += step
        self.endMoving()

    def moveLeft(self, step):
        self.field.left += step
        self.x -= step
        self.endMoving()

    def moveRight(self, step):
        self.field.left -= step
        self.x += step
        self.endMoving()

    def edMove(self, pressed):
        if pressed[pg.K_LSHIFT]:
            self.cSpeed = 2
        else:
            self.cSpeed = 1

    def startMoving(self, pos):
        self.auto = True
        x0, y0 = self.drawPos
        x, y = pos
        sx = x0 - x
        sy = y0 - y
        sx0, sy0 = abs(sx), abs(sy)
        self.time = max(sx0, sy0) // self.speed
        if sx:
            xSign = sx // sx0
            self.xStep = sx0 // self.time * xSign
            self.xEnd = sx0 % self.time * xSign
        if sy:
            ySign = sy // sy0
            self.yStep = sy0 // self.time * ySign
            self.yEnd = sy0 % self.time * ySign
        
    def endMoving(self):
        self.auto = False
        self.time = 0
        self.stepX = 0
        self.xEnd = 0
        self.stepY = 0
        self.yEnd = 0        

    def autoMoving(self):
        if self.time > 0:
            self.field.left += self.xStep * self.cSpeed
            self.field.top += self.yStep * self.cSpeed
            self.x += self.xStep * self.cSpeed
            self.y += self.yStep * self.cSpeed
            self.time -= self.cSpeed
        else:
            self.field.left += self.xEnd
            self.x += self.xEnd
            self.field.top -= self.yEnd
            self.y += self.yEnd
            self.endMoving()

















            
