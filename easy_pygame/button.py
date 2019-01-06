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


class TextButton(Button):
    
    def __trbl__(self, value):
        if not value:
            return [0, 0, 0, 0]

        if isinstance(value, int):
            return [value] *4

        value = list(value)
        while len(value) < 4:
            value += value

        return value[:4]

    def __init__(self, screen, label, pos, font_size=24, color=(0, 255, 0), padding=5):
        font = pygame.font.Font('wqy-zenhei.ttc', font_size)
        label_surface = font.render(label, True, color)
        _t, _r, _b, _l = self.__trbl__(padding)

        self.width, self.height = label_surface.get_width()+_r+_l, label_surface.get_height()+_t+_b
        surface = pygame.Surface((self.width, self.height))
        surface.blit(label_surface, (_r, _t))
        pygame.draw.rect(surface, color, (0, 0, self.width-1, self.height-1), 1)
        px, py = pos
        screen_width, screen_height = screen.get_width(), screen.get_height()
        if px < 0:
            px += screen_width-self.width
        if py < 0:
            py += screen_height-self.height
        super(TextButton, self).__init__(screen, (px, py), surface)
        self.x = px
        self.y = py
        self.hover = False
        self._surface = pygame.Surface((self.width, self.height))
        self._surface.set_alpha(50)
        self._surface.fill((0, 255, 0))

    def Event(self, event):
        self.hover = False
        if EVENT(event) == MOUSE_MOTION:
            _x, _y = event.pos
            if self.x < _x < self.x+self.width and self.y < _y < self.y+self.height:
                self.hover = True
                return True

    def Show(self):
        self.screen.blit(self.button, self.pos)
        if self.hover:
            self.screen.blit(self._surface, (self.x, self.y))

