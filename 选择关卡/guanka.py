#!/usr/bin/env python
#coding=utf8
import pygame
import os
import sys
sys.path.append('..')
from easy_pygame.EVENT import *

class GuanKa:
    def __init__(self):
        self.logoW,self.logoH=400,200
        self.guanka=self.get_guanka('../数据')
        print len(self.guanka)
    def get_guanka(self,path):
        ''' 获取 关卡信息 '''
        res={}
        fflist=os.listdir(path)
        for ff in fflist:
            fname=path+os.sep+ff
            if os.path.isdir(fname):
                try:
                    img=pygame.image.load(fname+'/'+ff+'.png').convert()
                    img=pygame.transform.scale(img, (self.logoW,self.logoH))
                except:
                    img=pygame.Surface((400,200))
                    img.fill((255,255,255))
                font=pygame.font.Font('../wqy-zenhei.ttc',24)
                sss=font.render(unicode(ff,'utf8'),True,(0,255,0))
                img.blit(sss,((self.logoW-sss.get_width())/2,self.logoH-sss.get_height()))

                res[ff]=img
        return res
    def get_surface(self):
        surface=pygame.Surface((self.logoW ,self.logoH*len(self.guanka)))
        self.isin_list={}
        i=0
        for x in self.guanka.keys():
            surface.blit(self.guanka[x],(0,self.logoH*i))
            self.isin_list[(0,i)]=x
            i=i+1
        return surface

    def isin(self,pos):
        x,y=pos
        i,j=x/self.logoW,y/self.logoH
        print x,y,i,j
        return self.isin_list.get((i,j))
    
        
def run(screen):
    gk=GuanKa()
    logos=gk.get_surface()
    
    basex,basey=screen.get_width()/2-logos.get_width()/2,0
    sss=None
    while True:
        screen.fill((0,0,0,))
        for event in pygame.event.get():
            if event.type == FRAME_QUIT:
                exit()

            Event=EVENT(event)

            if Event==MOUSE_LEFT_UP:
                x,y=event.pos
                name_guanka=gk.isin((x-basex,y-basey))
                print name_guanka
                #确定关卡
                if name_guanka!=None:
                    sys.path.append('../选择势力')
                    import shili
                    shili.run(screen,name_guanka)

            elif Event==MOUSE_MIDDLE_FORWARD:
                basey=basey+200
            elif Event==MOUSE_MIDDLE_BACKWARD:
                basey=basey-200

            elif Event==MOUSE_LEFT_MOVE:
                x,y=event.rel
                basey=basey+y
    
        #边界检测
        if basey<screen.get_height()-logos.get_height():
            basey=screen.get_height()-logos.get_height()

        if basey>0:
            basey=0
            

        screen.blit(logos,(basex,basey))
        pygame.display.update()


if __name__ =='__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 560), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    run(screen)
    
    
