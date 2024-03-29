import pygame as pg
from random import randint
import Game
import Start
import My as my
from Help import cut, Invisible
from Thing import Apple, Knife, Heart, God
from Objects import Water
from Evil import Ghost
from Bullets import AppleBall, FireBall


"""Герой"""


class Hero(pg.sprite.Sprite):

    """
    Герой:
    - Кидается яблоками
    - С помощью кастетов ранит монстров, отбивает файрболы, ломает объекты
    - С помощью сердца восстанавливает жизнь
    - С помощью молитвы:
        * Получает неприкосновенность на время действия молитвы
        * Убивает последнего ранившего его призрака
        * С вероятностью 10% восстанавливает всё здоровье    
    """
    
    image = {'R': pg.image.load('data/hero/right.png'),
             'L': pg.image.load('data/hero/left.png'),
             'U': pg.image.load('data/hero/up.png'),
             'D': pg.image.load('data/hero/down.png'),
             }

    imageRun = {'R': cut(pg.image.load('data/hero/rightRun.png')),
                'L': cut(pg.image.load('data/hero/leftRun.png')),
                'U': cut(pg.image.load('data/hero/upRun.png')),
                'D': cut(pg.image.load('data/hero/downRun.png')),
                }

    imageAttack = {'R': pg.image.load('data/hero/rightAttack.png'),
                   'L': pg.image.load('data/hero/leftAttack.png'),
                   'U': pg.image.load('data/hero/upAttack.png'),
                   'D': pg.image.load('data/hero/downAttack.png'),
                   }

    imageGod = cut(pg.image.load('data/hero/with_god.png'))

    soundRun = pg.mixer.Sound('data/sounds/hero/run.mp3')
    volumeRun = Game.SOUND_VOLUME / 5
    soundRun.set_volume(Game.SOUND_VOLUME / 5)
    soundApple = pg.mixer.Sound('data/sounds/hero/apple.mp3')
    soundApple.set_volume(Game.SOUND_VOLUME)
    soundAttack = pg.mixer.Sound('data/sounds/hero/attack.mp3')
    soundAttack.set_volume(Game.SOUND_VOLUME)
    soundDamage = pg.mixer.Sound('data/sounds/hero/damage.mp3')
    soundDamage.set_volume(Game.SOUND_VOLUME)
    soundLife = pg.mixer.Sound('data/sounds/hero/life.mp3')
    soundLife.set_volume(Game.SOUND_VOLUME)
    soundGod = pg.mixer.Sound('data/sounds/hero/with_god.mp3')
    soundGod.set_volume(Game.SOUND_VOLUME)

    speed = 0.1 * Game.CELL_SIZE
    
    def __init__(self):
        self.hand = None
        self.health = Game.MAX_HEALTH
        self.direction = 'D'
        self.step = 1
        self.run = False
        self.god = False
        self.time = 0
        self.god_time = 0
        self.waitImage = 20
        self.ghost = None

        super().__init__(my.player_group, my.all_sprites)
        self.image = Hero.image['D']
        self.x = Game.H_POS[0]
        self.y = Game.H_POS[1]
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)
        
        self.crHealth()

    def crHealth(self):
        # Создание здоровья
        self.lifes = [Life(self, i * 30) for i in range(self.health)]

    def addLife(self):
        # Добавление жизни
        if self.health < Game.MAX_HEALTH:
            print(f"Hero: +1 hp")
            self.lifes.append(Life(self, self.health * 30))
            self.health += 1
            return True

    def removeLifes(self, damage):
        # Удаление жизни
        if self.god:
            return 0
        print(f"Hero: -{damage} hp")
        if my.sound:
            Hero.soundDamage.play()
        damage = min(self.health, damage)
        for _ in range(damage):
            self.health -= 1
            my.player_group.remove(self.lifes[-1])
            self.lifes.pop(-1)
        if not self.health:
            Start.endGame()

    def move(self):
        # Действие
        self.hand = my.inventory.obj

        # Установка скорости
        speed = Hero.speed
        if my.pressed[pg.K_LSHIFT]:
            speed *= 2

        # Перемещение персонажа
        if my.pressed[pg.K_w] or my.pressed[pg.K_UP]:
            # Шаг вверх
            self.run = True
            self.direction = 'U'
            self.rect.y -= speed
            if self.cant():
                self.rect.y += speed
        if my.pressed[pg.K_s] or my.pressed[pg.K_DOWN]:
            # Шаг вниз
            self.run = True
            self.direction = 'D'
            self.rect.y += speed
            if self.cant():
                self.rect.y -= speed
        if my.pressed[pg.K_a] or my.pressed[pg.K_LEFT]:
            # Шаг влево
            self.run = True
            self.direction = 'L'
            self.rect.x -= speed
            if self.cant():
                self.rect.x += speed
        if my.pressed[pg.K_d] or my.pressed[pg.K_RIGHT]:
            # Шаг вправо
            self.run = True
            self.direction = 'R'
            self.rect.x += speed
            if self.cant():
                self.rect.x -= speed
        if not self.run:
            Hero.soundRun.set_volume(0)
        self.setImage()

    def setImage(self, fight=False):
        # Смена кадра анимации
        if self.god:
            if self.time == Game.TIME:
                self.image = Hero.imageGod[self.step]
                self.step = (self.step + 1) % len(Hero.imageGod)
                self.time = 0
                self.god_time += 1
                if self.god_time == Game.TIME * 7:
                    self.god = False
                    self.endPrayer()
            else:
                self.time += 1
        elif fight:
            self.image = Hero.imageAttack[self.direction]
            self.time = 0
        elif self.run:
            if self.time == Game.TIME:
                if my.sound_run:
                    Hero.soundRun.set_volume(Hero.volumeRun)
                    Hero.soundRun.play() 
                self.image = Hero.imageRun[self.direction][self.step]
                self.step = (
                    self.step + 1) % len(Hero.imageRun[self.direction])
                self.time = 0
            else:
                self.time += 1
        else:
            if self.time == Game.TIME:
                self.image = Hero.image[self.direction]
                self.step = 0
                self.time = 0
            else:
                self.time += 1
        self.run = False

    def used(self):
        # Взаимодействие с объектом
        if not self.run:
            Hero.soundRun.set_volume(0)
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction, my.objects)
        print(f"Hero: used {type(obj).__name__}")
        if obj:
            obj.do()

    def cant(self):
        # Проверка возможности перемещения в клетку
        obj = pg.sprite.spritecollideany(self, my.objects)
        evil = pg.sprite.spritecollideany(self, my.evil_group)
        return (obj or evil and
                pg.sprite.spritecollideany(self, my.evil_group).__class__ != Ghost)

    def do(self):
        # Использование предмета из инвентаря
        if not self.hand:
            return 0
        print(f"Hero: used {type(self.hand).__name__}")
        if self.hand.__class__ is Apple:
            if my.sound:
                Hero.soundApple.play()
            my.inventory.remove(self.hand)
            AppleBall(self.direction)
            my.score += 100
        elif self.hand.__class__ is Knife:
            if my.sound:
                Hero.soundAttack.play()
            self.fight(self.hand.power)
            if randint(1, 10) == 1:
                my.inventory.remove(self.hand)
            my.score += self.hand.power * 100
        elif self.hand.__class__ is Heart:
            if my.sound:
                Hero.soundLife.play()
            if self.addLife():
                my.inventory.remove(self.hand)
            my.score += 400
        elif self.hand.__class__ is God:
            if my.sound:
                Hero.soundGod.play()
            my.inventory.remove(self.hand)
            self.prayer()
            my.score += 600

    def fight(self, power):
        # Атака
        self.setImage(True)
        inv = Invisible(self.x, self.y)
        obj = inv.search(self.direction, my.evil_group)
        if obj:
            print(f"Hero: attacked {type(obj).__name__}")
            if obj.__class__ == FireBall:
                self.addLife()
                obj.back()
            else:
                obj.to_hurt(power)
        else:
            obj = inv.check(my.objects)
            if obj and obj.__class__ != Water:
                print(f"Hero: broke {type(obj).__name__}")
                obj.death()

    def prayer(self):
        print(f"Hero: praying")
        if my.sound_run:
            Hero.soundGod.play() 
        self.step = 0
        self.time = 0
        self.god = True
        self.god_time = 0

    def endPrayer(self):
        if self.ghost:
            self.ghost.death()
            self.ghost = None
        if randint(1, 10) == 1:
            while self.health < Game.MAX_HEALTH:
                self.addLife()


class Life(pg.sprite.Sprite):

    # Единица здоровья героя

    image = pg.image.load('data/heart.png')

    def __init__(self, hero, x):
        super().__init__(my.player_group)
        self.rect = self.image.get_rect().move(x, 0)

    def move(self):
        pass



    
