import pygame as pg
from Start import my


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
    