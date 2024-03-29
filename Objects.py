import pygame as pg
from random import randint, choice
import Game
import My as my
from Thing import Apple, Knife, Heart, God


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
        self.image = self.imageTrash
        

class Water(Object):

    image = pg.image.load('data/water.png')

        
class Tree(Object):

    image = pg.image.load('data/tree/with_apples.png')
    imageUsed = pg.image.load('data/tree/without_apples.png')
    imageTrash = pg.image.load('data/tree/trash.png')
    
    sound = pg.mixer.Sound('data/sounds/objects/tree.mp3')
    sound.set_volume(Game.SOUND_VOLUME)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.apples = True

    def do(self):
        # Взаимодействие с объектом
        if not self.apples:
            return 0
        self.apples = False
        if my.sound:
            Tree.sound.play()
        self.image = Tree.imageUsed
        count = randint(1, 10)
        for _ in range(count):
            my.inventory.append(Apple)


class Stone(Object):

    image = pg.image.load('data/stone/stone.png')
    imageTrash = pg.image.load('data/stone/trash.png')


class Chest(Object):

    objects = [Apple, Knife, Heart, God]
    
    image = pg.image.load('data/chest/closed.png')
    imageUsed = pg.image.load('data/chest/open.png')
    imageTrash = pg.image.load('data/chest/trash.png')
    
    sound = pg.mixer.Sound('data/sounds/objects/chest.mp3')
    sound.set_volume(Game.SOUND_VOLUME)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.closed = True

    def do(self):
        # Взаимодействие с объектом
        if not self.closed:
            return 0
        self.closed = False
        if my.sound:
            Chest.sound.play()
        self.image = Chest.imageUsed
        count = randint(1, 5)
        for _ in range(count):
            name = choice(Chest.objects)
            my.inventory.append(name)

            
