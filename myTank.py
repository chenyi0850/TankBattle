import pygame
import bulletClass
import music


       

class MyTank(pygame.sprite.Sprite):
    def __init__(self, playerNumber):
        pygame.sprite.Sprite.__init__(self)
        
        # 玩家生命
        self.moving = 0
        self.moveDirection = 0
        self.life = 3

        if playerNumber == 1:
            self.tank_L0_image = pygame.image.load("image/tank_T1_0.png").convert_alpha()
        if playerNumber == 2:
            self.tank_L0_image = pygame.image.load("image/tank_T2_0.png").convert_alpha()
        self.tank = self.tank_L0_image
        
        # 坦克图片
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        self.rect = self.tank_R0.get_rect()
        if playerNumber == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24 
        if playerNumber == 2:
            self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24 
        
        # 坦克速度   坦克方向   坦克生命   子弹冷却
        self.speed = 3
        self.dir_x, self.dir_y = 0, -1
        self.life = 3
        self.bulletNotCooling = True
        self.bullet = bulletClass.Bullet()
    
    def shoot(self):
        # 子弹
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
    
        
        
    #返回True代表发生碰撞
    def moveUp(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * 0, self.speed * -1)
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        self.dir_x, self.dir_y = 0, -1
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        return False
    def moveDown(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * 0, self.speed * 1)
        self.tank_R0 = self.tank.subsurface((0, 48),(48, 48))
        self.dir_x, self.dir_y = 0, 1
        if self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        return False
    def moveLeft(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * -1, self.speed * 0)
        self.tank_R0 = self.tank.subsurface((0, 96),(48, 48))
        self.dir_x, self.dir_y = -1, 0
        if self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        return False
    def moveRight(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * 1, self.speed * 0)
        self.tank_R0 = self.tank.subsurface((0, 144),(48, 48))
        self.dir_x, self.dir_y = 1, 0
        if self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        return False

    #坦克1的移动
    def move1(self, allTankGroup, brickGroup, ironGroup):
        key_pressed = pygame.key.get_pressed()
        if self.moving:
            self.moving -= 1
            if self.moveDirection == 0:
                allTankGroup.remove(self)
                if self.moveUp(allTankGroup, brickGroup, ironGroup):
                    self.moving += 1
                allTankGroup.add(self)
            if self.moveDirection == 1:
                allTankGroup.remove(self)
                if self.moveDown(allTankGroup, brickGroup, ironGroup):
                    self.moving += 1
                allTankGroup.add(self)
            if self.moveDirection == 2:
                allTankGroup.remove(self)
                if self.moveLeft(allTankGroup, brickGroup, ironGroup):
                    self.moving += 1
                allTankGroup.add(self)
            if self.moveDirection == 3:
                allTankGroup.remove(self)
                if self.moveRight(allTankGroup, brickGroup, ironGroup):
                    self.moving += 1
                allTankGroup.add(self)
                
        if not self.moving:
            if key_pressed[pygame.K_w]:
                self.moving = 7
                self.moveDirection = 0
                allTankGroup.remove(self)
                if self.moveUp(allTankGroup, brickGroup, ironGroup):
                    self.moving = 0
                allTankGroup.add(self)
            elif key_pressed[pygame.K_s]:
                self.moving = 7
                self.moveDirection = 1
                allTankGroup.remove(self)
                if self.moveDown(allTankGroup, brickGroup, ironGroup):
                    self.moving = 0
                allTankGroup.add(self)
            elif key_pressed[pygame.K_a]:
                self.moving = 7
                self.moveDirection = 2
                allTankGroup.remove(self)
                if self.moveLeft(allTankGroup, brickGroup, ironGroup):
                    self.moving = 0
                allTankGroup.add(self)
            elif key_pressed[pygame.K_d]:
                self.moving = 7
                self.moveDirection = 3
                allTankGroup.remove(self)
                if self.moveRight(allTankGroup, brickGroup, ironGroup):
                    self.moving = 0
                allTankGroup.add(self)
    #坦克2的移动
    def move2(self, allTankGroup, brickGroup, ironGroup):
        key_pressed = pygame.key.get_pressed()
        if self.moving:
            self.moving -= 1
            if self.moveDirection == 0:
                allTankGroup.remove(self)
                self.moveUp(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
            if self.moveDirection == 1:
                allTankGroup.remove(self)
                self.moveDown(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
            if self.moveDirection == 2:
                allTankGroup.remove(self)
                self.moveLeft(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
            if self.moveDirection == 3:
                allTankGroup.remove(self)
                self.moveRight(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
                
        if not self.moving:
            if key_pressed[pygame.K_UP]:
                allTankGroup.remove(self)
                self.moveUp(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
                self.moving = 7
                self.moveDirection = 0
            elif key_pressed[pygame.K_DOWN]:
                allTankGroup.remove(self)
                self.moveDown(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
                self.moving = 7
                self.moveDirection = 1
            elif key_pressed[pygame.K_LEFT]:
                allTankGroup.remove(self)
                self.moveLeft(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
                self.moving = 7
                self.moveDirection = 2
            elif key_pressed[pygame.K_RIGHT]:
                allTankGroup.remove(self)
                self.moveRight(allTankGroup, brickGroup, ironGroup)
                allTankGroup.add(self)
                self.moving = 7
                self.moveDirection = 3

    def createBulletImage(self, screen, enemyBulletGroup, heavyEnemyGroup, mediumEnemyGroup, lightEnemyGroup, brickGroup, ironGroup, myhome, gameMusic):
        if self.bullet.life:
            self.bullet.move()    
            screen.blit(self.bullet.bullet, self.bullet.rect)
            # 子弹碰撞子弹
            for each in enemyBulletGroup:
                if each.life:
                    if pygame.sprite.collide_rect(self.bullet, each):
                        self.bullet.life = False
                        each.life = False
                        pygame.sprite.spritecollide(self.bullet, enemyBulletGroup, True, None)
            # 子弹碰撞敌方坦克
            if pygame.sprite.spritecollide(self.bullet,mediumEnemyGroup, False, None):
                for each in mediumEnemyGroup:
                    if pygame.sprite.collide_rect(self.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(self.bullet,mediumEnemyGroup, True, None)
                            gameMusic.boom()
                            return -1
                        elif each.life == 2:
                            each.life -= 1
                            each.tank = each.enemy_2_1
                self.bullet.life = False
            elif pygame.sprite.spritecollide(self.bullet,heavyEnemyGroup, False, None):
                for each in heavyEnemyGroup:
                    if pygame.sprite.collide_rect(self.bullet, each):
                        if each.life == 1:
                            pygame.sprite.spritecollide(self.bullet,heavyEnemyGroup, True, None)
                            gameMusic.boom()
                            return -1
                        elif each.life == 2:
                            each.life -= 1
                            each.tank = each.enemy_3_0
                        elif each.life == 3:
                            each.life -= 1
                            each.tank = each.enemy_3_2
                self.bullet.life = False
            elif pygame.sprite.spritecollide(self.bullet, lightEnemyGroup, True, None):
                gameMusic.boom()
                self.bullet.life = False    
                return -1
            # 子弹碰撞砖块
            if pygame.sprite.spritecollide(self.bullet, brickGroup, True, None):
                self.bullet.life = False
                self.bullet.rect.left, self.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            #子弹碰撞铁块
            else:    
                if pygame.sprite.spritecollide(self.bullet, ironGroup, False, None):
                    self.bullet.life = False
                    self.bullet.rect.left, self.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            #子弹碰撞大本营
            if pygame.sprite.collide_rect(self.bullet, myhome):
                self.bullet.life = False
                myhome.setDead()