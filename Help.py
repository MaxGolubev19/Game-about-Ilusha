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


class Particle(pg.sprite.Sprite):
    magic = [pg.image.load('data/ghost/magic.png')]
    for scale in (5, 10, 20):
        magic.append(pg.transform.scale(magic[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(my.all_sprites)
        self.image = choice(Particle.magic)
        self.rect = self.image.get_rect().move(pos)
        self.velocity = [dx, dy]
        self.board = (pos[0] - Game.CELL_SIZE, pos[1] - Game.CELL_SIZE,
                      2 * Game.CELL_SIZE, 2 * Game.CELL_SIZE)

    def update(self, firework):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.board):
            firework.remove(self)
            self.kill()
        

def crFirework(position):
    count = 20
    numbers = [range(-2, 0), range(1, 3)]
    return [Particle(position, choice(choice(numbers)),
                    choice(choice(numbers))) for _ in range(count)]


class Button(pg.sprite.Sprite):
    texts = ["Новая игра", "Инструкция", "Выxод"]
    def __init__(self, style, group):
        super().__init__(group)
        self.style = style
        self.first = True
        
        font = pg.font.Font(None, 40)
        text1 = font.render(Button.texts[0], True, 'yellow')
        text2 = font.render(Button.texts[1], True, 'yellow')
        text3 = font.render(Button.texts[2], True, 'yellow')
        self.h = text1.get_height()
        self.w = max(text1.get_width(), text2.get_width(), text3.get_width())
        if self.style == 'Game':
            self.text = text1
            self.x = self.w / 2 - self.text.get_width() / 2 + 40
            self.y = Game.H - 180
        elif self.style == 'Docs':
            self.text = text2
            self.x = self.w / 2 - self.text.get_width() / 2 + 40
            self.y = Game.H - 125
        elif self.style == 'Exit':
            self.text = text3
            self.x = self.w / 2 - self.text.get_width() / 2 + 40
            self.y = Game.H - 70
        self.rect = (30, self.y - 10, self.w + 20, self.h + 20)

    def draw(self):
        Game.SCREEN.blit(self.text, (self.x, self.y))
        pg.draw.rect(Game.SCREEN, 'yellow', self.rect, 3)

    def check(self, pos):
        x, y = pos
        chosen = (self.x <= x <= self.x + self.w and
                 self.y <= y <= self.y + self.h)
        if not chosen:
            self.first = True
        return chosen
        

    def chosen(self):
        self.first = False
        pg.draw.rect(Game.SCREEN, 'brown', self.rect)












