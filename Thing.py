import pygame as pg
from random import randint
import Game
import My as my


"""Предметы инвентаря"""


class Thing(pg.sprite.Sprite):
    def __init__(self, place):
        super().__init__(my.inventory.inventory)
        self.image = self.image
        x = place * Game.CELL_SIZE
        y = Game.H - Game.CELL_SIZE
        self.rect = self.image.get_rect().move(x, y)

    
class Apple(Thing):

    image = pg.image.load('data/inventory/apple.png')


class Knife(Thing):

    image = pg.image.load('data/inventory/knife/1.png')
    images = {1: pg.image.load('data/inventory/knife/1.png'),
              2: pg.image.load('data/inventory/knife/2.png'),
              3: pg.image.load('data/inventory/knife/3.png'),
              4: pg.image.load('data/inventory/knife/4.png'),
              5: pg.image.load('data/inventory/knife/5.png'),
              }

    def __init__(self, place):
        super().__init__(place)
        self.power = randint(1, 5)
        self.image = self.images[self.power]


class Heart(Thing):
    
    image = pg.image.load('data/inventory/heart.png')
