import pygame as pg
from random import randint, choice
from Start import my


class Thing(pg.sprite.Sprite):
    def __init__(self, place):
        super().__init__(my.inventory)
        self.image = self.image
        x = place * my.cellSize
        y = my.h - my.invSize
        self.rect = self.image.get_rect().move(x, y)

    
class Apple(Thing):
    
    image = pg.image.load('data/inventory/apple.png')

class Knife1(Thing):
    
    image = pg.image.load('data/inventory/knife/1.png')
    power = 1

class Knife2(Thing):
    
    image = pg.image.load('data/inventory/knife/2.png')
    power = 2

class Knife3(Thing):
    
    image = pg.image.load('data/inventory/knife/3.png')
    power = 3

class Knife4(Thing):
    
    image = pg.image.load('data/inventory/knife/4.png')
    power = 4

class Knife5(Thing):
    
    image = pg.image.load('data/inventory/knife/5.png')
    power = 5

knifes = [Knife1, Knife2, Knife3, Knife4, Knife5]

class Heart(Thing):
    
    image = pg.image.load('data/inventory/heart.png')
        
        
class Object(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.objects, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(x * my.cellSize, y * my.cellSize)

    def do(self):
        print(self.__class__)

    def trash(self):
        my.objects.remove(self)
        my.all_sprites.remove(self)
        

class Water(Object):

    image = pg.image.load('data/water.png')

        
class Tree(Object):

    image = pg.image.load('data/tree/with_apples.png')
    image2 = pg.image.load('data/tree/without_apples.png')

    def __init__(self, x, y):
        super().__init__(x, y)
        self.apples = True

    def do(self):
        if not self.apples:
            return 0
        self.apples = False
        self.image = Tree.image2
        count = randint(1, 10)
        for _ in range(count):
            my.inv.append(Apple)


class Stone(Object):

    image = pg.image.load('data/stone.png')


class Chest(Object):

    image = pg.image.load('data/chest/closed.png')
    image2 = pg.image.load('data/chest/open.png')
    objects = [Apple, 'Knife', Heart]
    knifes = [Knife1, Knife2, Knife3, Knife4, Knife5]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.closed = True

    def do(self):
        if not self.closed:
            return 0
        self.closed = False
        self.image = Chest.image2
        count = randint(1, 5)
        for _ in range(count):
            name = choice(Chest.objects)
            if name == 'Knife':
                name = choice(Chest.knifes)
            my.inv.append(name)
    
            
