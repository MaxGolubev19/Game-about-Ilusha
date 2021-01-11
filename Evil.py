import pygame as pg
from Start import my, cut
from Objects import Water


class Evil(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.evil_group, my.all_sprites)
        self.direction = 'R'
        self.image = self.imageDied[self.direction]
        self.rect = self.image.get_rect().move(x * my.cellSize, y * my.cellSize)
        self.health = self.maxHealth
        self.wait = False
        self.step = 0
        self.time = 0

    def moving(self):
        x, y = my.hPos
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
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self):
        my.evil_group.remove(self)
        if self.__class__ != Ghost:
            my.objects.add(self)
        self.image = self.imageDied[self.direction]
        my.crEvil()

    def setImage(self, style):
        if style == 'moving' or self.wait:
            if self.time == my.time:
                self.image = self.imageRun[self.direction][self.step]
                self.step = (
                    self.step + 1) % len(self.imageRun[self.direction])
                self.time = 0
            else:
                self.time += 1
        elif style == 'fight':
            self.image = self.imageAttack[self.direction]
            self.time = 0


class Pig(Evil):

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

    speed = 0.1 * my.cellSize
    disRun = 10 * my.cellSize
    disAttack = 2 * my.cellSize
    disFight = my.cellSize
    maxHealth = 5
    power = 2

    def move(self):
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
                obj.trash()
            else:
                self.death()

    def check(self, dis):
        return (dis >= abs(self.rect.x - my.hPos[0]) and
                dis >= abs(self.rect.y - my.hPos[1]))

    def attack(self):
        x, y = my.hPos
        if (abs(self.rect.x - x) < my.cellSize and
                abs(self.rect.y - y) < my.cellSize):
            return

        if y > self.rect.y:
            self.rect.y += self.speed * 3
        if y <= self.rect.y:
            self.rect.y -= self.speed * 3
        if x > self.rect.x:
            self.rect.x += self.speed * 3
        if x <= self.rect.x:
            self.rect.x -= self.speed * 3

    def fight(self):
        my.player.removeLifes(Pig.power)
        self.wait = True

    def backMoving(self):
        if self.direction == 'U':
            self.rect.y += self.speed * 3
        if self.direction == 'D':
            self.rect.y -= self.speed * 3
        if self.direction == 'L':
            self.rect.x += self.speed * 3
        if self.direction == 'R':
            self.rect.x -= self.speed * 3
        if not self.check(self.disAttack * 4):
            self.wait = False


class Ghost(Evil):

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

    speed = 0.05 * my.cellSize
    disRun = 10 * my.cellSize
    disFight = 6 * my.cellSize
    maxHealth = 10

    def move(self):
        if self.check(Ghost.disFight, 0):
            self.setImage('fight')
            self.fight()
        elif self.check(Ghost.disRun, Ghost.disRun):
            self.setImage('moving')
            self.moving()

    def check(self, dis1, dis2):
        x, y = abs(self.rect.x - my.hPos[0]), abs(self.rect.y - my.hPos[1])
        return (dis1 >= x and dis2 >= y or dis1 >= y and dis2 >= x)

    def fight(self):
        if not self.wait:
            if my.hPos[1] > self.rect.y:
                direction = 'D'
            elif my.hPos[1] < self.rect.y:
                direction = 'U'
            elif my.hPos[0] > self.rect.x:
                direction = 'R'
            elif my.hPos[0] < self.rect.x:
                direction = 'L'
            MagicBall(self, direction)
            self.wait = True


class MagicBall(pg.sprite.Sprite):

    image = {'R': pg.image.load('data/fireball/right.png'),
             'L': pg.image.load('data/fireball/left.png'),
             'U': pg.image.load('data/fireball/up.png'),
             'D': pg.image.load('data/fireball/down.png'),
             }

    def __init__(self, evil, direction):
        super().__init__(my.evil_group, my.all_sprites)
        self.direction = direction
        self.speed = 0.2
        self.power = 1
        self.evil = evil

        self.image = MagicBall.image[self.direction]
        self.rect = self.image.get_rect().move(self.evil.rect.x, self.evil.rect.y)

    def move(self):
        if self.direction == 'U':
            self.rect.y -= self.speed * my.cellSize
        elif self.direction == 'D':
            self.rect.y += self.speed * my.cellSize
        elif self.direction == 'R':
            self.rect.x += self.speed * my.cellSize
        elif self.direction == 'L':
            self.rect.x -= self.speed * my.cellSize

        obj = pg.sprite.spritecollideany(self, my.player_group)
        if obj is my.player:
            self.to_hurt()
            my.player.removeLifes(self.power)
        elif obj is None:
            if obj is None:
                obj = pg.sprite.spritecollideany(self, my.objects)
            if obj:
                if obj.__class__ != Water:
                    obj.trash()
                self.to_hurt()
                self.evil.wait = False

    def to_hurt(self, damage=None):
        self.evil.wait = False
        my.evil_group.remove(self)
        my.all_sprites.remove(self)
