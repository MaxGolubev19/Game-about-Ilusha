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
        self.place = 0
        self.choice = -1
        self.gun = None

    def append(self, obj):
        if self.counts.get(obj, False):
            self.counts[obj][1] += 1
        else:
            self.counts[obj] = [self.place, 1]
            obj(self.place, inv=True)
            self.place += 1
        
    def draw(self):
        pg.draw.rect(my.screen, 'black', (0, my.h - my.invSize, my.w, my.invSize))
        my.inventory.draw(my.screen)
        pg.draw.rect(my.screen, 'white', (self.choice * my.cellSize, my.h - my.invSize,
                                          my.cellSize, my.invSize), 3)
        for obj in self.counts:
            place, count = self.counts[obj]
            text = self.font.render(f"{count}", True, 'red')
            w, h = text.get_width(), text.get_height()
            x, y = (place + 1) * my.cellSize - w, my.h - h
            my.screen.blit(text, (x, y))
        
    def choose(self, x):
        place = x // my.cellSize
        if place < self.place:
            self.choice = place
            inv = Invisible((place - 1) * my.cellSize, my.h - my.invSize)
            self.gun = inv.search(group=my.inventory)
        
        
            
        
    
    
