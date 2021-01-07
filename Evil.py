import pygame as pg
from Start import my


class Pig(pg.sprite.Sprite):

    image = pg.image.load('data/pig/right.png')
    imageRight = pg.image.load('data/pig/right.png')
    imageLeft = pg.image.load('data/pig/left.png')
    imageAttackRight = pg.image.load('data/pig/rightAttack.png')
    imageAttackLeft = pg.image.load('data/pig/leftAttack.png')
    imageDied = pg.image.load('data/pig/rightDied.png')    
    
    def __init__(self):
        super().__init__(my.evil_group, my.all_sprites)
        self.image = Pig.image
        self.x = my.hPos[0] + 100
        self.y = my.hPos[1] + 100
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.speed = 0.09 * my.cellSize
        self.disFight = 2 * my.cellSize

    def move(self):
        if self.checkFight():
            my.fight = True
            self.fight()
        else:
            my.fight = False
            self.moving()
            
    def checkFight(self):
        return (self.disFight >= abs(self.rect.x - my.hPos[0]) and
                self.disFight >= abs(self.rect.y - my.hPos[1]))

    def moving(self):
        x, y = my.hPos
        if y > self.rect.y:
            self.rect.y += self.speed
        if y < self.rect.y:
            self.rect.y -= self.speed
        if x > self.rect.x:
            self.image = Pig.imageRight
            self.rect.x += self.speed
        if x < self.rect.x:
            self.image = Pig.imageLeft
            self.rect.x -= self.speed

    def fight(self):
        x, y = my.hPos
        if (abs(self.rect.x - x) < my.cellSize and
            abs(self.rect.y - y) < my.cellSize):
            print('Oy')
            return
            
        if y > self.rect.y:
            self.rect.y += self.speed * 2
        if y < self.rect.y:
            self.rect.y -= self.speed * 2
        if x > self.rect.x:
            self.image = Pig.imageAttackRight
            self.rect.x += self.speed * 2
        if x < self.rect.x:
            self.image = Pig.imageAttackLeft
            self.rect.x -= self.speed * 2
    
