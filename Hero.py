import pygame as pg
from Start import my


class Hero(pg.sprite.Sprite):

    image = pg.image.load('data/hero/right.png')
    imageRight = pg.image.load('data/hero/right.png')
    imageLeft = pg.image.load('data/hero/left.png')
    
    def __init__(self):
        super().__init__(my.player_group, my.all_sprites)
        self.image = Hero.image
        self.x = my.hPos[0]
        self.y = my.hPos[1]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)

        self.checkPos()
        
        self.crHealth()
        
        self.speed = 0.1
        self.fight = False

    def checkPos(self):
        objs = pg.sprite.spritecollide(self, my.objects, True)
        for obj in objs:
            my.all_sprites.remove(obj)

    def crHealth(self):
        [Life(self, i * 30, 0) for i in range(my.maxHealth)]   

    def move(self):
        # Получение команд клавиатуры
        pressed = pg.key.get_pressed()

        # Установка скорости
        speed = self.speed
        if pressed[pg.K_LSHIFT]:
            speed *= 2

        # Перемещение персонажа
        if pressed[pg.K_w] or pressed[pg.K_UP]:
            self.rect.y -= my.cellSize * speed
            if self.cant():
                self.rect.y += my.cellSize * speed
        if pressed[pg.K_s] or pressed[pg.K_DOWN]:
            self.rect.y += my.cellSize * speed
            if self.cant():
                self.rect.y -= my.cellSize * speed
        if pressed[pg.K_a] or pressed[pg.K_LEFT]:
            self.image = Hero.imageLeft
            self.rect.x -= my.cellSize * speed
            if self.cant():
                self.rect.x += my.cellSize * speed
        if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            self.image = Hero.imageRight
            self.rect.x += my.cellSize * speed
            if self.cant():
                self.rect.x -= my.cellSize * speed

        # Взаимодействие
        if pressed[pg.K_e]:
            inv = Invisible(self.x, self.y)
            obj = inv.search()
            if obj:
                obj.do()
                
    def cant(self):
        return (pg.sprite.spritecollideany(self, my.objects) or
                pg.sprite.spritecollideany(self, my.evil_group))


class Life(pg.sprite.Sprite):

    image = pg.image.load('data/heart.png')

    def __init__(self, hero, x, y):
        super().__init__(my.player_group)
        self.rect = self.image.get_rect().move(x, y)   
        
    
class Invisible(pg.sprite.Sprite):

    image = pg.image.load('data/grass.png')
    
    def __init__(self, x, y):
        super().__init__()
        self.image = Invisible.image
        self.x = x
        self.y = y

    def search(self):
        cells = [(self.x + my.cellSize, self.y),
                 (self.x - my.cellSize, self.y),
                 (self.x, self.y - my.cellSize),
                 (self.x, self.y + my.cellSize)]
        
        for x, y in cells:
            obj = self.check(x, y)
            if obj:
                return obj

    def check(self, x, y):
        self.rect = self.image.get_rect().move(x, y)
        return pg.sprite.spritecollideany(self, my.objects)












            
