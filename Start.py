import pygame as pg
from random import randint, choice
import Game
import My as my
from Field import Camera
from Inventory import Inventory
from Objects import Water, Tree, Stone, Chest
from Hero import Hero
from Evil import Pig, Ghost
from Help import crObject, crEvil, can, Button


"""Новая игра"""


def newGame():
    # Перезапуск игры
    crGame()
    menu()
    crWater()
    crObjects()


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
    my.score = 0


def crWater():
    # Создание водной границы вокруг поля
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
    # Создание монстров
    for _ in range(allCount):
        crEvil()

    
def menu():
    # Создание меню
    image = pg.transform.scale(pg.image.load('data/new_game.png'), Game.SIZE)
    click = pg.mixer.Sound('data/sounds/click.mp3')
    click.set_volume(Game.SOUND_VOLUME)
    buttons = pg.sprite.Group()
    Button('Game', buttons)
    Button('Docs', buttons)
    Button('Exit', buttons)

    while True:
        
        Game.SCREEN.blit(image, (0, 0))
            
        mousePos = pg.mouse.get_pos()
        chosenBtn = None
        for btn in buttons:
            if btn.check(mousePos):
                chosenBtn = btn
        if chosenBtn:
            if chosenBtn.first:
                click.play()
            chosenBtn.chosen()

        for btn in buttons:
            btn.draw()
            
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                style = None
                for btn in buttons:
                    if btn.check(event.pos):
                        style = btn.style
                if style == 'Game':
                    return
                elif style == 'Docs':
                    docs()
                elif style == 'Exit':
                    pg.quit()
                    exit()
            
        pg.display.flip()
        my.clock.tick(Game.FPS)


def docs():
    # Справка
    text = ["WASD / СТРЕЛКИ - управление персонажем",
            "SHIFT - ускорение",
            "E - взаимодействие с объектом",
            "TAB / МЫШЬ - выбор предмета в инветаре",
            "SPACE - использование выбранного предмета инвентаря",
            "I - включить/выключить фоновую музыку",
            "O - включить/выключить звуки (кроме звуков ходьбы)",
            "P - включить/выключить все звуки",
            "F1 - инструкция",
            "",
            "Нажмите любую кнопку для возвращения в игру"
            ]
    
    fon = pg.transform.scale(pg.image.load('data/docs.png'), Game.SIZE)
    Game.SCREEN.blit(fon, (0, 0))
    
    font = pg.font.Font(None, 30)
    y = 100
    for line in text:
        string = font.render(line, 1, 'white')
        rect = string.get_rect()
        y += 10
        rect.top = y
        rect.x = 100
        y += rect.height
        Game.SCREEN.blit(string, rect)

    my.openDocs = False

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
    

def res():
    # Справка
    fon = pg.transform.scale(pg.image.load('data/docs.png'), Game.SIZE)
    Game.SCREEN.blit(fon, (0, 0))
    
    font1 = pg.font.Font(None, 80)
    headline = font1.render("Результат:", 1, 'white')
    rect1 = headline.get_rect()
    rect1.x = (Game.W - rect1.w) / 2
    rect1.y = 100
    Game.SCREEN.blit(headline, rect1)
    
    font2 = pg.font.Font(None, 100)
    score = font2.render(str(my.score), 1, 'white')
    rect2 = score.get_rect()
    rect2.x = (Game.W - rect2.w) / 2
    rect2.y = 300
    Game.SCREEN.blit(score, rect2)

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
    res()
