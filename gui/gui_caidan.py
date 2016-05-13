#coding=utf8 
'''
JJDL.三国 菜单
'''
import Init

import pygame
import math
import module.loop as loop
from easy_pygame.EVENT import *

class Menu:
    def __init__(self,menu,pos):
        """
        menu=[
        ('内政',[('开垦',None),('招商',None)]),
        ('军备',None),
        ('外交',None),
        ]
        """
        self.menu=menu
        self.statue=None
        self.menulist=self.get_menulist(self.statue)
        self.select=False
        self.offset=0
        self.pos=pos
        self.index=0
        self._angle=0
        self.font=pygame.font.Font('../wqy-zenhei.ttc',28)
        self.bg=pygame.image.load('../src/bg_menu.png').convert_alpha()
        pass

    def set_statue(self,statue):
        self.statue=statue
        self.menulist=self.get_menulist(self.statue)
        self.index=-1
        self.offset=0
        self._angle=0

    def submenu(self,menu):
        if menu==None:
            return None
        res=[]
        for x,l in menu:
            res.append(x)
        return res
    def get_menulist(self,name=None,menu=None,level=1):
        """ 获取子菜单
        return True/False,[子菜单]
        """
        res=[]
        if name==None:
            return 1,self.submenu(self.menu)
        if menu==None:
            level,menu=1,self.menu

        for _name,_menu in menu:
            if _name==name: 
                return level+1,self.submenu(_menu)
            else:
                if _menu!=None:
                    find,_menu=self.get_menulist(name,_menu,level+1)
                    if find:
                        return find,_menu

        return 0,[]

    def xy(self,a,r=100):
        """ 坐标位置"""
        posx,posy=self.pos
        x=r*math.sin(a)+posx
        y=r*math.cos(a)+posy

        return (int(x),int(y))
    def show(self,screen):
        find,ll=self.menulist
        if ll==None:
            return
        
        da=6.28/len(ll)

        if len(ll)>9:
            da=6.28/10        
            lp=loop.Loop(ll,10)
            Index=[self.index]
            ll=lp.get(Index)
            self.index=Index[0]

        a=self.offset
        r=80*int(find)

        text=self.font.render(str(self.index)+":"+str(len(self.menulist[1])),True,(0,255,0))
        screen.blit(text,(0,0))
        text=self.font.render(str(self.offset),True,(0,255,0))
        screen.blit(text,(0,30))
        text=self.font.render(str(self._angle),True,(0,255,0))
        screen.blit(text,(0,60))

        cx,cy=self.pos        
        screen.blit(self.bg,(cx-self.bg.get_width()/2,cy-self.bg.get_height()/2))

        i=0    
        for name in ll:
            text=self.font.render(unicode(name,'utf8'),True,(0,255,0))
            pos=self.xy(a,r)
            x,y=pos
            x,y=x-text.get_width()/2,y-text.get_height()/2
            screen.blit(text,(x,y))
            text=self.font.render(str(self.index+i),True,(0,255,0))
            screen.blit(text,(x-30,y-30))
            pygame.draw.circle(screen,(0,255,0),pos,40,1)
            a=a+da
            i=i+1
        if len(ll)==10:            
            pygame.draw.circle(screen,(255,0,0),self.xy(0,r),40,2)
            
    def isin(self,pos):
        find,ll=self.menulist
        if ll==None:
            return
        
        da=6.28/len(ll)

        if len(ll)>9:
            da=0.628        
            lp=loop.Loop(ll,10)
            Index=[self.index]
            ll=lp.get(Index)
            self.index=Index[0]

        a=self.offset
        r=80*int(find)
       
        px,py=pos
        for name in ll:
            x,y=self.xy(a,r)
            rr=math.sqrt((px-x)*(px-x)+(py-y)*(py-y))
            if rr<40:
                return name
            a=a+da

        x,y=self.pos
        if math.sqrt((px-x)*(px-x)+(py-y)*(py-y))<210:
            return True
        return False

    def event(self,event):
        if event.type == MOUSEBUTTONDOWN:
            self.select = self.isin(event.pos)
            if self.select :
                x,y=event.pos
                posx,posy=self.pos
                self.angle = math.atan2(y-posy,x-posx)
                return True
            else:
                self.set_statue(None)
                return None
                
        if self.select and event.type == MOUSEBUTTONUP:
            if self.select !=True and self.select == self.isin(event.pos):
                self.set_statue( self.select)
                if self.statue and self.menulist[1]==None:
                    #print self.statue,self.menulist[1]
                    return self.statue
                self.offset=0
            self.select = False
            return True

        if self.select and event.type == MOUSEMOTION:
            x,y=event.pos
            posx,posy=self.pos
            cur_angle=math.atan2(y-posy,x-posx)
            self._angle=self.angle-cur_angle
            if self._angle>3.14:
                self._angle-=6.28
            if self._angle<-3.14:
                self._angle+=6.28

            self.offset=self.offset+(self._angle)
            self.angle=cur_angle

            if len(self.menulist[1])<10:
                return 
            if self.offset>0.628:
                self.offset-=0.628
                self.index-=1
            if self.offset<0:
                self.offset+=0.628
                self.index+=1
            return True
        return None
        

class CelueMenu:
    """策略菜单 """
    def __init__(self,pos,data=None):
        self.menu=Menu(
            [('内政',
              [('开垦',None),
               ('招商',None),
               ('搜寻',None),
               ('治理',None),
               ('出巡',None),
               ('招降',None),
               ('处斩',None),
               ('流放',None),
               ('赏赐',None),
               ('没收',None),
               ('交易',None),
               ('宴请',None),
               ('输送',None),
               ('移动',None),
               ]),
             ('Военное дело',
              [('侦察',None),
               ('征兵',None),
               ('分配',None),
               ('掠夺',None),
               ('出征',None),
               ]),
             ('外交',
              [('离间',None),
               ('招揽',None),
               ('策反',None),        
               ('反间',None),
               ('劝降',None),
               ]),]
            ,pos)
    def event(self,event):
        return self.menu.event(event)
    
    def show(self,screen):
        self.menu.show(screen)

def run(screen):
    
    menu=CelueMenu((400,280))
    
    while True:        
        screen.fill((0,0,0))
        for event in pygame.event.get():
            print menu.event(event)
            if event.type == pygame.QUIT:
                exit()
        menu.show(screen)
        pygame.display.update()
    
if __name__=='__main__':
    #run('')
    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------
    run(screen)

