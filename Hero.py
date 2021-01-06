import pygame as pg
from Start import my


class Hero(pg.sprite.Sprite):

    image = pg.image.load('data/hero.png')
    
    def __init__(self):
        super().__init__(my.player_group, my.all_sprites)
        self.image = Hero.image
        self.x = my.hPos[0]
        self.y = my.hPos[1]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.speed = 0.1

    def move(self):
        # Получение команд клавиатуры
        pressed = pg.key.get_pressed()

        # Установка скорости
        speed = self.speed
        if pressed[pg.K_LSHIFT]:
            speed *= 2

        # Перемещение персонажа
        if pressed[pg.K_w] or pressed[pg.K_UP]:
            self.rect.y -= my.cellSize * speed
        if pressed[pg.K_s] or pressed[pg.K_DOWN]:
            self.rect.y += my.cellSize * speed
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.rect.x -= my.cellSize * speed
        if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.rect.x += my.cellSize * speed

    """            
    def startMoving(self, pos, speed):
        self.auto = True
        x, y = pos
        sx = x - self.rect.x
        sy = y - self.rect.y
        sx0, sy0 = abs(sx), abs(sy)
        self.time = max(sx0, sy0) // speed
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
        self.xStep = 0
        self.xEnd = 0
        self.yStep = 0
        self.yEnd = 0        

    def autoMoving(self):
        if self.time > 0:
            self.field.left -= self.xStep * self.cSpeed
            self.field.top -= self.yStep * self.cSpeed
            self.rect.x += self.xStep * self.cSpeed
            self.rect.y += self.yStep * self.cSpeed
            self.time -= self.cSpeed
        else:
            self.field.left += self.xEnd
            self.field.top -= self.yEnd
            self.rect.x += self.xEnd
            self.rect.y += self.yEnd
            self.endMoving()
    """















            
