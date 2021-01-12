import pygame as pg
import Game
import My as my


"""Игровое поле"""


class Cell(pg.sprite.Sprite):

    image = pg.image.load('data/grass.png')
    
    def __init__(self, bg_sprites, x, y):
        super().__init__(bg_sprites)
        image = Cell.image
        self.rect = self.image.get_rect().move(x, y)    
            
 
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.stepX = 0
        self.stepY = 0

    def apply(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy

    def update(self, obj):
        self.dx = obj.rect.x - Game.H_POS[0]
        self.dy = obj.rect.y - Game.H_POS[1]
        self.stepX = (self.stepX - self.dx) % Game.CELL_SIZE - Game.CELL_SIZE
        self.stepY = (self.stepY - self.dy) % Game.CELL_SIZE - Game.CELL_SIZE


def render():
    # Рисование фона
    bg_sprites = pg.sprite.Group()
    for x in range(my.camera.stepX, Game.W, Game.CELL_SIZE):
        for y in range(my.camera.stepY, Game.H, Game.CELL_SIZE):
            cell = Cell(bg_sprites, x, y)
    bg_sprites.draw(Game.SCREEN)
    
