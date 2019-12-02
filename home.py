# coding: utf-8
# 大本营类
import pygame


# 大本营类
class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.home = pygame.image.load('image/home1.png')
		self.rect = self.home.get_rect()
		self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.alive = True
	# 大本营被摧毁
	def setDead(self):
		self.home = pygame.image.load('image/home.png')
		self.alive = False