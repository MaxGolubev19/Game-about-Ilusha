import pygame as pg
from random import randint, choice
from Start import my


class Thing(pg.sprite.Sprite):
    def __init__(self, inv, args):
        super().__init__(my.inventory)
        if inv:
            self.image = self.imageInv
            x = args[0] * my.cellSize
            y = my.h - my.invSize
        else:
            self.image = self.image
            x, y = args
        self.rect = self.image.get_rect().move(x, y)

    
class Apple(Thing):

    image = pg.image.load('data/stone.png')
    imageInv = pg.image.load('data/stone.png')

    def __init__(self, *args, inv=False):
        super().__init__(inv, args)
        

class Apple2(Thing):

    image = pg.image.load('data/tree.png')
    imageInv = pg.image.load('data/tree.png')

    def __init__(self, *args, inv=False):
        super().__init__(inv, args)


class Apple3(Thing):

    image = pg.image.load('data/water.png')
    imageInv = pg.image.load('data/water.png')

    def __init__(self, *args, inv=False):
        super().__init__(inv, args)
        
        
class Object(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.objects, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(x * my.cellSize, y * my.cellSize)

    def do(self):
        print(self.__class__)
        

class Water(Object):

    image = pg.image.load('data/water.png')

        
class Tree(Object):

    image = pg.image.load('data/tree.png')


class Stone(Object):

    image = pg.image.load('data/stone.png')


class Chest(Object):

    image = pg.image.load('data/chest/closed.png')
    image2 = pg.image.load('data/chest/open.png')
    objects = [Apple, Apple2, Apple3]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.closed = True

    def do(self):
        if not self.closed:
            return 0
        self.closed = False
        self.image = Chest.image2
        count = randint(0, 10)
        for _ in range(count):
            my.inv.append(choice(Chest.objects))
    
            
