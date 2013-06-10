#coding=utf8
import pygame

def LoadImg(src):
    return pygame.image.load(src).convert_alpha()

def Scale(surface,(width,height)):
    return pygame.transform.smoothscale(surface,(width,height))

#------------------------------------------------------------
#图形函数
def DrawLine(sf,(r,g,b),(xs,ys),(xe,ye)):
    pygame.draw.line(sf,(r,g,b),(xs,ys),(xe,ye))
