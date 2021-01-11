import pygame as pg
from random import randint
from Start import my, cut
from Objects import Apple, knifes, Heart, Water
from Evil import Ghost


class Hero(pg.sprite.Sprite):
    image = {'R': pg.image.load('data/hero/right.png'),
             'L': pg.image.load('data/hero/left.png'),
             'U': pg.image.load('data/hero/up.png'),
             'D': pg.image.load('data/hero/down.png'),
             }

    imageRun = {'R': cut(pg.image.load('data/hero/rightRun.png')),
                'L': cut(pg.image.load('data/hero/leftRun.png')),
                'U': cut(pg.image.load('data/hero/upRun.png')),
                'D': cut(pg.image.load('data/hero/downRun.png')),
                }

    imageAttack = {'R': pg.image.load('data/hero/rightAttack.png'),
                   'L': pg.image.load('data/hero/leftAttack.png'),
                   'U': pg.image.load('data/hero/up.png'),
                   'D': pg.image.load('data/hero/down.png'),
                   }

    def __init__(self):
        self.speed = 0.1
        self.hand = None
        self.health = my.maxHealth
        self.direction = 'D'
        self.step = 1
        self.run = False
        self.time = 0
        self.waitImage = 20

        super().__init__(my.player_group, my.all_sprites)
        self.image = Hero.image['D']
        self.x = my.hPos[0]
        self.y = my.hPos[1]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)

        self.checkPos()
        self.crHealth()
        self.endAutoMoving()

    def checkPos(self):
        objs = pg.sprite.spritecollide(self, my.objects, True)
        for obj in objs:
            my.all_sprites.remove(obj)

    def crHealth(self):
        self.lifes = [Life(self, i * 30) for i in range(self.health)]

    def addLife(self):
        if self.health < my.maxHealth:
            self.lifes.append(Life(self, self.health * 30))
            self.health += 1
            return True

    def removeLifes(self, damage):
        damage = min(self.health, damage)
        for _ in range(damage):
            self.health -= 1
            my.player_group.remove(self.lifes[-1])
            self.lifes.pop(-1)
        if not self.health:
            my.endGame()

    def move(self):
        if self.auto:
            self.autoMoving()
            return 0
        self.hand = my.inv.obj

        # Установка скорости
        speed = self.speed
        if my.pressed[pg.K_LSHIFT]:
            speed *= 2

        # Перемещение персонажа
        if my.pressed[pg.K_w] or my.pressed[pg.K_UP]:
            self.run = True
            self.direction = 'U'
            self.rect.y -= my.cellSize * speed
            if self.cant():
                self.rect.y += my.cellSize * speed
        elif my.pressed[pg.K_s] or my.pressed[pg.K_DOWN]:
            self.run = True
            self.direction = 'D'
            self.rect.y += my.cellSize * speed
            if self.cant():
                self.rect.y -= my.cellSize * speed
        elif my.pressed[pg.K_a] or my.pressed[pg.K_LEFT]:
            self.run = True
            self.direction = 'L'
            self.rect.x -= my.cellSize * speed
            if self.cant():
                self.rect.x += my.cellSize * speed
        elif my.pressed[pg.K_d] or my.pressed[pg.K_RIGHT]:
            self.run = True
            self.direction = 'R'
            self.rect.x += my.cellSize * speed
            if self.cant():
                self.rect.x -= my.cellSize * speed
        self.setImage()

    def setImage(self, fight=False):
        if fight:
            self.image = Hero.imageAttack[self.direction]
            self.time = 0
        elif self.run:
            if self.time == my.time:
                self.image = Hero.imageRun[self.direction][self.step]
                self.step = (
                    self.step + 1) % len(Hero.imageRun[self.direction])
                self.time = 0
            else:
                self.time += 1
        else:
            if self.time == my.time:
                self.image = Hero.image[self.direction]
                self.step = 0
                self.time = 0
            else:
                self.time += 1
        self.run = False

    def autoMoving(self):
        if self.time > 0:
            xStep = self.xStep
            yStep = self.yStep
        else:
            xStep = self.xEnd
            yStep = self.yEnd
        self.rect.x -= xStep
        self.rect.y -= yStep
        if self.cant():
            self.rect.x += self.xStep
            self.rect.y += self.yStep
            self.endAutoMoving()
        if not self.time:
            self.endAutoMoving()

    def startAutoMoving(self, x, y):
        self.auto = True
        sx = my.hPos[0] - x
        sy = my.hPos[1] - y
        sx0, sy0 = abs(sx), abs(sy)
        self.time = int(max(sx0, sy0) / (self.speed * my.cellSize))
        if sx:
            xSign = sx // sx0
            self.xStep = (sx0 // self.time) * xSign
            self.xEnd = (sx0 % self.time) * xSign
        if sy:
            ySign = sy // sy0
            self.yStep = (sy0 // self.time) * ySign
            self.yEnd = (sy0 % self.time) * ySign

    def endAutoMoving(self):
        self.auto = False
        self.time = 0
        self.stepX = 0
        self.xEnd = 0
        self.stepY = 0
        self.yEnd = 0

    def used(self):
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction)
        print(obj)
        if obj:
            obj.do()

    def cant(self):
        obj = pg.sprite.spritecollideany(self, my.objects)
        evil = pg.sprite.spritecollideany(self, my.evil_group)
        return (obj or evil and pg.sprite.spritecollideany(self, my.evil_group).__class__ != Ghost)

    def do(self):
        if not self.hand:
            return 0
        if self.hand.__class__ is Apple:
            my.inv.remove(self.hand)
            AppleBall(self.direction)
        elif self.hand.__class__ in knifes:
            self.fight(self.hand.power)
            if randint(1, 10) == 1:
                my.inv.remove(self.hand)
        elif self.hand.__class__ is Heart:
            if self.addLife():
                my.inv.remove(self.hand)

    def fight(self, power):
        self.setImage(True)
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction)
        if obj in my.evil_group:
            obj.to_hurt(power)
        elif obj and obj.__class__ != Water:
            obj.trash()


class Life(pg.sprite.Sprite):

    image = pg.image.load('data/heart.png')

    def __init__(self, hero, x):
        super().__init__(my.player_group)
        self.rect = self.image.get_rect().move(x, 0)

    def move(self):
        pass


class Invisible(pg.sprite.Sprite):

    image = pg.image.load('data/grass.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = Invisible.image
        self.x = x
        self.y = y

    def search(self, direction, group=my.objects):
        if direction == 'U':
            self.y -= my.cellSize
        elif direction == 'D':
            self.y += my.cellSize
        elif direction == 'R':
            self.x += my.cellSize
        elif direction == 'L':
            self.x -= my.cellSize
        return self.check(group)

    def check(self, group):
        self.rect = self.image.get_rect().move(self.x, self.y)
        return pg.sprite.spritecollideany(self, group)


class AppleBall(pg.sprite.Sprite):

    image = pg.image.load('data/apple.png')

    def __init__(self, direction):
        super().__init__(my.player_group, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(my.hPos)
        self.direction = direction
        self.speed = 0.2
        self.damage = 1

    def move(self):
        if self.direction == 'U':
            self.rect.y -= self.speed * my.cellSize
        elif self.direction == 'D':
            self.rect.y += self.speed * my.cellSize
        elif self.direction == 'R':
            self.rect.x += self.speed * my.cellSize
        elif self.direction == 'L':
            self.rect.x -= self.speed * my.cellSize

        obj = pg.sprite.spritecollideany(self, my.evil_group)
        if obj:
            obj.to_hurt(self.damage)
        else:
            obj = pg.sprite.spritecollideany(self, my.objects)
        if obj:
            self.trash()

    def trash(self):
        my.player_group.remove(self)
        my.all_sprites.remove(self)
