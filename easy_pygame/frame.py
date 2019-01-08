# coding=utf8
from __future__ import unicode_literals
from EVENT import *
import pygame


class GameObject(object):
    """ 游戏部件基类"""

    def __init__(self):
        self.KILL = False  # 自杀事件,当KILL==True时,frame会删除此部件
        self.frame = None  # 游戏框架

    def __del__(self):
        self.KILL = True

    def Update(self):
        """ GameFrame Add 后调用 """
        pass

    def Show(self):
        """部件显示"""
        pass

    def Event(self, event):
        """ 事件处理
        return 
        True or False 
        """

        return False
        
    def Add(self, gameObj):
        """ 想框架中添加新部件"""
        self.frame.Add(gameObj)


class GameFrame(object):
    """ 游戏框架 """
    

    def debug(self):
        print(self,'---------------')
        print('len(__objetc):',len(self.__object))
        print('__objetc:',self.__object)
        print('__loop:',self.__loop)

    def __init__(self):
        self.__loop = True
        self.__object = []
        self.__name_group = {}

    def Add(self, gameObj, name=None):
        """ Add GameObject"""
        if isinstance(gameObj,GameObject):
            self.__object.append(gameObj)
            gameObj.frame = self
            gameObj.Update()
            if name is not None:
                objs = self.__name_group.get(name, [])
                objs.append(gameObj)
                self.__name_group[name] = objs

        else:
            raise ValueError


    def Call(self, name, fn, *args, **kwargs):
        for obj in self.__name_group.get(name, []):
            getattr(obj, fn)(*args, **kwargs)


    def Kill(self, gameObj):
        """ 移除 gameObj部件"""
        if gameObj and (gameObj in self.__object):
            self.__object.remove(gameObj)

    def Quit(self):
        """ 退出循环 """
        self.__loop = False

    def MainLoop(self):
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


