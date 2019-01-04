# coding=utf8
from __future__ import unicode_literals
from EVENT import *
from frame import GameObject
import pygame


class Button(GameObject):
    """
    按钮
    点击时触发 Button.Click() 函数
    """

    def Click(self):
        pass

    def __init__(self, screen, pos, style, ID=None):
        """
        screen
        pos
        style=pygame.Surface 按钮样式
        """
        GameObject.__init__(self)

        self.ID = ID
        self.screen = screen
        self.pos = pos
        self.size = style.get_size()
        self.button = style

    def Show(self):
        self.screen.blit(self.button, self.pos)

    def __isin(self, (x, y)):
        xs, ys = self.pos
        w, h = self.size
        if xs < x < xs+w and ys < y < ys + h:
            return True
    
        return False
        
    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_DOWN:
            if self.__isin(event.pos):
                self.Click()
                return True
        return False

