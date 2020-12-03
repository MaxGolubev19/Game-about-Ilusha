import pygame as pg
from Board import Board


def crBoard():
    board = Board(w, h, maxSize, cellSize, screen)
    board.render()
    return board


def autoMoving():
    global time, stepX, endX, stepY, endY, moving
    if time:
        board.left -= stepX
        board.top -= stepY
        time -= 1
    else:
        board.left -= endX
        board.top -= endY
        moving = False


size = w, h = 1000, 600
cellSize = 40
maxSize = 1000000

running = True
moving = False
fps = 100
step = 3
cStep = 1
center = x0, y0 = w // 2, h // 2

 
pg.init()
pg.display.set_caption("Проект")
screen = pg.display.set_mode(size)
screen.fill('green')
pg.display.flip()
clock = pg.time.Clock()
board = crBoard()

while running:
    pressed = pg.key.get_pressed()
    
    if pressed[pg.K_LSHIFT]:
        cStep = 2
    else:
        cStep = 1
        
    if pressed[pg.K_w] or pressed[pg.K_UP]:
        board.top += step * cStep
        moving = False
    elif pressed[pg.K_s] or pressed[pg.K_DOWN]:
        board.top -= step * cStep
        moving = False
    elif pressed[pg.K_a] or pressed[pg.K_LEFT]:
        board.left += step * cStep
        moving = False
    elif pressed[pg.K_d] or pressed[pg.K_RIGHT]:
        board.left -= step * cStep
        moving = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                moving = True
                x, y = event.pos
                sx = x - x0
                sy = y - y0
                time = max(abs(sx), abs(sy)) // step
                stepX, endX, stepY, endY = 0, 0, 0, 0
                if sx:
                    stepX = abs(sx) // time * (sx // abs(sx))
                    endX = abs(sx) % time * (sx // abs(sx))
                if sy:
                    stepY = abs(sy) // time * (sy // abs(sy))
                    endY = abs(sy) % time * (sy // abs(sy))

    if moving:
        autoMoving()
    
    screen.fill('green')
    board.render()
    pg.draw.circle(screen, 'red', center, 20)
    pg.display.flip()
    clock.tick(fps)

pg.quit()
