import pygame as pg
from random import randint, choice
import Game
import My as my
from Thing import Apple, Knife, Heart


"""Объекты"""


class Object(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.objects, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(x * Game.CELL_SIZE,
                                               y * Game.CELL_SIZE)

    def do(self):
        # Взаимодействие с объектом
        pass

    def death(self):
        # Уничтожение объекта
        my.objects.remove(self)
        my.all_sprites.remove(self)
        

class Water(Object):

    image = pg.image.load('data/water.png')

        
class Tree(Object):

    image = pg.image.load('data/tree/with_apples.png')
    imageUsed = pg.image.load('data/tree/without_apples.png')

    def __init__(self, x, y):
        super().__init__(x, y)
        self.apples = True

    def do(self):
        # Взаимодействие с объектом
        if not self.apples:
            return 0
        self.apples = False
        self.image = Tree.imageUsed
        count = randint(1, 10)
        for _ in range(count):
            my.inventory.append(Apple)


class Stone(Object):

    image = pg.image.load('data/stone.png')


class Chest(Object):

    image = pg.image.load('data/chest/closed.png')
    imageUsed = pg.image.load('data/chest/open.png')
    objects = [Apple, Knife, Heart]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.closed = True

    def do(self):
        # Взаимодействие с объектом
        if not self.closed:
            return 0
        self.closed = False
        self.image = Chest.imageUsed
        count = randint(1, 5)
        for _ in range(count):
            name = choice(Chest.objects)
            my.inventory.append(name)

            
