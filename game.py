# -*- coding: utf-8 -*-
#游戏类
import pygame
import sys
import traceback
import block
import myTank
import enemyTank
import home
import music


class Game(object):
    def __init__(self):
        # 默认一个玩家
        self.playerNum = 1
        self.closeMusic = False
        self.isDifficult = False
        self.stage = 0
        self.totalStages = 20
        self.screen = pygame.display.set_mode((630, 630))
        self.isOver = False
        self.time = 0

    #开始界面显示
    def startInterface(self, width, height):
        tfont = pygame.font.Font('font/simkai.ttf', width//4)
        cfont = pygame.font.Font('font/simkai.ttf', width//35)
        title = tfont.render(u'坦克大战', True, (255, 0, 0))
        content1 = cfont.render(u'游戏说明：按1键选择单人游戏，按2键选择双人人游戏', True, (0, 0, 255))
        content2 = cfont.render(u'按3键关闭音效，按4键选择困难模式，设置完毕后按5键进入游戏', True, (0, 0, 255))
        content3 = cfont.render(u'玩家1通过wasd控制方向，空格键发射子弹', True, (0, 0, 255))
        content4 = cfont.render(u'玩家2通过方向键控制方向，小键盘0发射子弹', True, (0, 0, 255))
        content5 = cfont.render(u'每一关我方每辆坦克有3条生命，游戏默认简单模式,困难模式从第10关开始', True, (0, 0, 255))
        trect = title.get_rect()
        trect.midtop = (width/2, height/4)
        crect1 = content1.get_rect()
        crect1.midtop = (width/2, height/1.8)
        crect2 = content2.get_rect()        
        crect2.midtop = (width/2, height/1.6)
        crect3 = content3.get_rect()
        crect3.midtop = (width/2, height/1.5)
        crect4 = content4.get_rect()
        crect4.midtop = (width/2, height/1.4)
        crect5 = content5.get_rect()
        crect5.midtop = (width/2, height/1.3)
        self.screen.blit(title, trect)
        self.screen.blit(content1, crect1)
        self.screen.blit(content2, crect2)
        self.screen.blit(content3, crect3)
        self.screen.blit(content4, crect4)
        self.screen.blit(content5, crect5)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.playerNum = 1
                    if event.key == pygame.K_2:
                        self.playerNum = 2
                    if event.key == pygame.K_3:
                        self.closeMusic = True
                    if event.key == pygame.K_4:
                        self.isDifficult = True
                    if event.key == pygame.K_5:
                        return
    # 结束界面
    def endInterface(self, width, height, isWin, time):
        bgImg = pygame.image.load("image/background.png")
        self.screen.blit(bgImg, (0,0))
        if isWin:
            font = pygame.font.Font('font/simkai.ttf', width//15)
            content = font.render(u'恭喜通关！', True, (255, 0, 0))
            time = time / 1000
            content1 = font.render(u'用时%d秒' % time, True, (255, 0, 0))
            rect = content.get_rect()
            rect.midtop = (width/2, height/2)
            crect1 = content1.get_rect()
            crect1.midtop = (width/2, height/1.8)
            self.screen.blit(content, rect)
            self.screen.blit(content1, crect1)
        else:
            failImg = pygame.image.load("image/gameover.png")
            font = pygame.font.Font('font/simkai.ttf', width//20)
            self.stage -= 1
            content = font.render(u'通过了%d关' % self.stage, True, (255, 0, 0))
            time = time / 1000
            content1 = font.render(u'用时%d秒' % time, True, (255, 0, 0))
            crect = content.get_rect()
            crect.midtop = (width/2, height/2)
            crect1 = content1.get_rect()
            crect1.midtop = (width/2, height/1.8)
            rect = failImg.get_rect()
            rect.midtop = (width/2, height/2.2)
            self.screen.blit(failImg, rect)
            self.screen.blit(content, crect)
            self.screen.blit(content1, crect1)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    # 关卡切换界面
    def switchStage(self, width, height):
        bgImg = pygame.image.load("image/background.png")
        self.screen.blit(bgImg, (0, 0))
        font = pygame.font.Font('font/simkai.ttf', width//10)
        content = font.render(u'第%d关' % self.stage, True, (0, 255, 0))
        rect = content.get_rect()
        rect.midtop = (width/2, height/2)
        self.screen.blit(content, rect)
        pygame.display.update()
        delayEvent = pygame.constants.USEREVENT
        pygame.time.set_timer(delayEvent, 1000)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == delayEvent:
                    return

    def main(self):
        pygame.init()
        pygame.mixer.init()
            
        pygame.display.set_caption("坦克大战")       
        # 背景
        backgroundImage = pygame.image.load("image/background.png")
        self.startInterface(630, 630)
        # 游戏开始的时间
        time1 = pygame.time.get_ticks()
        # 游戏主循环
        while not self.isOver:
            self.stage += 1
            if self.stage > self.totalStages:
                break
            if self.isDifficult:
                self.stage = 10
            self.switchStage(630, 630)
            # 音效
            gameMusic = music.Music()
            if self.closeMusic:
                gameMusic.closeMusic()
            gameMusic.start()
            #该关卡敌方坦克总数量
            totalEnemyTanks = 19 + self.stage
            #场上存在的敌方坦克总数量
            existEnemyTanks = 0
            #场上可以存在的敌方坦克总数量
            canExistEnemyTanks = min(max(self.stage * 2, 4), 8)
            #定义精灵组:坦克，我方坦克，敌方坦克，敌方子弹
            self.allTankGroup = pygame.sprite.Group()
            self.mytankGroup = pygame.sprite.Group()
            self.allEnemyGroup = pygame.sprite.Group()
            self.mediumEnemyGroup = pygame.sprite.Group() #中型坦克
            self.heavyEnemyGroup = pygame.sprite.Group()  #重型坦克
            self.lightEnemyGroup = pygame.sprite.Group()  #轻型坦克
            self.enemyBulletGroup = pygame.sprite.Group()
        
            #创建地图 
            gameMap = block.Map(self.stage)
            #创建我方坦克
            myTank1 = myTank.MyTank(1)
            self.allTankGroup.add(myTank1)
            self.mytankGroup.add(myTank1)
            if self.playerNum != 1:
                myTank2 = myTank.MyTank(2)
                self.allTankGroup.add(myTank2)
                self.mytankGroup.add(myTank2)
            # 创建敌方坦克 
            for i in range(1, 4):
                if totalEnemyTanks > 0:
                    totalEnemyTanks -= 1
                    existEnemyTanks += 1
                    enemy = enemyTank.EnemyTank(i)
                    self.allTankGroup.add(enemy)
                    self.allEnemyGroup.add(enemy)
                    if enemy.kind == 2:
                        self.mediumEnemyGroup.add(enemy)
                        continue
                    if enemy.kind == 3:
                        self.heavyEnemyGroup.add(enemy)
                        continue
                    self.lightEnemyGroup.add(enemy)
            
            
            
            
            # 自定义事件
            # 创建敌方坦克延迟200
            DELAYEVENT = pygame.constants.USEREVENT
            pygame.time.set_timer(DELAYEVENT, 200)
            # 创建敌方子弹延迟1000
            ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
            pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)
            # 创建我方子弹延迟200
            MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
            pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)

            clock = pygame.time.Clock()
            # 大本营
            myhome = home.Home()
            # 关卡主循环
            while True:
                if self.isOver:
                    break
                if totalEnemyTanks < 1 and existEnemyTanks < 1:
                    self.isOver = False
                    break   
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    # 我方子弹冷却事件
                    if event.type == MYBULLETNOTCOOLINGEVENT:
                        myTank1.bulletNotCooling = True
                        if self.playerNum != 1:
                            myTank2.bulletNotCooling = True
                        
                    # 敌方子弹冷却事件
                    if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                        for each in self.allEnemyGroup:
                            each.bulletNotCooling = True
                    
                    # 创建敌方坦克
                    if event.type == DELAYEVENT:
                        if totalEnemyTanks > 0:
                            if existEnemyTanks < canExistEnemyTanks: 
                                enemy = enemyTank.EnemyTank()
                                if pygame.sprite.spritecollide(enemy, self.allTankGroup, False, None):
                                    break
                                self.allEnemyGroup.add(enemy)
                                self.allTankGroup.add(enemy)
                                existEnemyTanks += 1
                                if enemy.kind == 2:
                                    self.mediumEnemyGroup.add(enemy)
                                elif enemy.kind == 3:
                                    self.heavyEnemyGroup.add(enemy)
                                else:
                                    self.lightEnemyGroup.add(enemy)           
                        
                # 检查用户的键盘操作
                key_pressed = pygame.key.get_pressed()
                # 玩家一的移动操作
                myTank1.move1(self.allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
                if key_pressed[pygame.K_SPACE]:
                    if not myTank1.bullet.life and myTank1.bulletNotCooling:
                        gameMusic.fire()
                        myTank1.shoot()
                        myTank1.bulletNotCooling = False
                        
                # 玩家二的移动操作
                if self.playerNum != 1:
                    myTank2.move2(self.allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
                    if key_pressed[pygame.K_KP0]:
                        if not myTank2.bullet.life and myTank2.bulletNotCooling:
                            gameMusic.fire()
                            myTank2.shoot()
                            myTank2.bulletNotCooling = False 
                            
                # 实现各种场景
                self.screen.blit(backgroundImage, (0, 0))
                for each in gameMap.brickGroup:
                    self.screen.blit(each.image, each.rect)        
                for each in gameMap.ironGroup:
                    self.screen.blit(each.image, each.rect)     
                for each in gameMap.grassGroup:
                    self.screen.blit(each.image, each.rect)   
                self.screen.blit(myhome.home, myhome.rect) 
                # 我方坦克1
                print(myTank1.life)
                if myTank1.life > 0:
                    self.screen.blit(myTank1.tank_R0, (myTank1.rect.left, myTank1.rect.top))
                # 我方坦克2
                if self.playerNum != 1: 
                    if myTank2.life > 0:
                        self.screen.blit(myTank2.tank_R0, (myTank2.rect.left, myTank2.rect.top))
                # 敌方坦克
                enemy.cartoon()
                enemy.creatImage(self.allEnemyGroup, self.allTankGroup, self.screen, gameMap.brickGroup, gameMap.ironGroup)
            
                        
                # 我方坦克1子弹
                if myTank1.createBulletImage(self.screen, self.enemyBulletGroup, self.heavyEnemyGroup, self.mediumEnemyGroup, self.lightEnemyGroup, gameMap.brickGroup, gameMap.ironGroup, myhome, gameMusic) == -1:
                    existEnemyTanks -= 1
                    totalEnemyTanks -= 1
                
                # 我方坦克2子弹
                if self.playerNum != 1:
                    if myTank2.createBulletImage(self.screen, self.enemyBulletGroup, self.heavyEnemyGroup, self.mediumEnemyGroup, self.lightEnemyGroup, gameMap.brickGroup, gameMap.ironGroup, myhome, gameMusic) == -1:
                        existEnemyTanks -= 1
                        totalEnemyTanks -= 1

                # 绘制敌人子弹
                if self.playerNum == 1:
                    enemy.createBulletImage(self.screen, self.allEnemyGroup, self.enemyBulletGroup, myTank1, gameMusic, self.playerNum, gameMap, myhome)
                    if myTank1.life == 0 or myhome.alive == False:
                        self.isOver = True
                    
                if self.playerNum != 1:
                    enemy.createBulletImage(self.screen, self.allEnemyGroup, self.enemyBulletGroup, myTank1, gameMusic, self.playerNum, gameMap, myhome, myTank2)
                    if myTank1.life == 0 and myTank2.life == 0:
                        self.isOver = True
                    if myhome.alive == False:
                        self.isOver = True
                
                pygame.display.flip()
                clock.tick(60)
        time2 = pygame.time.get_ticks()
        self.time = time2 - time1
        if not self.isOver:
            self.endInterface(630, 630, True, self.time)
        else:
            self.endInterface(630, 630, False, self.time)
    
    
if __name__ == "__main__":
    game = Game()
    try:
        game.main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()