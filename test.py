# coding=utf-8
from __future__ import unicode_literals
import pygame
import easy_pygame
from easy_pygame import _
import time


class Background(easy_pygame.GameObject):
    def __init__(self, screen):
        super(Background, self).__init__()
        self.screen = screen
        cfg = easy_pygame.utils.load_json_file("_last_map_.map")
        print(cfg)

    def Show(self):
        self.screen.fill((0, 0, 0))


class NPC(easy_pygame.GameObject):
    def __init__(self, screen, x=0, y=0, pos=(0, 0)):
        easy_pygame.GameObject.__init__(self)
        self.screen = screen
        self.pos = pos
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

    def Show(self):
        t1 = time.time()
        if t1 - self.t0 >= 0.5:
            self.current += self.step
            if (self.step > 0 and self.current == len(self.images[self.idx])-1)\
                    or (self.step < 0 and self.current == 0):
                self.step *= -1
            self.t0 = t1

        self.screen.blit(self.images[self.idx][self.current], self.pos)

        pass

def run(screen):
    print('loading')

    app = easy_pygame.GameFrame()
    app.Add(Background(screen))

    npc1 = NPC(screen)
    app.Add(npc1)

    app.Add(NPC(screen, 32*3, 0, (80, 0)))

    app.MainLoop()


if __name__ == '__main__':
    XWIDTH, XHEIGHT = 1280, 560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption(_("JJDL.三国-地图编辑器v0.1"))
    # -----------
    run(screen)

