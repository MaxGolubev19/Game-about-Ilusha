import pygame as pg
import Game


pg.init()


from Help import refresh
from Start import newGame
import My as my

"""Игровой цикл"""


pg.display.set_caption(Game.TITLE)
pg.display.set_icon(pg.image.load("data/icon.ico"))
Game.SCREEN = pg.display.set_mode(Game.SIZE)
pg.mixer.music.load('data/sounds/music.mp3')
pg.mixer.music.set_volume(Game.MUSIC_VOLUME)
pg.mixer.music.play()
newGame()

while True:
    while my.running:
        refresh()

        my.pressed = pg.key.get_pressed()

        for sprite in my.player_group:
            sprite.move()

        for sprite in my.evil_group:
            sprite.move()
            
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
                if event.key == pg.K_i:
                    my.music = not my.music
                    if my.music:
                       pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                if event.key == pg.K_o:
                    my.sound = not my.sound
                if event.key == pg.K_p:
                    my.sound_run = not my.sound_run
                    my.sound = my.sound_run
        
        my.camera.update(my.player)
        for sprite in my.all_sprites:
            my.camera.apply(sprite)

    newGame()
