import pygame as pg
from Start import my


class Object(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.objects, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(x * my.cellSize, y * my.cellSize)

    def do(self):
        print('do!')
        

class Water(Object):

    image = pg.image.load('data/water.png')

        
class Tree(Object):

    image = pg.image.load('data/tree.png')


class Stone(Object):

    image = pg.image.load('data/stone.png')


class Chest(Object):

    image = pg.image.load('data/chest.png')
    image2 = pg.image.load('data/chest_open.png')

    def do(self):
        print('open')
        self.image = Chect.image2
