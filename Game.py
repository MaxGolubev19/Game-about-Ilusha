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
    

player = Hero()
refresh()

while my.running:
    
    player.move()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            my.running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y > my.h - my.invSize:
                try:
                    my.inv.choose(x)
                except Exception as e:
                    print(e)
    
    my.camera.update(player)
    for sprite in my.all_sprites:
        my.camera.apply(sprite)

    if my.running:
        refresh()

pg.quit()
