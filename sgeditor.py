# coding=utf8

"""
JJDL.三国 地图编辑器
"""
from __future__ import unicode_literals, division

import sys
import math
from easy_pygame.EVENT import *
import easy_pygame
from easy_pygame import _
import random


class Screen(easy_pygame.GameObject):
    """"""

    def __init__(self, screen):
        easy_pygame.GameObject.__init__(self)
        self.screen = screen

    def Show(self):
        self.screen.fill((0, 0, 0))
        easy_pygame.GameObject.Show(self)

    def Event(self, event):
        if easy_pygame.GameObject.Event(self, event):
            return True

        if event.type == pygame.QUIT:
            exit()

        return False


class SGMap(easy_pygame.GameObject):
    def __init__(self, screen):
        """

        :param screen:
        """
        self.font = pygame.font.Font('wqy-zenhei.ttc', 16)

        easy_pygame.GameObject.__init__(self)
        self.cols = 20
        self.rows = 20

        self.width = 80*self.cols
        self.height = 80*self.rows

        self.pos = (0, 0)
        self.screen = screen
        grid = pygame.Surface((self.width+1, self.height+1))
        grid.fill((0, 0, 0))
        grid.set_colorkey((0, 0, 0))

        for j in range(self.rows+1):
            pygame.draw.line(grid, (255, 255, 255), (0, j*80), (self.width, j*80))

        for i in range(self.cols+1):
            pygame.draw.line(grid, (255, 255, 255), (i * 80, 0), (i * 80, self.height))
        self.grid = grid

        self.surface = pygame.Surface((self.width, self.width))
        self.surface.fill((0, 0, 0))

        self.blocks = []
        for j in range(self.rows):
            _row = []
            for i in range(self.cols):
                _row.append(None)
                s = self.font.render("%s,%s" % (j, i), True, (255, 255, 255))
                grid.blit(s, (80*i, 80*j))

            self.blocks.append(_row)

        self.selected = None
        self.mouse_down = False

    def SetBlock(self, row, col, mblock):
        self.surface.blit(mblock['surface'], (80*col, 80*row))
        self.blocks[row][col] = mblock

    def Show(self):
        if self.selected is not None:
            j, i = self.selected
            surface = self.surface.copy()
            pygame.draw.rect(surface, (0, 255, 0), (i*80, j*80, 80, 80), 1)
            self.screen.blit(surface, self.pos)
        else:
            self.screen.blit(self.surface, self.pos)

        self.screen.blit(self.grid, self.pos)

    def isin(self, pos):
        x, y = pos
        if x < self.width and y < self.height:
            return True
        return False

    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_UP and self.isin(event.pos):
            self.mouse_down = False
            return True

        if EVENT(event) == MOUSE_LEFT_MOVE and self.isin(event.pos):
            if self.mouse_down:
                _x, _y = event.rel
                px, py = self.pos
                self.pos = px+_x, py+_y
                # print(_x, _y)
                return True

        if EVENT(event) == MOUSE_LEFT_DOWN and self.isin(event.pos):
            x, y = event.pos
            px, py = self.pos
            j, i = int((y-py)/80), int((x-px)/80)
            print('map', (j, i), (x, y))
            self.selected = (j, i)
            self.mouse_down = True
            return True
        return False

    def Save(self):
        res = []

        for j in range(self.rows):
            _row = []
            for i in range(self.cols):
                mblock = self.blocks[j][i]
                # print("mblock", j, i, mblock)
                if mblock is None:
                    _row.append([-1, -1])
                else:
                    _row.append([mblock['dshow'], mblock['dtype']])

            res.append(_row)
        cfg = {
            'shape': (self.rows, self.cols),
            'blocks': res,
        }
        easy_pygame.utils.save_json_file("_last_map_.map", cfg)
        print(res)


class ToolBar(easy_pygame.GameObject):
    def __init__(self, screen, sgmap):
        """

        :param screen:
        """
        easy_pygame.GameObject.__init__(self)
        self.sgmap = sgmap
        self.width = 80*2

        self.pos = (screen.get_width()-self.width, 0)

        self.screen = screen
        src_cfg = easy_pygame.utils.load_json_file("map/config")
        self.src_length = len(src_cfg["src"])
        self.src_list = []
        self.cols = 2
        self.rows = int(math.ceil(self.src_length/2.0))
        self.d0 = None

        self.surface = pygame.Surface((80*self.cols, 80*self.rows))
        for y in range(self.rows):
            _row = []
            for x in range(self.cols):
                i = y*2+x
                if i > self.src_length-1:
                    break

                print(y, x, i, self.idx2ji(i))

                dshow, dtype = src_cfg["src"][i]
                img = easy_pygame.LoadImg("map/src/%s.png" % dshow)
                self.surface.blit(img, (80*x, 80*y))
                mblock = {
                    'surface': img,
                    'dtype': dtype,
                    'dshow': dshow,
                }
                _row.append(mblock)
                if dtype == 0:
                    self.d0 = mblock

            self.src_list.append(_row)
        self.selected = None

    def Show(self):
        self.screen.blit(self.surface, self.pos)
        easy_pygame.GameObject.Show(self)

    def isin(self,pos):
        x,y = pos
        if x>self.pos[0] and y < self.surface.get_height():
            return True
        return False

    def Event(self, event):
        if EVENT(event) == MOUSE_LEFT_DOWN and self.isin(event.pos):
            x, y = event.pos
            x -= self.pos[0]
            j, i = int(y/80), int(x/80)
            if self.sgmap.selected:
                _j, _i = self.sgmap.selected
                self.sgmap.SetBlock(_j, _i, self.src_list[j][i])
            #self.selected = self.src_list[j][i]
            return True


        return False

    def idx2ji(self, idx):
        j, i = int(idx/2), int(idx % 2)
        return j, i


class SaveButton(easy_pygame.TextButton):
    def __init__(self, screen, sgmap):
        super(SaveButton, self).__init__(screen, "保存", (-1, -1))
        self.sgmap = sgmap

    def Click(self):
        self.sgmap.Save()


class RandomMapButton(easy_pygame.TextButton):
    def __init__(self, screen, sgmap, toolbar):
        super(RandomMapButton, self).__init__(screen, "生成随机地图", (-1, -50))
        self.sgmap = sgmap
        self.toolbar = toolbar

    def Click(self):
        for mj in range(self.sgmap.rows):
            for mi in range(self.sgmap.cols):
                idx = random.randint(1, self.toolbar.src_length-1)
                j, i = self.toolbar.idx2ji(idx)
                print(mj, mi, j, i)
                self.sgmap.SetBlock(mj, mi, self.toolbar.src_list[j][i])

        self.sgmap.SetBlock(int(self.sgmap.rows/2), int(self.sgmap.cols/2), self.toolbar.d0)


def run(screen):
    print('loading')

    app = easy_pygame.GameFrame()

    bg = Screen(screen)
    app.Add(bg)
    sgmap = SGMap(screen)
    app.Add(sgmap)
    toolbar = ToolBar(screen, sgmap)
    app.Add(toolbar)
    save_btn = SaveButton(screen, sgmap)
    app.Add(save_btn)
    app.Add(RandomMapButton(screen, sgmap, toolbar))
    app.MainLoop()


if __name__ == '__main__':
    XWIDTH, XHEIGHT = 1280, 560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption(_("JJDL.三国-地图编辑器v0.1）"))
    # -----------
    run(screen)

