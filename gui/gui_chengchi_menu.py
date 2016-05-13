#coding=utf8 
'''
JJDL.三国 策略菜单
'''
import Init
import pygame
from easy_pygame.EVENT import *
import easy_pygame

from sys import exit
import math
import module.loop as loop

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
        self.color=[(255,0,0),
                    (255,128,0),
                    (255,255,0),
                    (0,255,0),
                    (0,255,255),
                    (0,0,255),
                    (128,0,255)]

        self.Select=self.__select
        
    def __select(self):
        pass

    def set_statue(self,statue):
        self.statue=statue
        self.menulist=self.get_menulist(self.statue)
        self.index=0
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
        lenll=len(ll)
        
        if len(ll)>9:
            da=6.28/10        
            lp=loop.Loop(ll,10)
            ll=lp.get(self.index)
            self.index=lp.get_start()

        a=self.offset
        r=66*int(find)

        
        cx,cy=self.pos
        R=(r+45)*2
        bg=pygame.Surface((R,R))
        bg.fill((255,255,255))
        bg.set_alpha(200)
        bg.set_colorkey((255,255,255))
        pygame.draw.circle(bg, (0,0,0), (R/2,R/2), R/2, 0)
        screen.blit(bg,(cx-R/2,cy-R/2))

        i=0    
        for name in ll:
            cid=(self.index+i)%lenll
            text=self.font.render(unicode(name,'utf8'),True,self.color[cid%7])
            pos=self.xy(a,r)
            x,y=pos
            x,y=x-text.get_width()/2,y-text.get_height()/2
            screen.blit(text,(x,y))
            text=self.font.render(str(cid),True,self.color[cid%7])
            screen.blit(text,(x-30,y-30))
            pygame.draw.circle(screen,self.color[cid%7],pos,40,1)
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
            ll=lp.get(self.index)
            
        a=self.offset
        r=66*int(find) 
        R=r+45
      
        px,py=pos
        for name in ll:
            x,y=self.xy(a,r)
            rr=math.sqrt((px-x)*(px-x)+(py-y)*(py-y))
            if rr<40:
                return name
            a=a+da

        x,y=self.pos
        if math.sqrt((px-x)*(px-x)+(py-y)*(py-y))<R:
            return True
        return False

    def update_index(self):

        if self.menulist[1]==None:
            return True

        if len(self.menulist[1])<10:
            return True
        if self.offset>0.628:
            self.offset-=0.628
            self.index-=1
        if self.offset<0:
            self.offset+=0.628
            self.index+=1

    def event(self,event):
        if EVENT(event) == MOUSE_LEFT_DOWN:
            self.select = self.isin(event.pos)
            if self.select :
                x,y=event.pos
                posx,posy=self.pos
                self.angle = math.atan2(y-posy,x-posx)
                return True
                
        if self.select and EVENT(event) == MOUSE_LEFT_UP:
            if self.select !=True and self.select == self.isin(event.pos):
                self.set_statue( self.select)
                if self.statue and self.menulist[1]==None:
                    self.Select()
                    return True
                self.offset=0
            self.select = False
            return True

        if self.select and EVENT(event) == MOUSE_LEFT_MOVE:
            x,y=event.pos
            posx,posy=self.pos
            cur_angle=math.atan2(y-posy,x-posx)
            self._angle=self.angle-cur_angle
            self.angle=cur_angle
            if self._angle>3.14:
                self._angle-=6.28
            if self._angle<-3.14:
                self._angle+=6.28

            self.offset=self.offset+(self._angle)
            self.update_index()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button==5:
            self.offset-=0.3
            self.update_index()        
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==4:
            self.offset+=0.3
            self.update_index()        
            return True
        return False
        

class ChengchiMenu(easy_pygame.GameObject):
    """策略菜单 """
    def __init__(self,screen,pos,db=None):
        easy_pygame.GameObject.__init__(self)
        self.screen=screen
        self.db=db
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
             ('军备',
              [('侦查',None),
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
               ]),
             ('INFO',None),]
            ,pos)

        self.menu.Select=self.Select

    def Select(self):
        pass

    def Event(self,event):
        return self.menu.event(event)
    
    def Show(self):
        self.menu.show(self.screen)
    
    def set_statue(self,statue):
        self.menu.set_statue(statue)

class Background(easy_pygame.GameObject):
    ''' 黑色背景'''

    def __init__(self,screen):
        easy_pygame.GameObject.__init__(self)
        self.screen=screen
        
    def Update(self):
        self.menu=ChengchiMenu(screen,(400,280))
        self.Add(self.menu)

    def Event(self,event):
        if EVENT(event)==FRAME_QUIT:
            self.frame.Quit()
            return True

        if EVENT(event)==MOUSE_LEFT_DOWN:
            self.menu.set_statue(None)
            return True

    def Show(self):
        self.screen.fill((255,255,255))

if __name__=='__main__':
    #run('')
    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------

    game=easy_pygame.GameFrame()
    game.Add(Background(screen))

    game.MainLoop()
    
