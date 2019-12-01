import pygame
import random

brickImage          = "image/brick.png"
ironImage           = "image/iron.png"
grassImage          = "image/grass.png"

#砖块
class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(brickImage)
        self.rect = self.image.get_rect()
#铁块       
class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(ironImage)
        self.rect = self.image.get_rect()

# 草地
class Grass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(grassImage)
		self.rect = self.image.get_rect()

#冰
class Ice(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ice = pygame.image.load('image/ice.png')
		self.rect = self.ice.get_rect()
		self.being = False


# 河流
class River(pygame.sprite.Sprite):
	def __init__(self, kind=None):
		pygame.sprite.Sprite.__init__(self)
		if kind is None:
			self.kind = random.randint(0, 1)
		self.rivers = ['image/scene/river1.png', 'image/scene/river2.png']
		self.river = pygame.image.load(self.rivers[self.kind])
		self.rect = self.river.get_rect()
		self.being = False


        
class Map():
    def __init__(self):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup  = pygame.sprite.Group()
        self.grassGroup = pygame.sprite.Group()        

        
        # 数字代表地图中的位置
        # 画砖块
        # X1379 = [2, 3, 6, 7, 18, 19, 22, 23]
        # Y1379 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]
        # X28 = [10, 11, 14, 15]
        # Y28 = [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]
        # X46 = [4, 5, 6, 7, 18, 19, 20, 21]
        # Y46 = [13, 14]
        # X5  = [12, 13]
        # Y5  = [16, 17]
        # X0Y0 = [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]
        # for x in X1379:
        #     for y in Y1379:
        #         self.brick = Brick()
        #         self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #         self.brickGroup.add(self.brick)
        # for x in X28:
        #     for y in Y28:
        #         self.brick = Brick()
        #         self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #         self.brickGroup.add(self.brick)
        # for x in X46:
        #     for y in Y46:
        #         self.brick = Brick()
        #         self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #         self.brickGroup.add(self.brick)
        # for x in X5:
        #     for y in Y5:
        #         self.brick = Brick()
        #         self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #         self.brickGroup.add(self.brick)
        # for x, y in X0Y0:
        #     self.brick = Brick()
        #     self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #     self.brickGroup.add(self.brick)
        
        # # 画石头
        # for x, y in [(0,14),(1,14),(12,6),(13,6),(12,7),(13,7),(24,14),(25,14)]:
            # self.iron = Iron()
            # self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            # self.ironGroup.add(self.iron)

        # directionX = []
        # directionY = []
        # i = 10
        # while i > 0:
        #     directionX.append(random.randint(0 , 25))
        #     directionY.append(random.randint(2 , 23))
        #     i -= 1
        #     # random.randint(a , b)    
        # for x in directionX:
        #     for y in directionY:
        #         self.brick = Brick()
        #         self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        #         self.brickGroup.add(self.brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brick.being = True
            self.brickGroup.add(self.brick)
        i = 0   #i是列，j是行
        while i < 25:
            j = 2
            while j < 23:
                flag = random.randint(1, 30)
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
                    self.iron = Iron()
                    self.iron.rect.left, self.iron.rect.top = 3 + i * 24, 3 + j * 24
                    self.ironGroup.add(self.iron)
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
                j += 1
            i += 1


