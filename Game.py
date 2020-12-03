import pygame as pg
from Board import Board


def crBoard():
    board = Board(500, 500, screen)
    board.set_view(-300, -300, 40)
    board.render()
    return board


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("Проект")
    screen = pg.display.set_mode((1000, 600))
    screen.fill('black')
    pg.display.flip()
    clock = pg.time.Clock()

    board = crBoard()

    running = True
    fps = 100
    step = 1
    x, y = 500, 300

    while running:
        pressed = pg.key.get_pressed()
        if pressed[pg.K_w] or pressed[pg.K_UP]:
            y -= step
        elif pressed[pg.K_s] or pressed[pg.K_DOWN]:
            y += step
        elif pressed[pg.K_a] or pressed[pg.K_LEFT]:
            x -= step
        elif pressed[pg.K_d] or pressed[pg.K_RIGHT]:
            x += step

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill('black')
        board.render()
        pg.draw.circle(screen, 'red', (x, y), 20)
        pg.display.flip()
        clock.tick(fps)

    pg.quit()
