# -*- coding:utf-8 -*-

import pygame
import time
from pygame.locals import *
import random


class Base(object):
    """创建基类"""

    def __init__(self, screen, x, y, name):
        '''设置默认值'''
        self.screen = screen
        self.x = x
        self.y = y
        self.name = pygame.image.load(name).convert()  # 加载对象（飞机、子弹）


class PlaneBase(Base):
    """定义飞机的类"""

    def __init__(self, screen, x, y, name):
        '''设置默认值'''
        Base.__init__(self, screen, x, y, name)
        self.plane_bullet_list = []  # 设置列表存子弹对象的引用

    def display(self):
        self.screen.blit(self.name, (self.x, self.y))  # 显示飞机
        # 显示所有子弹，并移动
        for plane_bullet in self.plane_bullet_list:
            plane_bullet.display()
            plane_bullet.move_space()
            # 删除屏幕外子弹
            if plane_bullet.judge():
                self.plane_bullet_list.remove(plane_bullet)


class PlaneHero(PlaneBase):
    """定义一个玩家的类"""

    def __init__(self, screen):
        # 向飞机类玩家传递窗口、位置、图片参数
        PlaneBase.__init__(self, screen, 200, 680, "./feiji/hero.gif")

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def shooting_bullet(self):
        new_plane_bullet = Bullet(self.x, self.y, self.screen)  # 创建玩家子弹对象
        self.plane_bullet_list.append(new_plane_bullet)


class EnemyPlane(PlaneBase):
    """定义一个敌机类"""

    def __init__(self, screen):
        # 向飞机类敌机传递窗口、位置、图片参数
        PlaneBase.__init__(self, screen, 0, 0, "./feiji/enemy-3.gif")
        self.direction = "right"  # 定义一个位置常量

     # 控制敌机的位置
    def move_space(self):
        if self.direction == "right":
            self.x += 2
        elif self.direction == "left":
            self.x -= 2
        if self.x >= 350:
            self.direction = "left"
        elif self.x <= 0:
            self.direction = "right"

    def shooting_bullet(self):
        if random.randint(1, 8) == 5 and random.randint(1, 8) == 3:
            new_plane_bullet = EnemyBullet(
                self.x, self.y, self.screen)  # 创建敌机子弹对象
            self.plane_bullet_list.append(new_plane_bullet)


class BulletBase(Base):
    """定义子弹类"""

    def __init__(self, screen, x, y, name):
        '''设置默认值'''
        Base.__init__(self, screen, x, y, name)

    def display(self):
        self.screen.blit(self.name, (self.x, self.y))  # 显示子弹


class Bullet(BulletBase):
    """定义玩家子弹类"""

    def __init__(self, x, y, screen):
        BulletBase.__init__(self, screen, x + 40, y -
                            30, "./feiji/bullet-3.gif")  # 传参

    def move_space(self):
        self.y -= 2

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyBullet(BulletBase):
    """定义敌机子弹类"""

    def __init__(self, x, y, screen):
        BulletBase.__init__(self, screen, x + 70, y +
                            250, "./feiji/bullet-1.gif")  # 传参

    def move_space(self):
        self.y += 2

    def judge(self):
        if self.y > 850:
            return True
        else:
            return False


def main():
    # 1. 创建窗口
    screen = pygame.display.set_mode((480, 852), 0, 32)

    # 2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png").convert()

    # 3.创建一个飞机
    plane_hero = PlaneHero(screen)

    # 4.创建一个敌机
    plane_enemy = EnemyPlane(screen)

    while True:
        screen.blit(background, (0, 0))  # 显示背景
        plane_hero.display()  # 显示飞机和子弹
        plane_enemy.display()  # 显示敌机
        plane_enemy.move_space()  # 敌机移动
        plane_enemy.shooting_bullet()  # 敌机开火

        # 获取事件，比如按键等
        for event in pygame.event.get():

              # 判断是否是点击了退出按钮
            if event.type == QUIT:
                print("exit")
                exit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    plane_hero.move_left()

              # 检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    plane_hero.move_right()

              # 检测按键是否是空格键
                elif event.key == K_SPACE:
                    print('space')
                    plane_hero.shooting_bullet()  # 射击子弹
        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
