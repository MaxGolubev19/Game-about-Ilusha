import pygame as pg
from random import randint, choice
import Game
import My as my
from Field import Camera
from Inventory import Inventory
from Objects import Water, Tree, Stone, Chest
from Hero import Hero
from Evil import Pig, Ghost
from Help import crObject, crEvil, can


"""Новая игра"""


def newGame():
    crGame()
    crWater()
    crObjects()
    startScreen()


def crGame():
    # Создание новой игры
    my.all_sprites = pg.sprite.Group()
    my.player_group = pg.sprite.Group()
    my.evil_group = pg.sprite.Group()
    my.objects = pg.sprite.Group()
    my.pressed = []
    my.player = Hero()
    my.camera = Camera()
    my.inventory = Inventory()
    my.clock = pg.time.Clock()
    my.running = True


def crWater():
    for a in range(-Game.LENGTH - 10, Game.LENGTH + 11):
        for b in range(Game.LENGTH + 1, Game.LENGTH + 11):
            Water(a, b)
            Water(a, -b)
            Water(b, a)
            Water(-b, a)


def crObjects():
    # Создание объектов
    crObject(Stone, Game.LENGTH)
    crObject(Tree, Game.LENGTH)
    crObject(Chest, Game.LENGTH // 2)
    crEvils(Game.LENGTH // 5)


def crEvils(allCount):
        for _ in range(allCount):
            crEvil()

    
def startScreen():
    image = pg.transform.scale(pg.image.load('data/new_game.png'), Game.SIZE)
    Game.SCREEN.blit(image, (0, 0))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        my.clock.tick(Game.FPS)


def docs(text):
    # Экран
    fon = pg.transform.scale(pg.image.load('data/new_game.png'), Game.SIZE)
    Game.SCREEN.blit(fon, (0, 0))
    font = pg.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, 'white')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        Game.SCREEN.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        my.clock.tick(Game.FPS)


def endGame():
    # Окончание игры
    global running    
    my.clock.tick(5)
    my.running = False
