# -*- coding: utf-8 -*-
#敌方坦克类

import pygame
import random
import bulletClass



class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x = None, kind = None):
        pygame.sprite.Sprite.__init__(self)
        
        # 坦克出现前动画是否播放
        self.flash = False
        self.times = 90
        # 参数:坦克种类      
        self.kind = kind
        if not kind:
            self.kind = random.choice([1, 2, 3])     
            
        # 选择敌军坦克种类        
        if self.kind == 1:
            self.enemy_x_0 = pygame.image.load("image/enemy_2_0.png").convert_alpha()
        if self.kind == 2:
            self.enemy_x_0 = pygame.image.load("image/enemy_1_1.png").convert_alpha()
        if self.kind == 3:
            self.enemy_x_0 = pygame.image.load("image/enemy_3_3.png").convert_alpha()
        self.enemy_2_1 = pygame.image.load("image/enemy_1_0.png").convert_alpha()
        self.enemy_3_0 = pygame.image.load("image/enemy_3_0.png").convert_alpha()
        self.enemy_3_2 = pygame.image.load("image/enemy_3_2.png").convert_alpha()
        self.tank = self.enemy_x_0
        # 参数:坦克生成位置
        self.x = x
        if not self.x:
            self.x = random.choice([1, 2, 3])
        self.x -= 1
        # 坦克图片
        self.tank_R0 = self.tank.subsurface(( 0, 48), (48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3 + 0 * 24
        
        # 坦克方向
        self.dir_x, self.dir_y = 0, 1
        self.bulletNotCooling = True
        self.bullet = bulletClass.Bullet()
        # 是否撞墙，撞墙则改变方向
        self.dirChange = False
        
        # 每种坦克不同的属性
        if self.kind == 1:
            self.life = 1
            self.speed = 3
        if self.kind == 2:
            self.life = 2
            self.speed = 2
        if self.kind == 3:#无需修改
            self.life = 3
            self.speed = 1
        
    def shoot(self):
        # 赋予子弹生命
        self.bullet.life = True
        self.bullet.changeImage(self.dir_x, self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top + 1
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom - 1
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
    
    def move(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * self.dir_x, self.speed * self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.tank_R0 = self.tank.subsurface(( 0, 0),(48, 48))
        elif self.dir_x == 0 and self.dir_y == 1:
            self.tank_R0 = self.tank.subsurface(( 0, 48),(48, 48))
        elif self.dir_x == -1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 96),(48, 48))
        elif self.dir_x == 1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 144),(48, 48))
        
        
        # 碰撞地图边缘
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        # 碰撞墙体 和坦克
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None) \
            or pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.dir_x, self.speed * -self.dir_y)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))

    def cartoon(self):
        self.appearance_image = pygame.image.load("image/appear.png").convert_alpha()
        self.appearance = []
        self.appearance.append(self.appearance_image.subsurface(( 0, 0), (48, 48)))
        self.appearance.append(self.appearance_image.subsurface((48, 0), (48, 48)))
        self.appearance.append(self.appearance_image.subsurface((96, 0), (48, 48)))

    def creatImage(self, allEnemyGroup, allTankGroup, screen, brickGroup, ironGroup):

        for each in allEnemyGroup:
            # 特效是否播放            
            if each.flash:
                #　实现动画效果
                screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                allTankGroup.remove(each)
                each.move(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(each)                
            else:
                # 播放特效
                if each.times > 0:
                    each.times -= 1
                    if each.times <= 10:
                        screen.blit(self.appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 20:
                        screen.blit(self.appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 30:
                        screen.blit(self.appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 40:
                        screen.blit(self.appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 50:
                        screen.blit(self.appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 60:
                        screen.blit(self.appearance[0], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 70:
                        screen.blit(self.appearance[2], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 80:
                        screen.blit(self.appearance[1], (3 + each.x * 12 * 24, 3))
                    elif each.times <= 90:
                        screen.blit(self.appearance[0], (3 + each.x * 12 * 24, 3))
                if each.times == 0:
                    each.flash = True

    def createBulletImage(self, screen, allEnemyGroup, enemyBulletGroup, myTank1, gameMusic, playerNum, gameMap, myhome, myTank2 = None):
        for each in allEnemyGroup:
            # 如果子弹没有生命，则赋予子弹生命
            if not each.bullet.life and each.bulletNotCooling:
                enemyBulletGroup.remove(each.bullet)
                each.shoot()
                enemyBulletGroup.add(each.bullet)
                each.bulletNotCooling = False
            # 如果特效播放完毕并且子弹存活,则绘制敌方子弹
            if each.flash:
                if each.bullet.life:
                    # 如果敌人可以移动
                    each.bullet.move()
                    screen.blit(each.bullet.bullet, each.bullet.rect)
                    # 子弹碰撞我方坦克
                    if playerNum == 1:
                        if pygame.sprite.collide_rect(each.bullet, myTank1):
                            gameMusic.boom()
                            myTank1.rect.left, myTank1.rect.top = 3 + 8 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            myTank1.moving = 0  # 重置移动控制参数
                            myTank1.life -= 1
                    else:
                        if pygame.sprite.collide_rect(each.bullet, myTank1):
                            gameMusic.boom()
                            myTank1.rect.left, myTank1.rect.top = 3 + 8 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            myTank1.moving = 0  # 重置移动控制参数
                            myTank1.life -= 1
                        if pygame.sprite.collide_rect(each.bullet, myTank2):
                            gameMusic.boom()
                            myTank2.rect.left, myTank2.rect.top = 3 + 16 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            myTank2.moving = 0
                            myTank2.life -= 1
                    # 子弹碰撞砖块
                    if pygame.sprite.spritecollide(each.bullet, gameMap.brickGroup, True, None):
                        each.bullet.life = False
                    # 子弹碰撞铁块
                    else:    
                        if pygame.sprite.spritecollide(each.bullet, gameMap.ironGroup, False, None):
                            each.bullet.life = False
                    #子弹碰撞大本营
                    if pygame.sprite.collide_rect(each.bullet, myhome):
                        each.bullet.life = False
                        myhome.setDead()
						