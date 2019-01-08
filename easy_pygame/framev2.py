# coding=utf8
from __future__ import unicode_literals
from EVENT import *
import pygame


class GameObject(object):
    """ 游戏部件基类"""

    def __init__(self, x=0, y=0, width=0, height=0):
        # 自杀事件,当KILL==True时,frame会删除此部件
        self.KILL = False
        # 游戏框架
        self.frame = None

        self.surface = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.__objects = []
        self.__name_group = {}
        self.__oid_group = {}

    def __del__(self):
        self.KILL = True

    def update(self):
        pass

    def show(self, screen, x0=0, y0=0):
        """部件显示"""
        if self.surface is not None:
            screen.blit(self.surface, (x0+self.x, y0+self.y))

        for obj in self.__objects:
            obj.show(screen, x0+self.x, y0+self.y)
        pass

    def event(self, evt):
        """ 事件处理
        """
        pass

    def add(self, obj, name=None, oid=None):
        """ 想框架中添加新部件"""
        if isinstance(obj, GameObject):
            self.__objects.append(obj)
            if name is not None:
                objs = self.__name_group.get(name, [])
                objs.append(obj)
                self.__name_group[name] = objs
            if oid is not None:
                self.__oid_group[oid] = obj

    def get(self, name=None, oid=None):
        if oid in self.__oid_group:
            return self.__oid_group[oid]
        return self.__name_group.get(name)

    def isin(self, x, y):
        return self.x < x < self.x+self.width and self.y < y < self.y+self.height


class GameFrame(object):
    """ 游戏框架 """

    def debug(self):
        print(self, '---------------')
        print('len(__objetc):', len(self.__object))
        print('__objetc:', self.__object)
        print('__loop:', self.__loop)

    def __init__(self, screen=None):
        self.__object = []
        self.__loop = True
        self._name_group = {}

    def add(self, game_obj, name=None):
        """ Add GameObject"""
        if isinstance(game_obj, GameObject):
            self.__object.append(game_obj)
            game_obj.frame = self
            if name is not None:
                objs = self._name_group.get(name, [])
                objs.append(game_obj)
                self._name_group[name] = objs
        else:
            raise ValueError

    def call(self, name, fn, *args, **kwargs):
        for obj in self._name_group.get(name, []):
            getattr(obj, fn)(*args, **kwargs)

    def kill(self, obj):
        """ 移除 gameObj部件"""
        if obj in self.__object:
            self.__object.remove(obj)

    def quit(self):
        """ 退出循环 """
        self.__loop = False

    def run(self):
        """ 框架主循环,游戏从这里开始"""
        print("In MainLoop", self)
        while self.__loop:

            # 处理事件
            for event in pygame.event.get():
                for obj in self.__object[::-1]:
                    if obj.KILL:
                        # 移除自杀组件
                        self.__object.remove(obj)

                    if obj.Event(event):
                        # 组件事件处理
                        break

                if event.type == pygame.QUIT:
                    exit()

            # 显示
            for obj in self.__object:
                obj.Show()

            pygame.display.update()


