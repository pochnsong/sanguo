# coding=utf8
from __future__ import unicode_literals
import pygame
from EVENT import *
from frame import GameObject


class Grid(GameObject):
    """
    网格
    """

    def __init__(self, screen, pos, cols, rows=-1):
        """
        """
        GameObject.__init__(self)

        self.screen = screen
        self.pos = pos

    def Show(self):
        self.screen.blit(self.button, self.pos)

    def __isin(self, (x, y)):
        xs, ys = self.pos
        w, h = self.size
        if xs < x < xs + w and ys < y < ys + h:
            return True

        return False

    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_DOWN:
            if self.__isin(event.pos):
                self.Click()
                return True
        return False

