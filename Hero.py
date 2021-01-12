import pygame as pg
from random import randint
import Game
import Start
import My as my
from Help import cut, Invisible
from Thing import Apple, Knife, Heart
from Objects import Water
from Evil import Ghost
from Bullets import AppleBall


"""Герой"""


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

    speed = 0.1 * Game.CELL_SIZE
    
    def __init__(self):
        self.hand = None
        self.health = Game.MAX_HEALTH
        self.direction = 'D'
        self.step = 1
        self.run = False
        self.time = 0
        self.waitImage = 20

        super().__init__(my.player_group, my.all_sprites)
        self.image = Hero.image['D']
        self.x = Game.H_POS[0]
        self.y = Game.H_POS[1]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)

        self.checkPos()
        self.crHealth()

    def checkPos(self):
        # Уничтожение объектов в клетке героя
        objs = pg.sprite.spritecollide(self, my.objects, True)
        for obj in objs:
            my.all_sprites.remove(obj)

    def crHealth(self):
        # Создание здоровья
        self.lifes = [Life(self, i * 30) for i in range(self.health)]

    def addLife(self):
        # Добавление жизни
        if self.health < Game.MAX_HEALTH:
            self.lifes.append(Life(self, self.health * 30))
            self.health += 1
            return True

    def removeLifes(self, damage):
        # Удаление жизни
        damage = min(self.health, damage)
        for _ in range(damage):
            self.health -= 1
            my.player_group.remove(self.lifes[-1])
            self.lifes.pop(-1)
        if not self.health:
            Start.endGame()

    def move(self):
        # Действие
        self.hand = my.inventory.obj

        # Установка скорости
        speed = Hero.speed
        if my.pressed[pg.K_LSHIFT]:
            speed *= 2

        # Перемещение персонажа
        if my.pressed[pg.K_w] or my.pressed[pg.K_UP]:
            # Шаг вверх
            self.run = True
            self.direction = 'U'
            self.rect.y -= speed
            if self.cant():
                self.rect.y += speed
        if my.pressed[pg.K_s] or my.pressed[pg.K_DOWN]:
            # Шаг вниз
            self.run = True
            self.direction = 'D'
            self.rect.y += speed
            if self.cant():
                self.rect.y -= speed
        if my.pressed[pg.K_a] or my.pressed[pg.K_LEFT]:
            # Шаг влево
            self.run = True
            self.direction = 'L'
            self.rect.x -= speed
            if self.cant():
                self.rect.x += speed
        if my.pressed[pg.K_d] or my.pressed[pg.K_RIGHT]:
            # Шаг вправо
            self.run = True
            self.direction = 'R'
            self.rect.x += speed
            if self.cant():
                self.rect.x -= speed
        self.setImage()

    def setImage(self, fight=False):
        # Смена кадра анимации
        if fight:
            self.image = Hero.imageAttack[self.direction]
            self.time = 0
        elif self.run:
            if self.time == Game.TIME:
                self.image = Hero.imageRun[self.direction][self.step]
                self.step = (
                    self.step + 1) % len(Hero.imageRun[self.direction])
                self.time = 0
            else:
                self.time += 1
        else:
            if self.time == Game.TIME:
                self.image = Hero.image[self.direction]
                self.step = 0
                self.time = 0
            else:
                self.time += 1
        self.run = False

    def used(self):
        # Взаимодействие с объектом
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction, my.objects)
        print(obj)
        if obj:
            obj.do()

    def cant(self):
        # Проверка возможности перемещения в клетку
        obj = pg.sprite.spritecollideany(self, my.objects)
        evil = pg.sprite.spritecollideany(self, my.evil_group)
        return (obj or evil and
                pg.sprite.spritecollideany(self, my.evil_group).__class__ != Ghost)

    def do(self):
        # Использование предмета из инвентаря
        if not self.hand:
            return 0
        if self.hand.__class__ is Apple:
            my.inventory.remove(self.hand)
            AppleBall(self.direction)
        elif self.hand.__class__ is Knife:
            self.fight(self.hand.power)
            if randint(1, 10) == 1:
                my.inventory.remove(self.hand)
        elif self.hand.__class__ is Heart:
            if self.addLife():
                my.inventory.remove(self.hand)

    def fight(self, power):
        # Атака
        self.setImage(True)
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction, my.evil_group)
        if obj:
            obj.to_hurt(power)
        else:
            obj = inv.check(my.objects)
            if obj and obj.__class__ != Water:
                obj.death()


class Life(pg.sprite.Sprite):

    # Единица здоровья героя

    image = pg.image.load('data/heart.png')

    def __init__(self, hero, x):
        super().__init__(my.player_group)
        self.rect = self.image.get_rect().move(x, 0)

    def move(self):
        pass



    
