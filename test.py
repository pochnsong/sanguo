# coding=utf-8
from __future__ import unicode_literals
import pygame
import easy_pygame
from easy_pygame.EVENT import *
from easy_pygame import _
import time


class Background(easy_pygame.GameObject):
    def load_src(self):
        src_cfg = easy_pygame.utils.load_json_file("map/config")
        self.source = {}

        for i in range(len(src_cfg['src'])):
            dshow, dtype = src_cfg['src'][i]
            self.source[dshow] = {
                'surface': easy_pygame.LoadImg("map/src/%s.png" % dshow),
                'type': dtype,
            }

    def __init__(self, screen):
        """
        :param screen:
        """
        easy_pygame.GameObject.__init__(self)
        self.screen = screen
        self.load_src()
        cfg = easy_pygame.utils.load_json_file("_last_map_.map")

        self.rows, self.cols = cfg['shape']
        self.blocks = cfg['blocks']
        self.width = 80*self.cols
        self.height = 80*self.rows

        self.x = 0
        self.y = 0

        self.surface = pygame.Surface((self.width, self.width))
        self.surface.fill((0, 0, 0))

        for j in range(self.rows):
            for i in range(self.cols):
                dshow, dtyep = self.blocks[j][i]
                self.surface.blit(self.source[dshow]['surface'], (i*80, j*80))

        self.selected = None
        self.mouse_down = False

    def ji2xy(self, row, col):
        return self.x+col*80, self.y+row*80

    def xy2ji(self, x, y):
        return int((y - self.y) / 80), int((x - self.x) / 80)

    def Show(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.surface, (self.x, self.y))

    def isin(self, pos):
        x, y = pos
        if self.x < x < self.width+self.x and self.y < y < self.height+self.y:
            return True
        return False

    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_UP and self.isin(event.pos):
            self.mouse_down = False
            return True

        if EVENT(event) == MOUSE_LEFT_MOVE and self.isin(event.pos):
            if self.mouse_down:
                _x, _y = event.rel
                self.x += _x
                self.y += _y
                # print(_x, _y)
                return True

        if EVENT(event) == MOUSE_LEFT_DOWN and self.isin(event.pos):
            x, y = event.pos
            j, i = self.xy2ji(x, y)
            print('map', (j, i), (x, y))
            self.mouse_down = True
            return True
        return False


class NPC(easy_pygame.GameObject):
    def __init__(self, screen, x, y, bg, row, col):
        easy_pygame.GameObject.__init__(self)
        self.screen = screen
        self.bg = bg
        image = easy_pygame.LoadImg("src/rw.png")
        self.images = []
        for j in range(4):
            imgs = []
            for i in range(3):
                img = image.subsurface((x+i*32, y+j*32, 32, 32)).copy()
                imgs.append(pygame.transform.scale(img, (64, 64)))
            self.images.append(imgs)

        self.idx = 2
        self.current = 0
        self.t0 = time.time()
        self.step = 1
        self.j = row
        self.i = col
        self.show_steps = False
        self.surface = self.images[self.idx][self.current]

    def get_steps(self):
        n = 2
        pos = []
        for j in range(-n, n + 1):
            for i in range(abs(j) - n, n - abs(j) + 1):
                pos.append([j+self.j, i+self.i])
        return pos

    def update(self):
        t1 = time.time()
        if t1 - self.t0 >= 0.5:
            self.current += self.step
            if (self.step > 0 and self.current == len(self.images[self.idx])-1)\
                    or (self.step < 0 and self.current == 0):
                self.step *= -1
            self.t0 = t1

        self.surface = self.images[self.idx][self.current]

    def Show(self):
        self.update()

        self.screen.blit(self.surface, self.bg.ji2xy(self.j, self.i))
        if self.show_steps:
            for j, i in self.get_steps():
                x, y = self.bg.ji2xy(j, i)
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, 80, 80), 2)
        pass

    def clean(self):
        self.show_steps = False

    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_DOWN:
            x, y = event.pos
            j, i = self.bg.xy2ji(x, y)
            if j == self.j and i == self.i:
                self.frame.Call("npc", "clean")
                self.show_steps = True
                return True

            if self.show_steps and [j, i] in self.get_steps():
                self.j = j
                self.i = i
                self.frame.Call("npc", "clean")
                return True


def run(screen):
    print('loading')
    # pygame.event.Event()
    app = easy_pygame.GameFrame()
    bg = Background(screen)
    app.Add(bg)

    npc1 = NPC(screen, 0, 0, bg, 3, 3)
    app.Add(npc1, name='npc')

    app.Add(NPC(screen, 32*3, 0, bg, 5, 5), name="npc")

    app.MainLoop()


if __name__ == '__main__':
    XWIDTH, XHEIGHT = 1280, 560
    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption(_("JJDL.三国-地图编辑器v0.1"))
    # -----------
    run(screen)

