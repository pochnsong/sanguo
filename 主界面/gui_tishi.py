#coding=utf8
import Init
import pygame
from easy_pygame.EVENT import *
import easy_pygame

class Tishi(easy_pygame.GameObject):
    def __init__(self,screen,pos,msg,img=None,name=None,size=(600,150)):
        """ msg"""
        easy_pygame.GameObject.__init__(self)

        self.screen=screen
        self.pos=pos
        self.size=size

        self.pos_info=Add(pos,(100,0))
        self.info=TextInfo(self.pos_info,size=(500,150))
        self.info.set_pos((0,20))
        self.info.addtext(msg)
        self.imgbg=pygame.Surface((100,150))
        self.imgbg.set_alpha(200)
        if name:
            font=pygame.font.Font('../wqy-zenhei.ttc',18)
            txtsf=font.render(unicode(name,'utf8'),True,(255,128,0))
            self.imgbg.blit(txtsf,(30,110))
        self.img=img

    def Show(self):
        self.info.show(screen)
        self.screen.blit(self.imgbg,self.pos)
        if self.img:
            self.screen.blit(self.img,Add(self.pos,(20,20)))

    def __isin(self,(x,y)):
        xs,ys=self.pos
        w,h=self.size
        if x>xs and x<xs+w and y>ys and y<ys+h:
            return True
    
        return False

    def event(self,event):
        if EVENT(event)==MOUSE_LEFT_DOWN:
            if self.__isin(event.pos):
                self.K
                return True
        return False
