# coding: utf-8
# 块类

import pygame
import random


#砖块
class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/brick.png")
        self.rect = self.image.get_rect()
#铁块       
class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)       
        self.image = pygame.image.load("image/iron.png")
        self.rect = self.image.get_rect()

# 草地
class Grass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("image/grass.png")
		self.rect = self.image.get_rect()

#冰
class Ice(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ice = pygame.image.load('image/ice.png')
		self.rect = self.ice.get_rect()


        
class Map():
    def __init__(self, stage):
        self.stage = stage
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.grassGroup = pygame.sprite.Group()       
        self.iceGroup = pygame.sprite.Group()
        # 大本营
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brick.being = True
            self.brickGroup.add(self.brick)
        i = 0   #i是列，j是行
        while i < 25:
            j = 2
            while j < 22:
                flag = random.randint(1, 8)
                if flag == 1 or flag == 2:
                    self.brick1 = Brick()
                    self.brick1.rect.left, self.brick1.rect.top = 3 + (i+1) * 24, 3 + j * 24
                    self.brickGroup.add(self.brick1)
                    self.brick2 = Brick()
                    self.brick2.rect.left, self.brick2.rect.top = 3 + i * 24, 3 + (j+1) * 24
                    self.brickGroup.add(self.brick2)
                    self.brick3 = Brick()
                    self.brick3.rect.left, self.brick3.rect.top = 3 + (i+1) * 24, 3 + (j+1) * 24
                    self.brickGroup.add(self.brick3)
                    self.brick4 = Brick()
                    self.brick4.rect.left, self.brick4.rect.top = 3 + i * 24, 3 + j * 24
                    self.brickGroup.add(self.brick4)
                if flag == 3:
                    self.iron1 = Iron()
                    self.iron1.rect.left, self.iron1.rect.top = 3 + i * 24, 3 + j * 24
                    self.ironGroup.add(self.iron1)
                    self.iron2 = Iron()
                    self.iron2.rect.left, self.iron2.rect.top = 3 + i * 24, 3 + (j+1) * 24
                    self.ironGroup.add(self.iron2)
                    self.iron3 = Iron()
                    self.iron3.rect.left, self.iron3.rect.top = 3 + (i+1) * 24, 3 + j * 24
                    self.ironGroup.add(self.iron3)
                    self.iron4 = Iron()
                    self.iron4.rect.left, self.iron4.rect.top = 3 + (i+1) * 24, 3 + (j+1) * 24
                    self.ironGroup.add(self.iron4)
                if flag == 4:
                    self.grass1 = Grass()
                    self.grass1.rect.left, self.grass1.rect.top = 3 + i * 24, 3 + j * 24
                    self.grassGroup.add(self.grass1)
                    self.grass2 = Grass()
                    self.grass2.rect.left, self.grass2.rect.top = 3 + i * 24, 3 + (j+1) * 24
                    self.grassGroup.add(self.grass2)
                    self.grass3 = Grass()
                    self.grass3.rect.left, self.grass3.rect.top = 3 + (i+1) * 24, 3 + j * 24
                    self.grassGroup.add(self.grass3)
                    self.grass4 = Grass()
                    self.grass4.rect.left, self.grass4.rect.top = 3 + (i+1) * 24, 3 + (j+1) * 24
                    self.grassGroup.add(self.grass4)
                if self.stage >= 10:
                    if flag == 5:
                        self.ice1 = Ice()
                        self.ice1.rect.left, self.ice1.rect.top = 3 + i * 24, 3 + j * 24
                        self.iceGroup.add(self.ice1)
                        self.ice2 = Ice()
                        self.ice2.rect.left, self.ice2.rect.top = 3 + i * 24, 3 + (j+1) * 24
                        self.iceGroup.add(self.ice2)
                        self.ice3 = Ice()
                        self.ice3.rect.left, self.ice3.rect.top = 3 + (i+1) * 24, 3 + j * 24
                        self.iceGroup.add(self.ice3)
                        self.ice4 = Ice()
                        self.ice4.rect.left, self.ice4.rect.top = 3 + (i+1) * 24, 3 + (j+1) * 24
                        self.iceGroup.add(self.ice4)
                j += 2
            i += 2


