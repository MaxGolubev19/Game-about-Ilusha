import pygame as pg
from random import randint


class Start:
    def __init__(self):
        # Параметры игры
        self.cellSize = 50
        self.fps = 100
        self.length = 30
        self.size = self.w, self.h = 1000, 600
        self.hPos = (self.w // 2 - self.cellSize // 2,
                     self.h // 2 - self.cellSize // 2)
        self.stepX = 0
        self.stepY = 0

    def create(self):
        self.crGame()
        self.crWater()
        try:
            self.crObjects()
        except Exception as e:
            print(e)

    def crGame(self):
        # Создание игры
        from Field import Camera
        
        pg.init()
        pg.display.set_caption('Проект')
        self.screen = pg.display.set_mode(self.size)
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        
        self.camera = Camera()
        self.clock = pg.time.Clock()
        self.running = True

    def crWater(self):
        from Objects import Water
        
        for a in range(-self.length - 10, self.length + 11):
            for b in range(self.length + 1, self.length + 11):
                Water(a, b)
                Water(a, -b)
                Water(b, a)
                Water(-b, a)

    def crObjects(self):
        from Objects import Tree, Stone, Chest

        self.crObject(Stone, self.length)
        self.crObject(Tree, self.length)
        self.crObject(Chest, self.length // 5)

    def crObject(self, name, count):
        for i in range(count):
            x = randint(-self.length, self.length)
            y = randint(-self.length, self.length)
            name(x, y)
            

my = Start()
my.create()
