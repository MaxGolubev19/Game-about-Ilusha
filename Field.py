import pygame as pg
from Start import my
from Hero import Invisible


class Cell(pg.sprite.Sprite):

    image = pg.image.load('data/grass.png')
    
    def __init__(self, bg_sprites, x, y):
        super().__init__(bg_sprites)
        image = Cell.image
        self.rect = self.image.get_rect().move(x, y)


def render():
    # Рисование фона
    bg_sprites = pg.sprite.Group()
    for x in range(my.stepX, my.w, my.cellSize):
        for y in range(my.stepY, my.h, my.cellSize):
            cell = Cell(bg_sprites, x, y)
    bg_sprites.draw(my.screen)
    
            
 
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy

    def update(self, obj):
        self.dx = obj.rect.x - my.hPos[0]
        self.dy = obj.rect.y - my.hPos[1]
        my.stepX = (my.stepX - self.dx) % my.cellSize - my.cellSize
        my.stepY = (my.stepY - self.dy) % my.cellSize - my.cellSize


class Inventory:
    def __init__(self):
        self.textSize = 20
        self.font = pg.font.Font(None, self.textSize)
        
        self.counts = {}
        self.queue = []
        self.place = 0
        self.choice = -1
        self.obj = None

    def append(self, name):
        if self.counts.get(name, False):
            self.counts[name] += 1
        else:
            self.queue.append(name)
            self.counts[name] = 1
            name(self.place)
            self.place += 1

    def remove(self, obj):
        name = obj.__class__
        self.counts[name] -= 1
        if not self.counts[name]:
            for sprite in my.inventory:
                if sprite.rect.x // my.cellSize > self.queue.index(name):
                    sprite.rect.x -= my.cellSize
            self.counts.pop(name)
            self.queue.remove(name)
            self.place -= 1
            my.inventory.remove(obj)
            self.choice = min(self.choice, self.place - 1)
            self.search()
        
    def draw(self):
        pg.draw.rect(my.screen, 'black', (0, my.h - my.invSize, my.w, my.invSize))
        my.inventory.draw(my.screen)
        pg.draw.rect(my.screen, 'white', (self.choice * my.cellSize, my.h - my.invSize,
                                          my.cellSize, my.invSize), 3)
        for place in range(self.place):
            obj = self.queue[place]
            count = self.counts[obj]
            text = self.font.render(f"{count}", True, 'red')
            w, h = text.get_width(), text.get_height()
            x, y = (place + 1) * my.cellSize - w, my.h - h
            my.screen.blit(text, (x, y))
        
    def choose(self, x):
        place = x // my.cellSize
        if place < self.place:
            self.choice = place
            self.search()

    def next(self):
        if self.place:
            self.choice = (self.choice + 1) % self.place
            self.search()

    def search(self):
        inv = Invisible((self.choice - 1) * my.cellSize, my.h - my.invSize)
        self.obj = inv.search('R', group=my.inventory)
        
            
        
    
    
