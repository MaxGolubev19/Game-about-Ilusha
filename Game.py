import pygame as pg
from Start import my
from Hero import Hero
from Evil import Pig
from Field import render


def refresh():
    # Обновление экрана
    my.screen.fill('black')
    render()
    my.all_sprites.draw(my.screen)
    my.player_group.draw(my.screen)
    my.inv.draw()
    pg.display.flip()
    my.clock.tick(my.fps)
    

refresh()

while my.running:
    refresh()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            my.running = False
        if event.type == pg.MOUSEBUTTONUP:
            x, y = event.pos
            if y > my.h - my.invSize:
                my.inv.choose(x)
        if event.type == pg.KEYUP:
            if event.key == pg.K_TAB:
                my.inv.next()
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

pg.quit()
