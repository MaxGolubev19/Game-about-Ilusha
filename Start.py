import pygame as pg


class Start:
    def __init__(self):
        # Параметры игры
        self.cellSize = 50
        self.fps = 100
        self.size = self.w, self.h = 1000, 600
        self.hPos = (self.w // 2 - self.cellSize // 2,
                     self.h // 2 - self.cellSize // 2)
        self.stepX = 0
        self.stepY = 0

    def create(self):
        # Создание игры
        from Field import Camera
        
        pg.init()
        pg.display.set_caption('Проект')
        self.screen = pg.display.set_mode(self.size)
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        
        self.camera = Camera()
        self.clock = pg.time.Clock()
        self.running = True


my = Start()
my.create()
