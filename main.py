# -*- coding: utf-8 -*-

import pygame
import sys
import os
import traceback
import wall
import myTank
import enemyTank
import home
import music




playerNum = 0
closeMusic = False
isDifficult = False
#开始界面显示
def startInterface(screen, width, height):
    global playerNum
    global closeMusic
    global isDifficult
    tfont = pygame.font.Font('font/simkai.ttf', width//4)
    cfont = pygame.font.Font('font/simkai.ttf', width//25)
    pfont = pygame.font.Font('font/simkai.ttf', width//45)
    title = tfont.render(u'坦克大战', True, (255, 0, 0))
    content1 = cfont.render(u'按1键选择单人游戏，按2键选择双人人游戏', True, (0, 0, 255))
    content2 = cfont.render(u'按3键关闭音效，按4键选择困难模式，按5键进入游戏', True, (0, 0, 255))
    content3 = pfont.render(u'游戏说明：我方每辆坦克有3条生命，过一关生命值加1，游戏默认简单模式,困难模式从第10关开始', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (width/2, height/4)
    crect1 = content1.get_rect()
    crect1.midtop = (width/2, height/1.8)
    crect2 = content2.get_rect()        
    crect2.midtop = (width/2, height/1.6)
    crect3 = content3.get_rect()
    crect3.midtop = (width/2, height/1.2)
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
                    playerNum = 1
                if event.key == pygame.K_2:
                    playerNum = 2
                if event.key == pygame.K_3:
                    closeMusic = True
                if event.key == pygame.K_4:
                    isDifficult = True
                if event.key == pygame.K_5:
                    return

def endInterface(screen, width, height, isWin, stage, time):
    bgImg = pygame.image.load("image/background.png")
    screen.blit(bgImg, (0,0))
    if isWin:
        font = pygame.font.Font('font/simkai.ttf', width//10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        time = time / 1000
        content1 = font.render(u'用时%d秒' % time, True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width/2, height/2)
        crect1 = content1.get_rect()
        crect1.midtop = (width/2, height/1.8)
        screen.blit(content, rect)
        screen.blit(content1, crect1)
    else:
        failImg = pygame.image.load("image/gameover.png")
        font = pygame.font.Font('font/simkai.ttf', width//20)
        stage -= 1
        content = font.render(u'通过了%d关' % stage, True, (255, 0, 0))
        time = time / 1000
        content1 = font.render(u'用时%d秒' % time, True, (255, 0, 0))
        crect = content.get_rect()
        crect.midtop = (width/2, height/2)
        crect1 = content1.get_rect()
        crect1.midtop = (width/2, height/1.8)
        rect = failImg.get_rect()
        rect.midtop = (width/2, height/2.2)
        screen.blit(failImg, rect)
        screen.blit(content, crect)
        screen.blit(content1, crect1)
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
    pygame.init()
    pygame.mixer.init()
    
    resolution = 630, 630
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("坦克大战")
    
    # 加载图片,音乐,音效.
    background_image     = pygame.image.load("image/background.png")
    # home_image           = pygame.image.load("image/home.png")
    # home_destroyed_image = pygame.image.load("image/home_destroyed.png")
    
    # bang_sound          = pygame.mixer.Sound("music/bang.wav")
    # bang_sound.set_volume(1)
    # fire_sound           = pygame.mixer.Sound("music/Gunfire.wav")
    # start_sound          = pygame.mixer.Sound("music/start.wav")

    startInterface(screen, 630, 630)
    time1 = pygame.time.get_ticks()
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
        if closeMusic:
            pass
            # start_sound.set_volume(0)
            # bang_sound.set_volume(0)
            # fire_sound.set_volume(0)
        if isDifficult:
            stage = 10
        switchStage(screen, 630, 630, stage)
        gameMusic = music.Music()
        gameMusic.start()
        #该关卡敌方坦克总数量
        totalEnemyTanks = 19 + stage
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
        gameMap = wall.Map()
        #创建我方坦克
        myTank1 = myTank.MyTank(1)
        allTankGroup.add(myTank1)
        mytankGroup.add(myTank1)
        if playerNum != 1:
            myTank2 = myTank.MyTank(2)
            allTankGroup.add(myTank2)
            mytankGroup.add(myTank2)
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
        # appearance_image = pygame.image.load("image/appear.png").convert_alpha()
        # appearance = []
        # appearance.append(appearance_image.subsurface(( 0, 0), (48, 48)))
        # appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
        # appearance.append(appearance_image.subsurface((96, 0), (48, 48)))
        
        
        
        
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
        
        delay = 100
        # existEnemyTanks = 3
        enemyCouldMove      = True
        # switch_R1_R2_image  = True
        homeSurvive         = True
        running_T1          = True
        running_T2          = True
        clock = pygame.time.Clock()

        myhome = home.Home()
        # myhome
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
                    myTank1.bulletNotCooling = True
                    if playerNum != 1:
                        myTank2.bulletNotCooling = True
                    
                # 敌方子弹冷却事件
                if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                    for each in allEnemyGroup:
                        each.bulletNotCooling = True
                
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
                    


            # 检查用户的键盘操作
            key_pressed = pygame.key.get_pressed()
            # 玩家一的移动操作
            myTank1.move1(allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
            # fire = pygame.mixer.Sound("music/Gunfire.wav")
            if key_pressed[pygame.K_SPACE]:
                if not myTank1.bullet.life and myTank1.bulletNotCooling:
                    # fire.play()
                    gameMusic.fire()
                    myTank1.shoot()
                    myTank1.bulletNotCooling = False
                    
            # 玩家二的移动操作
            if playerNum != 1:
                myTank2.move2(allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
                if key_pressed[pygame.K_KP0]:
                    if not myTank2.bullet.life and myTank2.bulletNotCooling:
                        gameMusic.fire()
                        myTank2.shoot()
                        myTank2.bulletNotCooling = False 
            
            
                
            
            
            
            
            # 画背景
            screen.blit(background_image, (0, 0))
            # 画砖块
            for each in gameMap.brickGroup:
                screen.blit(each.image, each.rect)        
            # 画石头
            for each in gameMap.ironGroup:
                screen.blit(each.image, each.rect)     
            #画草地
            for each in gameMap.grassGroup:
                screen.blit(each.image, each.rect)   
            # 画大本营
            screen.blit(myhome.home, myhome.rect)
            # 画我方坦克1
            # if not (delay % 5):
            #     switch_R1_R2_image = not switch_R1_R2_image
            if myTank1.life != 0:
                if running_T1:
                    screen.blit(myTank1.tank_R0, (myTank1.rect.left, myTank1.rect.top))
                    running_T1 = False
                # if switch_R1_R2_image and running_T1:
                #     screen.blit(myTank1.tank_R0, (myTank1.rect.left, myTank1.rect.top))
                #     running_T1 = False
                else:
                    screen.blit(myTank1.tank_R1, (myTank1.rect.left, myTank1.rect.top))
            # 画我方坦克2
            if playerNum != 1: 
                if running_T2:
                    screen.blit(myTank2.tank_R0, (myTank2.rect.left, myTank2.rect.top))
                    running_T2 = False
                # if switch_R1_R2_image and running_T2:
                #     screen.blit(myTank2.tank_R0, (myTank2.rect.left, myTank2.rect.top))
                #     running_T2 = False
                else:
                    screen.blit(myTank2.tank_R1, (myTank2.rect.left, myTank2.rect.top))    
            # 画敌方坦克
            enemy.cartoon()
            enemy.creatImage(allEnemyGroup, allTankGroup, screen, gameMap.brickGroup, gameMap.ironGroup)
            # for each in allEnemyGroup:
            #     # 判断5毛钱特效是否播放            
            #     if each.flash:
            #         #　判断画左动作还是右动作
            #         if switch_R1_R2_image:
            #             screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
            #             if enemyCouldMove:
            #                 allTankGroup.remove(each)
            #                 each.move(allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
            #                 allTankGroup.add(each)
            #         else:
            #             screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
            #             if enemyCouldMove:
            #                 allTankGroup.remove(each)
            #                 each.move(allTankGroup, gameMap.brickGroup, gameMap.ironGroup)
            #                 allTankGroup.add(each)                    
            #     else:
            #         # 播放5毛钱特效
            #         if each.times > 0:
            #             each.times -= 1
            #             if each.times <= 10:
            #                 screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 20:
            #                 screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 30:
            #                 screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 40:
            #                 screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 50:
            #                 screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 60:
            #                 screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 70:
            #                 screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 80:
            #                 screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
            #             elif each.times <= 90:
            #                 screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
            #         if each.times == 0:
            #             each.flash = True
        
                    
            # 绘制我方子弹1
            if myTank1.createBulletImage(screen, enemyBulletGroup, heavyEnemyGroup, mediumEnemyGroup, lightEnemyGroup, gameMap.brickGroup, gameMap.ironGroup, gameMusic) == -1:
                existEnemyTanks -= 1
                totalEnemyTanks -= 1
            
            # if myTank1.bullet.life:
            #     myTank1.bullet.move()    
            #     screen.blit(myTank1.bullet.bullet, myTank1.bullet.rect)
            #     # 子弹 碰撞 子弹
            #     for each in enemyBulletGroup:
            #         if each.life:
            #             if pygame.sprite.collide_rect(myTank1.bullet, each):
            #                 myTank1.bullet.life = False
            #                 each.life = False
            #                 pygame.sprite.spritecollide(myTank1.bullet, enemyBulletGroup, True, None)
            #     # 子弹 碰撞 敌方坦克
            #     # if pygame.sprite.spritecollide(myTank1.bullet, mediumEnemyGroup, True, None):
            #     #     # prop.change()
            #     #     bang_sound.play()
            #     #     existEnemyTanks -= 1
            #     #     myTank1.bullet.life = False
            #     if pygame.sprite.spritecollide(myTank1.bullet,mediumEnemyGroup, False, None):
            #         for each in mediumEnemyGroup:
            #             if pygame.sprite.collide_rect(myTank1.bullet, each):
            #                 if each.life == 1:
            #                     pygame.sprite.spritecollide(myTank1.bullet,mediumEnemyGroup, True, None)
            #                     gameMusic.boom()
            #                     existEnemyTanks -= 1
            #                     totalEnemyTanks -= 1
            #                 elif each.life == 2:
            #                     each.life -= 1
            #                     each.tank = each.enemy_2_1
            #         myTank1.bullet.life = False
            #     elif pygame.sprite.spritecollide(myTank1.bullet,heavyEnemyGroup, False, None):
            #         for each in heavyEnemyGroup:
            #             if pygame.sprite.collide_rect(myTank1.bullet, each):
            #                 if each.life == 1:
            #                     pygame.sprite.spritecollide(myTank1.bullet,heavyEnemyGroup, True, None)
            #                     gameMusic.boom()
            #                     existEnemyTanks -= 1
            #                     totalEnemyTanks -= 1
            #                 elif each.life == 2:
            #                     each.life -= 1
            #                     each.tank = each.enemy_3_0
            #                 elif each.life == 3:
            #                     each.life -= 1
            #                     each.tank = each.enemy_3_2
            #         myTank1.bullet.life = False
            #     elif pygame.sprite.spritecollide(myTank1.bullet, lightEnemyGroup, True, None):
            #         gameMusic.boom()
            #         existEnemyTanks -= 1
            #         totalEnemyTanks -= 1
            #         myTank1.bullet.life = False    
            #     #if pygame.sprite.spritecollide(myTank1.bullet, allEnemyGroup, True, None):
            #     #    bang_sound.play()
            #     #    existEnemyTanks -= 1
            #     #    myTank1.bullet.life = False
            #     # 子弹 碰撞 brickGroup
            #     if pygame.sprite.spritecollide(myTank1.bullet, gameMap.brickGroup, True, None):
            #         myTank1.bullet.life = False
            #         myTank1.bullet.rect.left, myTank1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            #     # 子弹 碰撞 brickGroup
            #     # if myTank1.bullet.strong:
            #     #     if pygame.sprite.spritecollide(myTank1.bullet, gameMap.ironGroup, True, None):
            #     #         myTank1.bullet.life = False
            #     #         myTank1.bullet.rect.left, myTank1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            #     else:    
            #         if pygame.sprite.spritecollide(myTank1.bullet, gameMap.ironGroup, False, None):
            #             myTank1.bullet.life = False
            #             myTank1.bullet.rect.left, myTank1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
            
            # 绘制我方子弹2
            if playerNum != 1:
                if myTank2.createBulletImage(screen, enemyBulletGroup, heavyEnemyGroup, mediumEnemyGroup, lightEnemyGroup, gameMap.brickGroup, gameMap.ironGroup, gameMusic) == -1:
                    existEnemyTanks -= 1
                    totalEnemyTanks -= 1
                # if myTank2.bullet.life:
                #     myTank2.bullet.move()    
                #     screen.blit(myTank2.bullet.bullet, myTank2.bullet.rect)
                #     # 子弹 碰撞 敌方坦克
                #     if pygame.sprite.spritecollide(myTank2.bullet, allEnemyGroup, True, None):
                #         gameMusic.boom()
                #         existEnemyTanks -= 1
                #         totalEnemyTanks -= 1
                #         myTank2.bullet.life = False
                #     # 子弹 碰撞 brickGroup
                #     if pygame.sprite.spritecollide(myTank2.bullet, gameMap.brickGroup, True, None):
                #         myTank2.bullet.life = False
                #         myTank2.bullet.rect.left, myTank2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                #     # 子弹 碰撞 brickGroup
                #     # if myTank2.bullet.strong:
                #     #     if pygame.sprite.spritecollide(myTank2.bullet, gameMap.ironGroup, True, None):
                #     #         myTank2.bullet.life = False
                #     #         myTank2.bullet.rect.left, myTank2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                #     else:    
                #         if pygame.sprite.spritecollide(myTank2.bullet, gameMap.ironGroup, False, None):
                #             myTank2.bullet.life = False
                #             myTank2.bullet.rect.left, myTank2.bullet.rect.right = 3  + 12 * 24, 3 + 24 * 24
            

            # 绘制敌人子弹
            print(myTank1.life)
            if playerNum == 1:
                enemy.createBulletImage(screen, allEnemyGroup, enemyCouldMove, enemyBulletGroup, myTank1, gameMusic, isOver, playerNum, gameMap, myTank2)
                    # print(myTank1.life)
                    # myTank1.life -= 1
                if myTank1.life == 0:
                    isOver = True
                
            if playerNum != 1:
                enemy.createBulletImage(screen, allEnemyGroup, enemyCouldMove, enemyBulletGroup, myTank1, gameMusic, isOver, playerNum, gameMap, myTank2)
                if myTank1.life == 0 and myTank2.life == 0:
                    isover = True
            # for each in allEnemyGroup:
            #     # 如果子弹没有生命，则赋予子弹生命
            #     if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
            #         enemyBulletGroup.remove(each.bullet)
            #         each.shoot()
            #         enemyBulletGroup.add(each.bullet)
            #         each.bulletNotCooling = False
            #     # 如果5毛钱特效播放完毕 并且 子弹存活 则绘制敌方子弹
            #     if each.flash:
            #         if each.bullet.life:
            #             # 如果敌人可以移动
            #             if enemyCouldMove:
            #                 each.bullet.move()
            #             screen.blit(each.bullet.bullet, each.bullet.rect)
            #             # 子弹 碰撞 我方坦克
            #             if pygame.sprite.collide_rect(each.bullet, myTank1):
            #                 gameMusic.boom()
            #                 myTank1.rect.left, myTank1.rect.top = 3 + 8 * 24, 3 + 24 * 24 
            #                 each.bullet.life = False
            #                 myTank1.moving = 0  # 重置移动控制参数
            #                 # for i in range(myTank1.level+1):
            #                 #     myTank1.levelDown()
            #                 myTank1.life -= 1
            #                 if myTank1.life == 0:
            #                     isOver = True
            #             if playerNum != 1:
            #                 if pygame.sprite.collide_rect(each.bullet, myTank2):
            #                     gameMusic.boom()
            #                     myTank2.rect.left, myTank2.rect.top = 3 + 16 * 24, 3 + 24 * 24 
            #                     each.bullet.life = False
            #                     myTank2.life -= 1
            #                     if myTank2.life == 0 and myTank1.life == 0:
            #                         isOver = True
            #             # 子弹 碰撞 brickGroup
            #             if pygame.sprite.spritecollide(each.bullet, gameMap.brickGroup, True, None):
            #                 each.bullet.life = False
            #             # 子弹 碰撞 ironGroup
            #             # if each.bullet.strong:
            #             #     if pygame.sprite.spritecollide(each.bullet, gameMap.ironGroup, True, None):
            #             #         each.bullet.life = False
            #             else:    
            #                 if pygame.sprite.spritecollide(each.bullet, gameMap.ironGroup, False, None):
            #                     each.bullet.life = False
                
            
                        
                
                
                        
            # 延迟
            delay -= 1
            if not delay:
                delay = 100    
            
            pygame.display.flip()
            clock.tick(60)
    time2 = pygame.time.get_ticks()
    time = time2 - time1
    if not isOver:
        endInterface(screen, 630, 630, True, stage, time)
    else:
        endInterface(screen, 630, 630, False, stage, time)
    
    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()