import pygame as pg
import Game
from Help import refresh
from Start import newGame
import My as my


"""Игровой цикл"""


pg.init()
pg.display.set_caption(Game.TITLE)
pg.display.set_icon(pg.image.load("data/icon.ico"))
Game.SCREEN = pg.display.set_mode(Game.SIZE)
newGame(True)

while True:
    while my.running:
        refresh()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONUP:
                x, y = event.pos
                if y > Game.H - Game.INV_SIZE:
                    my.inventory.choose(x)
            if event.type == pg.KEYUP:
                if event.key == pg.K_TAB:
                    my.inventory.next()
                if event.key == pg.K_SPACE:
                    my.player.do()
                if event.key == pg.K_e:
                    my.player.used()

        my.pressed = pg.key.get_pressed()

        for sprite in my.player_group:
            sprite.move()

        for sprite in my.evil_group:
            sprite.move()
        
        my.camera.update(my.player)
        for sprite in my.all_sprites:
            my.camera.apply(sprite)

    newGame(False)
