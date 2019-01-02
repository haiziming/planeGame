"""
projent:pygame_planeGane
author:mihon.zhong
dependence:
    1.python
    2.pygame
direction:
    利用pygame简单实现打飞机大战游戏
"""
import pygame
from pygame.locals import *
from sys import exit
from random import randint

#玩家类
class Hero(pygame.sprite.Sprite):
   
    def __init__(self, hero_surface, hero_init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_position
        self.speed = 8
        self.is_hit = False
        self.bullets1 = pygame.sprite.Group()
        self.init_shoot = 18
        
        
    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        if x <0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
    
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y
    
    def single_shoot(self, bullet_suface):
        bullet = Bullet(bullet_suface, self.rect.midtop)
        self.bullets1.add(bullet)
    
 
#子弹类 
class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullet_suface,bullet_init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_suface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_position
        self.speed = 18
        
    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < -self.rect.height:
            self.kill()
    
#敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_surface,enemy_init_position,level,hp):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_position
        self.speed = 2
        self.index = 0
        self.level = level
        self.hp = hp
        
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#空投子弹类            
class Ufo(pygame.sprite.Sprite):
    def __init__(self,bomb_surface,bomb_init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bomb_init_position
        self.speed = 2
    
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#空投速度类
class Ufo2(pygame.sprite.Sprite):
    def __init__(self,ufo2_surface,ufo2_init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo2_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = ufo2_init_position
        self.speed = 2
        
    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            
            
#界面长宽，帧频率            
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
FRAME_RATE = 60
ANIMATE_CYCLE = 900
score = 0
ticks = 0
LEVEL = 1

#按键
offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('This is my first dialog')

#加载图片
background = pygame.image.load('resources/image/background.png')
shoot_img = pygame.image.load('resources/image/shoot.png')
gameover = pygame.image.load('resources/image/gameover.png')

#玩家机舰
hero_surface = []
hero_surface.append(shoot_img.subsurface(pygame.Rect(0, 99, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 360, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(165, 234, 102, 126))) 
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 624, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(330, 498, 102, 126)))
hero_surface.append(shoot_img.subsurface(pygame.Rect(432, 624, 102, 126)))
hero_position = [200, 500]
hero_down_index = 1

bullet_suface = shoot_img.subsurface(pygame.Rect(1004, 987, 9, 21))
ufo_surface = shoot_img.subsurface(pygame.Rect(102, 118, 60, 107))
ufo2_surface = shoot_img.subsurface(pygame.Rect(267, 398, 58, 88))
#一级敌机
enemy_surface = shoot_img.subsurface(pygame.Rect(534, 612, 57, 43))
#二级敌机
enemy_surface_2 = shoot_img.subsurface(pygame.Rect(0, 0, 69, 99))


#一级敌机销毁
enemy_kill_surface = []
enemy_kill_surface.append(shoot_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_kill_surface.append(shoot_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_kill_surface.append(shoot_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_kill_surface.append(shoot_img.subsurface(pygame.Rect(930, 697, 57, 43)))

#二级敌机销毁
enemy_kill_surface_2 = []
enemy_kill_surface_2.append(shoot_img.subsurface(pygame.Rect(534, 655, 69, 95)))
enemy_kill_surface_2.append(shoot_img.subsurface(pygame.Rect(603, 655, 69, 95)))
enemy_kill_surface_2.append(shoot_img.subsurface(pygame.Rect(672, 653, 69, 95)))
enemy_kill_surface_2.append(shoot_img.subsurface(pygame.Rect(741, 653, 69, 95)))

#二级敌机击中
enemy_hit_surface_2 = shoot_img.subsurface(pygame.Rect(432, 525, 69, 99))


hero = Hero(hero_surface[0],hero_position)
enemy_group = pygame.sprite.Group()
enemy_kill_group = pygame.sprite.Group()
enemy_hit_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
ufo2_group = pygame.sprite.Group()

clock = pygame.time.Clock()

enemy_surface = enemy_surface
enemy_kill_surface = enemy_kill_surface

enemy_surface_dic = {
    1:{'enemy_surface':enemy_surface,'enemy_kill_surface':enemy_kill_surface},
    2:{'enemy_surface':enemy_surface_2,'enemy_kill_surface':enemy_kill_surface_2}
}

while True:
    if score >= 20:
        LEVEL = 2

    clock.tick(FRAME_RATE)
    screen.blit(background, (0,0))
    
    if ticks >= ANIMATE_CYCLE:
        ticks = 0
    #print(ticks,ticks//(ANIMATE_CYCLE//2))
    #hero.image = hero_surface[ticks//(ANIMATE_CYCLE//2)]
    if hero.is_hit:
         if ticks%(ANIMATE_CYCLE//60) == 0:
             hero_down_index += 1
         hero.image = hero_surface[hero_down_index]
         if hero_down_index == 5:
             break
    else:
         #hero.image = hero_surface[ticks//(ANIMATE_CYCLE//60)]
         hero.image = hero_surface[0 if ticks%30 > 15 else 1]
         
    if ticks %(hero.init_shoot) == 0:
        hero.single_shoot(bullet_suface)     
    hero.bullets1.update()
    hero.bullets1.draw(screen)
    
    if ticks %30 == 0:
        enemy = Enemy(enemy_surface_dic[LEVEL]['enemy_surface'],
                    [randint(0, SCREEN_WIDTH - enemy_surface_dic[LEVEL]['enemy_surface'].get_width()),
                    -enemy_surface_dic[LEVEL]['enemy_surface'].get_height()], LEVEL, LEVEL)
        enemy_group.add(enemy)
    enemy_group.update()
    enemy_group.draw(screen)
    
    if ticks %900 == 899:
        ufo = Ufo(ufo_surface, [randint(0, SCREEN_WIDTH - ufo_surface.get_width()), -ufo_surface.get_height()])
        ufo_group.add(ufo)
    ufo_group.update()
    ufo_group.draw(screen)
    
    if ticks %900 == 455:
        ufo2 = Ufo2(ufo2_surface, [randint(0, SCREEN_WIDTH - ufo2_surface.get_width()), -ufo2_surface.get_height()])
        ufo2_group.add(ufo2)
    ufo2_group.update()
    ufo2_group.draw(screen)
    
    #如果这里能捕捉到enemy对象就很好
    enemy_objs = pygame.sprite.groupcollide(enemy_group,hero.bullets1,True,True)
    for enemy_obj in enemy_objs:
        
        enemy_obj.hp -= 1
        if enemy_obj.hp == 0:
            enemy_kill_group.add(enemy_obj)
        else:
            enemy = Enemy(enemy_hit_surface_2,enemy_obj.rect.topleft, LEVEL, enemy_obj.hp)
            enemy_group.add(enemy)
            enemy_group.remove(enemy_obj)
            
    #enemy_kill_group.add(pygame.sprite.groupcollide(enemy_group,hero.bullets1,False,True))
    
    
    #敌机摧毁
    for enemy_kill in enemy_kill_group:
        screen.blit(enemy_surface_dic[enemy_kill.level]['enemy_kill_surface'][enemy_kill.index], enemy_kill.rect)
        if ticks % (ANIMATE_CYCLE//200) ==0:
            if enemy_kill.index < 3:
                enemy_kill.index += 1
            else:
                score += 1
                enemy_kill_group.remove(enemy_kill)

#    #100分后敌机速度+2
#    if score >= 20:
#        for enemy in enemy_group:
#            enemy.speed = 4

    
    #玩家机舰摧毁
    enemy_down_list = pygame.sprite.spritecollide(hero, enemy_group, True)
    if len(enemy_down_list) > 0: 
        enemy_kill_group.add(enemy_down_list)
        hero.is_hit = True
       
    #吃到空投+子弹速度
    ufo_dowm_list = pygame.sprite.spritecollide(hero, ufo_group, True)
    if len(ufo_dowm_list) > 0:
        if hero.init_shoot// 2 > 5:
            hero.init_shoot //= 2
        else:
            hero.init_shoot = 6
    
    #吃到空投+移动速度
    ufo2_dowm_list = pygame.sprite.spritecollide(hero, ufo2_group, True)
    if len(ufo2_dowm_list) > 0:
        if hero.speed < 20:
            hero.speed += 5
        else:
            hero.speed = 20
    
    screen.blit(hero.image, hero.rect)
    ticks += 1
    
    #绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render('score: '+str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = hero.speed
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
    
    hero.move(offset)
                
screen.blit(gameover, (0, 0))
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()    
        
        
