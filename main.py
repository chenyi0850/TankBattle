# -*- coding: utf-8 -*-

import pygame
import sys
import os
import traceback
import wall
import myTank
import enemyTank
# import food
    

#开始界面显示
def startInterface(screen, width, height):
	tfont = pygame.font.Font('font/simkai.ttf', width//4)
	cfont = pygame.font.Font('font/simkai.ttf', width//20)
	title = tfont.render(u'坦克大战', True, (255, 0, 0))
	content1 = cfont.render(u'按1键进入单人游戏', True, (0, 0, 255))
	content2 = cfont.render(u'按2键进入双人人游戏', True, (0, 0, 255))
	content3 = cfont.render(u'按3键关闭音效', True, (0, 0, 255))
	trect = title.get_rect()
	trect.midtop = (width/2, height/4)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/1.8)
	crect2 = content2.get_rect()
	crect2.midtop = (width/2, height/1.6)
	crect3 = content3.get_rect()
	crect3.midtop = (width/2, height/1.4)
	screen.blit(title, trect)
	screen.blit(content1, crect1)
	screen.blit(content2, crect2)
	screen.blit(content3, crect3)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return 1
				if event.key == pygame.K_2:
					return 2
				if event.key == pygame.K_3:
					return 3

def endInterface(screen, width, height, isWin, stage):
    bgImg = pygame.image.load("image/background.png")
    screen.blit(bgImg, (0,0))
    if isWin:
        font = pygame.font.Font('font/simkai.ttf', width//10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(content, rect)
    else:
        failImg = pygame.image.load("gameover.png")
        font = pygame.font.Font('font/simkai.ttf', width//10)
        content = font.render(u'通过了%d关' % stage, True, (255, 0, 0))
        crect = content.get_rect()
        crect.midtop = (width/2, height/1.8)
        rect = failImg.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(failImg, rect)
        screen.blit(content, crect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def switchStage(screen, width, height, stage):
	bgImg = pygame.image.load("image/background.png")
	screen.blit(bgImg, (0, 0))
	font = pygame.font.Font('font/simkai.ttf', width//10)
	content = font.render(u'第%d关' % stage, True, (0, 255, 0))
	rect = content.get_rect()
	rect.midtop = (width/2, height/2)
	screen.blit(content, rect)
	pygame.display.update()
	delayEvent = pygame.constants.USEREVENT
	pygame.time.set_timer(delayEvent, 1000)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == delayEvent:
				return

def main():
    # print(os.getcwd())
    # print(os.path.dirname(os.path.realpath('__file__')))
    pygame.init()
    pygame.mixer.init()
    
    resolution = 630, 630
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("坦克大战")
    
    # 加载图片,音乐,音效.
    background_image     = pygame.image.load("image/background.png")
    home_image           = pygame.image.load("image/home.png")
    home_destroyed_image = pygame.image.load("image/home_destroyed.png")
    
    bang_sound          = pygame.mixer.Sound("music/bang.wav")
    bang_sound.set_volume(1)
    fire_sound           = pygame.mixer.Sound("music/Gunfire.wav")
    start_sound          = pygame.mixer.Sound("music/start.wav")
    start_sound.play()

    playerNum = startInterface(screen, 630, 630)
    # 游戏关卡
    stage = 0
    totalStage = 2

    #游戏是否结束

    isOver = False
    #游戏主循环
    while not isOver:
        stage += 1
        if stage > totalStage:
            break
        switchStage(screen, 630, 630, stage)
        #该关卡敌方坦克总数量
        totalEnemyTanks = min(stage * 18, 80)
        #场上存在的敌方坦克总数量
        existEnemyTanks = 0
        #场上可以存在的敌方坦克总数量
        canExistEnemyTanks = min(max(stage * 2, 4), 8)
    
        # 定义精灵组:坦克，我方坦克，敌方坦克，敌方子弹
        allTankGroup     = pygame.sprite.Group()
        mytankGroup      = pygame.sprite.Group()
        allEnemyGroup    = pygame.sprite.Group()
        mediumEnemyGroup    = pygame.sprite.Group()
        heavyEnemyGroup  = pygame.sprite.Group()
        lightEnemyGroup  = pygame.sprite.Group()  
        enemyBulletGroup = pygame.sprite.Group()
        # 创建地图 
        bgMap = wall.Map()
        # 创建食物/道具 但不显示
        # prop = food.Food()
        # 创建我方坦克
        if playerNum == 1:
            myTank_T1 = myTank.MyTank(1)
            allTankGroup.add(myTank_T1)
            mytankGroup.add(myTank_T1)
        else:
            myTank_T2 = myTank.MyTank(2)
            allTankGroup.add(myTank_T2)
            mytankGroup.add(myTank_T2)
        # 创建敌方 坦克 
        for i in range(1, 4):
            if totalEnemyTanks > 0:
                totalEnemyTanks -= 1
                existEnemyTanks += 1
                enemy = enemyTank.EnemyTank(i)
                allTankGroup.add(enemy)
                allEnemyGroup.add(enemy)
                if enemy.kind == 2:
                    mediumEnemyGroup.add(enemy)
                    continue
                if enemy.kind == 3:
                    heavyEnemyGroup.add(enemy)
                    continue
                lightEnemyGroup.add(enemy)
        # 敌军坦克出现动画
        appearance_image = pygame.image.load("image/appear.png").convert_alpha()
        appearance = []
        appearance.append(appearance_image.subsurface(( 0, 0), (48, 48)))
        appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
        appearance.append(appearance_image.subsurface((96, 0), (48, 48)))
        
        
        
        
        # 自定义事件
        # 创建敌方坦克延迟200
        DELAYEVENT = pygame.constants.USEREVENT
        pygame.time.set_timer(DELAYEVENT, 200)
        # 创建 敌方 子弹延迟1000
        ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)
        # 创建 我方 子弹延迟200
        MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2
        pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)
        # 敌方坦克 静止8000
        # NOTMOVEEVENT = pygame.constants.USEREVENT + 3
        # pygame.time.set_timer(NOTMOVEEVENT, 8000)
        
        
        delay = 100
        moving = 0
        movdir = 0
        moving2 = 0
        movdir2 = 0
        # existEnemyTanks = 3
        enemyCouldMove      = True
        switch_R1_R2_image  = True
        homeSurvive         = True
        running_T1          = True
        running_T2          = True
        clock = pygame.time.Clock()
        # 关卡主循环
        while True:
            if isOver:
                break
            if totalEnemyTanks < 1 and existEnemyTanks < 1:
                isOver = False
                break   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # 我方子弹冷却事件
                if event.type == MYBULLETNOTCOOLINGEVENT:
                    myTank_T1.bulletNotCooling = True
                    
                # 敌方子弹冷却事件
                if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                    for each in allEnemyGroup:
                        each.bulletNotCooling = True
                
                # 敌方坦克静止事件
                # if event.type == NOTMOVEEVENT:
                #     enemyCouldMove = True
                
                # 创建敌方坦克延迟
                if event.type == DELAYEVENT:
                    if totalEnemyTanks > 0:
                        if existEnemyTanks < canExistEnemyTanks: 
                            enemy = enemyTank.EnemyTank()
                            if pygame.sprite.spritecollide(enemy, allTankGroup, False, None):
                                break
                            allEnemyGroup.add(enemy)
                            allTankGroup.add(enemy)
                            existEnemyTanks += 1
                            if enemy.kind == 2:
                                mediumEnemyGroup.add(enemy)
                            elif enemy.kind == 3:
                                heavyEnemyGroup.add(enemy)
                            else:
                                lightEnemyGroup.add(enemy)
                                    
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_c and pygame.KMOD_CTRL:
                #         pygame.quit()
                #         sys.exit()
                
                #     if event.key == pygame.K_e:
                #         myTank_T1.levelUp()
                #     if event.key == pygame.K_q:
                #         myTank_T1.levelDown()
                #     if event.key == pygame.K_3:
                #         myTank_T1.levelUp()
                #         myTank_T1.levelUp()
                #         myTank_T1.level = 3
                #     if event.key == pygame.K_2:
                #         if myTank_T1.speed == 3:
                #             myTank_T1.speed = 24
                #         else:
                #             myTank_T1.speed = 3
                #     if event.key == pygame.K_1:
                #         for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                #             bgMap.brick = wall.Brick()
                #             bgMap.brick.rect.left, bgMap.brick.rect.top = 3 + x * 24, 3 + y * 24
                #             bgMap.brickGroup.add(bgMap.brick)                
                #     if event.key == pygame.K_4:
                #         for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                #             bgMap.iron = wall.Iron()
                #             bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                #             bgMap.ironGroup.add(bgMap.iron)                
                    


            # 检查用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            # 玩家一的移动操作
            if moving:
                moving -= 1
                if movdir == 0:
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 1:
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 2:
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 3:
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                    
            if not moving:
                if key_pressed[pygame.K_w]:
                    moving = 7
                    movdir = 0
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_s]:
                    moving = 7
                    movdir = 1
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_a]:
                    moving = 7
                    movdir = 2
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_d]:
                    moving = 7
                    movdir = 3
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
            if key_pressed[pygame.K_j]:
                if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                    fire_sound.play()
                    myTank_T1.shoot()
                    myTank_T1.bulletNotCooling = False
                    
            # 玩家二的移动操作
            if moving2:
                moving2 -= 1
                if movdir2 == 0:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    running_T2 = True
                if movdir2 == 1:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    running_T2 = True
                if movdir2 == 2:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    running_T2 = True
                if movdir2 == 3:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    running_T2 = True
                    
            if not moving2:
                if key_pressed[pygame.K_UP]:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    moving2 = 7
                    movdir2 = 0
                    running_T2 = True
                elif key_pressed[pygame.K_DOWN]:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    moving2 = 7
                    movdir2 = 1
                    running_T2 = True
                elif key_pressed[pygame.K_LEFT]:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    moving2 = 7
                    movdir2 = 2
                    running_T2 = True
                elif key_pressed[pygame.K_RIGHT]:
                    allTankGroup.remove(myTank_T2)
                    myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                    allTankGroup.add(myTank_T2)
                    moving2 = 7
                    movdir2 = 3
                    running_T2 = True
            if key_pressed[pygame.K_KP0]:
                if not myTank_T2.bullet.life:
                    # fire_sound.play()
                    myTank_T2.shoot()
            
            
            
            
            # 画背景
            screen.blit(background_image, (0, 0))
            # 画砖块
            for each in bgMap.brickGroup:
                screen.blit(each.image, each.rect)        
            # 花石头
            for each in bgMap.ironGroup:
                screen.blit(each.image, each.rect)        
            # 画home
            if homeSurvive:
                screen.blit(home_image, (3 + 12 * 24, 3 + 24 * 24))
            else:
                screen.blit(home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))
            # 画我方坦克1
            if not (delay % 5):
                switch_R1_R2_image = not switch_R1_R2_image
            if switch_R1_R2_image and running_T1:
                screen.blit(myTank_T1.tank_R0, (myTank_T1.rect.left, myTank_T1.rect.top))
                running_T1 = False
            else:
                screen.blit(myTank_T1.tank_R1, (myTank_T1.rect.left, myTank_T1.rect.top))
            # 画我方坦克2
            if playerNum != 1: 
                if switch_R1_R2_image and running_T2:
                    screen.blit(myTank_T2.tank_R0, (myTank_T2.rect.left, myTank_T2.rect.top))
                    running_T2 = False
                else:
                    screen.blit(myTank_T2.tank_R1, (myTank_T2.rect.left, myTank_T2.rect.top))    
            # 画敌方坦克
            for each in allEnemyGroup:
                # 判断5毛钱特效是否播放            
                if each.flash:
                    #　判断画左动作还是右动作
                    if switch_R1_R2_image:
                        screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                        if enemyCouldMove:
                            allTankGroup.remove(each)
                            each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                            allTankGroup.add(each)
                    else:
                        screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                        if enemyCouldMove:
                            allTankGroup.remove(each)
                            each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                            allTankGroup.add(each)                    
                else:
                    # 播放5毛钱特效
                    if each.times > 0:
                        each.times -= 1
                        if each.times <= 10:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 20:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 30:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 40:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 50:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 60:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 70:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 80:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 90:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    if each.times == 0:
                        each.flash = True
        
                    
            # 绘制我方子弹1
            if myTank_T1.bullet.life:
                myTank_T1.bullet.move()    
                screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)
                # 子弹 碰撞 子弹
                for each in enemyBulletGroup:
                    if each.life:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            myTank_T1.bullet.life = False
                            each.life = False
                            pygame.sprite.spritecollide(myTank_T1.bullet, enemyBulletGroup, True, None)
                # 子弹 碰撞 敌方坦克
                # if pygame.sprite.spritecollide(myTank_T1.bullet, mediumEnemyGroup, True, None):
                #     # prop.change()
                #     bang_sound.play()
                #     existEnemyTanks -= 1
                #     myTank_T1.bullet.life = False
                if pygame.sprite.spritecollide(myTank_T1.bullet,mediumEnemyGroup, False, None):
                    for each in mediumEnemyGroup:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            if each.life == 1:
                                pygame.sprite.spritecollide(myTank_T1.bullet,mediumEnemyGroup, True, None)
                                bang_sound.play()
                                existEnemyTanks -= 1
                                totalEnemyTanks -= 1
                            elif each.life == 2:
                                each.life -= 1
                                each.tank = each.enemy_2_1
                    myTank_T1.bullet.life = False
                elif pygame.sprite.spritecollide(myTank_T1.bullet,heavyEnemyGroup, False, None):
                    for each in heavyEnemyGroup:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            if each.life == 1:
                                pygame.sprite.spritecollide(myTank_T1.bullet,heavyEnemyGroup, True, None)
                                bang_sound.play()
                                existEnemyTanks -= 1
                                totalEnemyTanks -= 1
                            elif each.life == 2:
                                each.life -= 1
                                each.tank = each.enemy_3_0
                            elif each.life == 3:
                                each.life -= 1
                                each.tank = each.enemy_3_2
                    myTank_T1.bullet.life = False
                elif pygame.sprite.spritecollide(myTank_T1.bullet, lightEnemyGroup, True, None):
                    bang_sound.play()
                    existEnemyTanks -= 1
                    totalEnemyTanks -= 1
                    myTank_T1.bullet.life = False    
                #if pygame.sprite.spritecollide(myTank_T1.bullet, allEnemyGroup, True, None):
                #    bang_sound.play()
                #    existEnemyTanks -= 1
                #    myTank_T1.bullet.life = False
                # 子弹 碰撞 brickGroup
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                # 子弹 碰撞 brickGroup
                if myTank_T1.bullet.strong:
                    if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, True, None):
                        myTank_T1.bullet.life = False
                        myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                else:    
                    if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                        myTank_T1.bullet.life = False
                        myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            
            # 绘制我方子弹2
            if playerNum != 1:
                if myTank_T2.bullet.life:
                    myTank_T2.bullet.move()    
                    screen.blit(myTank_T2.bullet.bullet, myTank_T2.bullet.rect)
                    # 子弹 碰撞 敌方坦克
                    if pygame.sprite.spritecollide(myTank_T2.bullet, allEnemyGroup, True, None):
                        bang_sound.play()
                        existEnemyTanks -= 1
                        totalEnemyTanks -= 1
                        myTank_T2.bullet.life = False
                    # 子弹 碰撞 brickGroup
                    if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.brickGroup, True, None):
                        myTank_T2.bullet.life = False
                        myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                    # 子弹 碰撞 brickGroup
                    if myTank_T2.bullet.strong:
                        if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, True, None):
                            myTank_T2.bullet.life = False
                            myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                    else:    
                        if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, False, None):
                            myTank_T2.bullet.life = False
                            myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            

            # 绘制敌人子弹
            for each in allEnemyGroup:
                # 如果子弹没有生命，则赋予子弹生命
                if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                    enemyBulletGroup.remove(each.bullet)
                    each.shoot()
                    enemyBulletGroup.add(each.bullet)
                    each.bulletNotCooling = False
                # 如果5毛钱特效播放完毕 并且 子弹存活 则绘制敌方子弹
                if each.flash:
                    if each.bullet.life:
                        # 如果敌人可以移动
                        if enemyCouldMove:
                            each.bullet.move()
                        screen.blit(each.bullet.bullet, each.bullet.rect)
                        # 子弹 碰撞 我方坦克
                        if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                            bang_sound.play()
                            myTank_T1.rect.left, myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            moving = 0  # 重置移动控制参数
                            for i in range(myTank_T1.level+1):
                                myTank_T1.levelDown()
                        if playerNum != 1:
                            if pygame.sprite.collide_rect(each.bullet, myTank_T2):
                                bang_sound.play()
                                myTank_T2.rect.left, myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24 
                                each.bullet.life = False
                        # 子弹 碰撞 brickGroup
                        if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                            each.bullet.life = False
                        # 子弹 碰撞 ironGroup
                        if each.bullet.strong:
                            if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, True, None):
                                each.bullet.life = False
                        else:    
                            if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                                each.bullet.life = False
                
            
                        
                
                
                        
            # 延迟
            delay -= 1
            if not delay:
                delay = 100    
            
            pygame.display.flip()
            clock.tick(60)
    if not isOver:
        endInterface(screen, 630, 630, True, stage)
    else:
        endInterface(screen, 630, 630, False, stage)
    
    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()