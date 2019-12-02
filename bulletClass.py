# coding: utf-8
# 子弹类
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.bulletUp = pygame.image.load("image/bullet_up.png")
        self.bulletDown = pygame.image.load("image/bullet_down.png")
        self.bulletLeft = pygame.image.load("image/bullet_left.png")
        self.bulletRight = pygame.image.load("image/bullet_right.png")

        # 子弹方向 速度 生命 
        self.dir_x, self.dir_y = 0, 0
        self.speed  = 6
        self.life   = False

        self.bullet = self.bulletUp
        self.rect = self.bullet.get_rect()
        self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
    
    def changeImage(self, dir_x, dir_y):
        self.dir_x, self.dir_y = dir_x, dir_y
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet = self.bulletUp
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet = self.bulletDown
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet = self.bulletLeft
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet = self.bulletRight
        

    
    def move(self):
        self.rect = self.rect.move(self.speed * self.dir_x,self.speed * self.dir_y)
        # 碰撞地图边缘
        if self.rect.top < 3:
            self.life = False
        if self.rect.bottom > 630 - 3:
            self.life = False
        if self.rect.left < 3:
            self.life = False
        if self.rect.right > 630 - 3:
            self.life = False