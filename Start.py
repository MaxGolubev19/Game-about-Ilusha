import pygame as pg
from random import randint, choice

        
class Start:
    def __init__(self):
        # Параметры игры
        self.cellSize = 50
        self.invSize = 50
        self.fps = 100
        self.length = 60
        self.maxHealth = 10
        self.title = 'Игра'
        self.size = self.w, self.h = 1000, 600
        self.hPos = (self.w // 2 - self.cellSize // 2,
                     self.h // 2 - self.cellSize // 2)

        pg.init()
        pg.display.set_caption(self.title)
        self.screen = pg.display.set_mode(self.size)

    def create(self, text):
        self.crGame()
        self.crWater()
        self.crObjects()
        self.text_screen(text)

    def crGame(self):
        # Создание игры
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.evil_group = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.inventory = pg.sprite.Group()
        self.pressed = []

        from Field import Camera, Inventory

        self.stepX = 0
        self.stepY = 0        
        self.camera = Camera()
        self.inv = Inventory()
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
        from Hero import Hero

        self.player = Hero()
        self.crObject(Stone, self.length)
        self.crObject(Tree, self.length)
        self.crObject(Chest, self.length // 2)
        self.crEvils(self.length // 5)

    def crObject(self, name, allCount):
        count = 0
        while count != allCount:
            x = randint(-self.length, self.length)
            y = randint(-self.length, self.length)
            obj = name(x, y)
            if self.can(obj):
                count += 1
            else:
                my.objects.remove(obj)

    def crEvils(self, allCount):
        for _ in range(allCount):
            self.crEvil()        

    def crEvil(self):
        from Evil import Pig, Ghost
        
        name = choice([Pig, Ghost])
        x = randint(-self.length, self.length)
        y = randint(-self.length, self.length)
        evil = name(x, y)

    def text_screen(self, intro_text):
        fon = pg.transform.scale(pg.image.load('data/fon.jpg'), self.size)
        self.screen.blit(fon, (0, 0))
        font = pg.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, 'white')
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN or \
                        event.type == pg.MOUSEBUTTONDOWN:
                    return
            pg.display.flip()
            self.clock.tick(my.fps)
                
    def can(self, obj):
        return len(pg.sprite.spritecollide(obj, my.objects, False)) == 1

    def endGame(self):
        self.clock.tick(5)
        self.running = False
        self.create(['Вы проиграли!', '', 'Нажмите любую кнопку, чтобы начать новую игру'])
        

my = Start()
my.create(['Игра', '', 'Нажмите любую кнопку, чтобы начать игру'])
