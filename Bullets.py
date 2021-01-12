import pygame as pg
import Game
import My as my
from Objects import Water

"""Снаряды для стрельбы"""


class AppleBall(pg.sprite.Sprite):

    image = pg.image.load('data/apple.png')

    def __init__(self, direction):
        super().__init__(my.player_group, my.all_sprites)
        self.direction = direction
        self.speed = 0.2
        self.power = 1
        self.image = self.image
        self.rect = self.image.get_rect().move(Game.H_POS)

    def move(self):
        # Перемещение снаряда
        if self.direction == 'U':
            self.rect.y -= self.speed * Game.CELL_SIZE
        elif self.direction == 'D':
            self.rect.y += self.speed * Game.CELL_SIZE
        elif self.direction == 'R':
            self.rect.x += self.speed * Game.CELL_SIZE
        elif self.direction == 'L':
            self.rect.x -= self.speed * Game.CELL_SIZE

        # Проверка на препятствие 
        obj = pg.sprite.spritecollideany(self, my.evil_group)
        if obj:
            obj.to_hurt(self.power)
        else:
            obj = pg.sprite.spritecollideany(self, my.objects)
        if obj:
            self.death()

    def death(self):
        # Уничтожение файрбола
        my.player_group.remove(self)
        my.all_sprites.remove(self)

        
class FireBall(pg.sprite.Sprite):

    image = {'R': pg.image.load('data/fireball/right.png'),
             'L': pg.image.load('data/fireball/left.png'),
             'U': pg.image.load('data/fireball/up.png'),
             'D': pg.image.load('data/fireball/down.png'),
             }

    def __init__(self, evil, direction):
        super().__init__(my.evil_group, my.all_sprites)
        self.direction = direction
        self.speed = 0.2
        self.power = 1
        self.evil = evil
        self.image = FireBall.image[self.direction]
        self.rect = self.image.get_rect().move(self.evil.rect.x,
                                               self.evil.rect.y)

    def move(self):
        # Перемещение снаряда
        if self.direction == 'U':
            self.rect.y -= self.speed * Game.CELL_SIZE
        elif self.direction == 'D':
            self.rect.y += self.speed * Game.CELL_SIZE
        elif self.direction == 'R':
            self.rect.x += self.speed * Game.CELL_SIZE
        elif self.direction == 'L':
            self.rect.x -= self.speed * Game.CELL_SIZE

        # Проверка на препятствие 
        obj = pg.sprite.spritecollideany(self, my.player_group)
        if obj is my.player:
            self.death()
            my.player.removeLifes(self.power)
        else:
            obj = pg.sprite.spritecollideany(self, my.objects)
            if obj:
                if obj.__class__ != Water:
                    obj.death()
                self.death()
            else:
                obj = pg.sprite.spritecollideany(self, my.evil_group)
                if obj:
                    if obj != self.evil and obj.__class__ != FireBall:
                        obj.to_hurt(self.power)
                        self.death()

    def death(self, damage=None):
        # Уничтожение файрбола
        self.evil.wait = False
        my.evil_group.remove(self)
        my.all_sprites.remove(self)
