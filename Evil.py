import pygame as pg
from Start import my
from Objects import Water


class Evil(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(my.evil_group, my.all_sprites)
        self.image = self.image
        self.rect = self.image.get_rect().move(x * my.cellSize, y * my.cellSize)
        self.health = self.maxHealth
        self.direction = 'R'
        self.wait = False

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
            self.image = self.imageRight
            self.rect.x += self.speed
        if x < self.rect.x:
            self.direction = 'L'
            self.image = self.imageLeft
            self.rect.x -= self.speed

    def to_hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death()

    def death(self):
        my.evil_group.remove(self)
        my.objects.add(self)
        self.image = self.imageDied
        my.crEvil()


class Pig(Evil):

    image = pg.image.load('data/pig/right.png')
    imageRight = pg.image.load('data/pig/right.png')
    imageLeft = pg.image.load('data/pig/left.png')
    imageAttackRight = pg.image.load('data/pig/rightAttack.png')
    imageAttackLeft = pg.image.load('data/pig/leftAttack.png')
    imageDied = pg.image.load('data/pig/rightDied.png')
    
    speed = 0.1 * my.cellSize
    disRun = 10 * my.cellSize
    disAttack = 2 * my.cellSize
    disFight = my.cellSize
    maxHealth = 5
    power = 2

    def move(self):
        if self.wait:
            self.backMoving()
        elif self.check(Pig.disFight):
            self.fight() 
        elif self.check(Pig.disAttack):
            self.attack()
        elif self.check(Pig.disRun):
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
            self.image = Pig.imageAttackRight
            self.rect.x += self.speed * 3
        if x <= self.rect.x:
            self.image = Pig.imageAttackLeft
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

    image = pg.image.load('data/ghost/right.png')
    imageRight = pg.image.load('data/ghost/right.png')
    imageLeft = pg.image.load('data/ghost/left.png')
    imageAttackRight = pg.image.load('data/ghost/right.png')
    imageAttackLeft = pg.image.load('data/ghost/left.png')
    imageDied = pg.image.load('data/ghost/rightDied.png')

    speed = 0.05 * my.cellSize
    disRun = 10 * my.cellSize
    disFight = 6 * my.cellSize
    maxHealth = 10

    def move(self):
        if self.check(Ghost.disFight, 0):
            self.fight()
        elif self.check(Ghost.disRun, Ghost.disRun):
            self.moving()

    def check(self, dis1, dis2):
        x, y = abs(self.rect.x - my.hPos[0]), abs(self.rect.y - my.hPos[1])
        return (dis1 >= x and dis2 >= y or dis1 >= y and dis2 >= x)

    def fight(self):
        if not self.wait:
            MagicBall(self, self.direction)
            self.wait = True


class MagicBall(pg.sprite.Sprite):

    imageUp = pg.image.load('data/fireball/up.png')
    imageDown = pg.image.load('data/fireball/down.png')
    imageRight = pg.image.load('data/fireball/right.png')
    imageLeft = pg.image.load('data/fireball/left.png')
    
    def __init__(self, evil, direction):
        super().__init__(my.evil_group, my.all_sprites)
        self.direction = direction
        self.speed = 0.2
        self.power = 1
        self.evil = evil

        self.image = MagicBall.imageUp
        self.rect = self.image.get_rect().move(self.evil.rect.x, self.evil.rect.y)

    def move(self):
        if self.direction == 'U':
            self.rect.y -= self.speed * my.cellSize
            self.image = MagicBall.imageUp
        elif self.direction == 'D':
            self.rect.y += self.speed * my.cellSize
            self.image = MagicBall.imageDown
        elif self.direction == 'R':
            self.rect.x += self.speed * my.cellSize
            self.image = MagicBall.imageRight
        elif self.direction == 'L':
            self.rect.x -= self.speed * my.cellSize
            self.image = MagicBall.imageLeft

        obj = pg.sprite.spritecollideany(self, my.player_group)
        if obj is my.player:
            self.to_hurt()
            my.player.removeLifes(self.power)
        elif obj is None:
            if obj is None:
                obj = pg.sprite.spritecollideany(self, my.objects)
            if obj:
                obj.trash()
                self.to_hurt()
                self.evil.wait = False

    def to_hurt(self, damage=None):
        self.evil.wait = False
        my.evil_group.remove(self)
        my.all_sprites.remove(self)




    
    
