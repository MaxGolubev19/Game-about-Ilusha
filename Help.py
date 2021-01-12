import pygame as pg
from random import randint, choice
import Game
import My as my
from Field import render


"""Вспомогательные функции и классы"""


class Invisible(pg.sprite.Sprite):

    # Поиск объекта для взаимодейтсвия

    image = pg.image.load('data/grass.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = Invisible.image
        self.x = x
        self.y = y

    def search(self, direction, group):
        # Перемещение на нужную клетку
        if direction == 'U':
            self.y -= Game.CELL_SIZE
        elif direction == 'D':
            self.y += Game.CELL_SIZE
        elif direction == 'R':
            self.x += Game.CELL_SIZE
        elif direction == 'L':
            self.x -= Game.CELL_SIZE
        return self.check(group)

    def check(self, group):
        # Проверка существования объекта
        self.rect = self.image.get_rect().move(self.x, self.y)
        return pg.sprite.spritecollideany(self, group)


def cut(image): 
    # Разделение анимации на кадры
    frames = []
    w = image.get_width() // Game.CELL_SIZE
    h = image.get_height() // Game.CELL_SIZE
    rect = pg.Rect(0, 0, Game.CELL_SIZE, Game.CELL_SIZE)
    for y in range(h):
        for x in range(w):
            location = rect.w * x, rect.h * y
            frames.append(image.subsurface(pg.Rect(location, rect.size)))
    return frames


def refresh():
    # Обновление экрана
    Game.SCREEN.fill('black')
    render()
    my.all_sprites.draw(Game.SCREEN)
    my.player_group.draw(Game.SCREEN)
    my.inventory.draw()
    pg.display.flip()
    my.clock.tick(Game.FPS)


def crObject(name, allCount):
    # Создание объекта
    count = 0
    while count != allCount:
        x = randint(-Game.LENGTH, Game.LENGTH)
        y = randint(-Game.LENGTH, Game.LENGTH)
        inv = Invisible(x * Game.CELL_SIZE, y * Game.CELL_SIZE)
        obj1 = inv.search(None, my.player_group)
        obj2 = inv.search(None, my.objects)
        if not obj1 and not obj2:
            obj = name(x, y)
            count += 1


def crEvil():
    # Создание монстра
    from Evil import Pig, Ghost
    name = choice([Pig, Ghost])
    x = randint(-Game.LENGTH, Game.LENGTH)
    y = randint(-Game.LENGTH, Game.LENGTH)
    evil = name(x, y)


def can(obj):
    # Проверка клетки на другие объекты
    return len(pg.sprite.spritecollide(obj, my.objects, False)) == 1




















