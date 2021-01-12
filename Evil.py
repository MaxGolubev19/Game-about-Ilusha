import pygame as pg
import Game
import My as my
from Help import cut, crEvil
from Objects import Water
from Bullets import FireBall


"""Монстры"""


class Evil(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.evil_group, my.all_sprites)
        self.direction = 'R'
        self.health = self.maxHealth
        self.wait = False
        self.step = 0
        self.time = 0
        self.image = self.imageDied[self.direction]
        self.rect = self.image.get_rect().move(x * Game.CELL_SIZE,
                                               y * Game.CELL_SIZE)
        
    def moving(self):
        # Перемещение
        x, y = Game.H_POS
        if y > self.rect.y:
            self.direction = 'D'
            self.rect.y += self.speed
        if y < self.rect.y:
            self.direction = 'U'
            self.rect.y -= self.speed
        if x > self.rect.x:
            self.direction = 'R'
            self.rect.x += self.speed
        if x < self.rect.x:
            self.direction = 'L'
            self.rect.x -= self.speed

    def to_hurt(self, damage):
        # Получение урона
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self):
        # Смерть
        my.evil_group.remove(self)
        if self.__class__ != Ghost:
            my.objects.add(self)
        self.image = self.imageDied[self.direction]
        crEvil()

    def setImage(self, style):
        # Смена кадра анимации
        if style == 'moving' or self.wait:
            if self.time == Game.TIME:
                self.image = self.imageRun[self.direction][self.step]
                self.step = (
                    self.step + 1) % len(self.imageRun[self.direction])
                self.time = 0
            else:
                self.time += 1
        elif style == 'fight':
            self.image = self.imageAttack[self.direction]
            self.time = 0

    def do(self):
        pass


class Pig(Evil):
    
    """
    Свин:
    - Колет героя рогом
    - Разрушает всё на своём пути
    """
    
    imageRun = {'R': cut(pg.image.load('data/pig/rightRun.png')),
                'L': cut(pg.image.load('data/pig/leftRun.png')),
                'U': cut(pg.image.load('data/pig/leftRun.png')),
                'D': cut(pg.image.load('data/pig/leftRun.png')),
                }

    imageAttack = {'R': pg.image.load('data/pig/rightAttack.png'),
                   'L': pg.image.load('data/pig/leftAttack.png'),
                   'U': pg.image.load('data/pig/leftAttack.png'),
                   'D': pg.image.load('data/pig/leftAttack.png'),
                   }

    imageDied = {'R': pg.image.load('data/pig/rightDied.png'),
                 'L': pg.image.load('data/pig/leftDied.png'),
                 'U': pg.image.load('data/pig/leftDied.png'),
                 'D': pg.image.load('data/pig/leftDied.png'),
                 }

    speed = 0.1 * Game.CELL_SIZE
    disRun = 10 * Game.CELL_SIZE
    disAttack = 2 * Game.CELL_SIZE
    disFight = Game.CELL_SIZE
    maxHealth = 5
    power = 2

    def move(self):
        # Действие
        if self.wait:
            self.setImage('moving')
            self.backMoving()
        elif self.check(Pig.disFight):
            self.setImage('fight')
            self.fight()
        elif self.check(Pig.disAttack):
            self.setImage('fight')
            self.attack()
        elif self.check(Pig.disRun):
            self.setImage('moving')
            self.moving()
        obj = pg.sprite.spritecollideany(self, my.objects)
        if obj:
            if obj.__class__ != Water:
                obj.death()
            else:
                self.death()

    def check(self, dis):
        # Проверка расстояния до героя
        return (dis >= abs(self.rect.x - Game.H_POS[0]) and
                dis >= abs(self.rect.y - Game.H_POS[1]))

    def attack(self):
        # Атака
        x, y = Game.H_POS
        if (abs(self.rect.x - x) < Game.CELL_SIZE and
                abs(self.rect.y - y) < Game.CELL_SIZE):
            return

        if y > self.rect.y:
            self.rect.y += self.speed * 4
        if y <= self.rect.y:
            self.rect.y -= self.speed * 4
        if x > self.rect.x:
            self.rect.x += self.speed * 4
        if x <= self.rect.x:
            self.rect.x -= self.speed * 4

    def fight(self):
        # Удар
        my.player.removeLifes(Pig.power)
        self.wait = True

    def backMoving(self):
        # Возвращение на изначальную позицию
        if self.direction == 'U':
            self.rect.y += self.speed * 4
        if self.direction == 'D':
            self.rect.y -= self.speed * 4
        if self.direction == 'L':
            self.rect.x += self.speed * 4
        if self.direction == 'R':
            self.rect.x -= self.speed * 4
        if not self.check(self.disAttack * 4):
            self.wait = False


class Ghost(Evil):

    """
    Призрак:
    - Запускает в героя файрбол
    - Проходит сквозь любые препятствия 
    """

    imageRun = {'R': cut(pg.image.load('data/ghost/right.png')),
                'L': cut(pg.image.load('data/ghost/left.png')),
                'U': cut(pg.image.load('data/ghost/left.png')),
                'D': cut(pg.image.load('data/ghost/left.png')),
                }

    imageAttack = {'R': pg.image.load('data/ghost/rightAttack.png'),
                   'L': pg.image.load('data/ghost/leftAttack.png'),
                   'U': pg.image.load('data/ghost/leftAttack.png'),
                   'D': pg.image.load('data/ghost/leftAttack.png'),
                   }

    imageDied = {'R': pg.image.load('data/ghost/rightDied.png'),
                 'L': pg.image.load('data/ghost/leftDied.png'),
                 'U': pg.image.load('data/ghost/leftDied.png'),
                 'D': pg.image.load('data/ghost/leftDied.png'),
                 }

    speed = 0.05 * Game.CELL_SIZE
    disRun = 10 * Game.CELL_SIZE
    disFight = 6 * Game.CELL_SIZE
    maxHealth = 10

    def move(self):
        # Действие 
        if self.check(Ghost.disFight, 0):
            self.setImage('fight')
            self.fight()
        elif self.check(Ghost.disRun, Ghost.disRun):
            self.setImage('moving')
            self.moving()

    def check(self, dis1, dis2):
        # Проверка расстояния до героя
        x, y = abs(self.rect.x - Game.H_POS[0]), abs(self.rect.y - Game.H_POS[1])
        return (dis1 >= x and dis2 >= y or dis1 >= y and dis2 >= x)

    def fight(self):
        # Запуск файрбола
        if not self.wait:
            if Game.H_POS[1] > self.rect.y:
                direction = 'D'
            elif Game.H_POS[1] < self.rect.y:
                direction = 'U'
            elif Game.H_POS[0] > self.rect.x:
                direction = 'R'
            elif Game.H_POS[0] < self.rect.x:
                direction = 'L'
            FireBall(self, direction)
            self.wait = True
