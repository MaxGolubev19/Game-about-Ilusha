import pygame as pg
from Start import my
from Hero import Hero
from Evil import Evil
from Field import render


def refresh():
    # Обновление экрана
    my.screen.fill('black')
    render()
    my.all_sprites.draw(my.screen)
    my.player_group.draw(my.screen)
    pg.display.flip()
    my.clock.tick(my.fps)
    

player = Hero()
refresh()

while my.running:
    
    player.move()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            my.running = False

    my.camera.update(player)
    for sprite in my.all_sprites:
        my.camera.apply(sprite)

    refresh()

pg.quit()
