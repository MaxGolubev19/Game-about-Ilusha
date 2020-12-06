import pygame as pg
from Field import Field
from Hero import Hero
from Evil import Evil


def crGame():
    global screen, field, clock
    pg.init()
    pg.display.set_caption("Проект")
    screen = pg.display.set_mode(size)
    field = Field(size, maxSize, cellSize, screen)
    clock = pg.time.Clock()


def refresh():
    field.render()
    hero.draw()
    evil.draw(hero.getPos(), hPos)
    pg.display.flip()
    

def crHeroes():
    global hero, evil
    hero = Hero(hPos, field, screen)
    evil = Evil((100, 100), field, screen)
    
# Параметры поля
size = w, h = 1000, 600
maxSize = 1000000
cellSize = 40

# Параметры игры
running = True
fps = 100
hPos = w // 2, h // 2

# Создание игры
crGame()
crHeroes()

#Игровой цикл
while running:
    pressed = pg.key.get_pressed()
    hero.moving(pressed)
    evil.moving(hero.getPos())

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                hero.startMoving(event.pos)
    
    refresh()
    clock.tick(fps)

pg.quit()
