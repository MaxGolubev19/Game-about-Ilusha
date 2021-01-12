import pygame as pg
import Game


"""Инвентарь"""


class Inventory:
    def __init__(self):
        self.textSize = Game.INV_SIZE // 2
        self.font = pg.font.Font(None, self.textSize)
        self.inventory = pg.sprite.Group()      
        self.counts = {}
        self.queue = []
        self.place = 0
        self.choice = -1
        self.obj = None

    def append(self, name):
        # Добавление предмета в инвентарь
        if self.counts.get(name, False):
            self.counts[name] += 1
        else:
            self.queue.append(name)
            self.counts[name] = 1
            name(self.place)
            self.place += 1

    def remove(self, obj):
        # Удаление предмета из инвентаря
        name = obj.__class__
        self.counts[name] -= 1
        if not self.counts[name]:
            for sprite in self.inventory:
                if sprite.rect.x // Game.CELL_SIZE > self.queue.index(name):
                    sprite.rect.x -= Game.CELL_SIZE
            self.counts.pop(name)
            self.queue.remove(name)
            self.place -= 1
            self.inventory.remove(obj)
            self.choice = min(self.choice, self.place - 1)
            self.search()
        
    def draw(self):
        # Рисование инвентаря
        pg.draw.rect(Game.SCREEN, 'black', (0, Game.H - Game.INV_SIZE, Game.W, Game.INV_SIZE))
        self.inventory.draw(Game.SCREEN)
        pg.draw.rect(Game.SCREEN, 'white', (self.choice * Game.CELL_SIZE, Game.H - Game.INV_SIZE,
                                          Game.CELL_SIZE, Game.INV_SIZE), 3)
        for place in range(self.place):
            obj = self.queue[place]
            count = self.counts[obj]
            text = self.font.render(f"{count}", True, 'red')
            w, h = text.get_width(), text.get_height()
            x, y = (place + 1) * Game.CELL_SIZE - w, Game.H - h
            Game.SCREEN.blit(text, (x, y))
        
    def choose(self, x):
        # Выбор нового объекта
        place = x // Game.CELL_SIZE
        if place < self.place:
            self.choice = place
            self.search()

    def next(self):
        # Выбор следующего предмета в инвентаре
        if self.place:
            self.choice = (self.choice + 1) % self.place
            self.search()

    def search(self):
        # Поиск выбранного объекта
        from Hero import Invisible
        inv = Invisible((self.choice - 1) * Game.CELL_SIZE, Game.H - Game.CELL_SIZE)
        self.obj = inv.search('R', group=self.inventory)
        
