#coding=utf8
from __future__ import unicode_literals
import pygame

def LoadImg(src):
    res = None
    with open(src, 'rb') as rf:
        res = pygame.image.load(rf).convert_alpha()
        rf.close()
    return res

def Scale(surface,(width,height)):
    return pygame.transform.smoothscale(surface,(width,height))

#------------------------------------------------------------
#图形函数
def DrawLine(sf,(r,g,b),(xs,ys),(xe,ye)):
    pygame.draw.line(sf,(r,g,b),(xs,ys),(xe,ye))
