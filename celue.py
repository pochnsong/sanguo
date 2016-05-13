#coding=utf8

'''
JJDL.三国 大地图模块
'''
from __future__ import unicode_literals
SRC_WORLD='src/wd.png'

import sys
from sgdata import SGDatabase #三国数据库
from easy_pygame.EVENT import *
import easy_pygame

from gui.gui_chengchi import ChengChiInfo
from gui.gui_chengchi_menu import ChengchiMenu
#---------------------
def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)

class SanGuo:
    def __init__(self,sgdatabase):
        self.sgdatabase=sgdatabase

class Background(easy_pygame.GameObject):
    ''' 背景 '''
    def __init__(self,bg,screen):
        easy_pygame.GameObject.__init__(self)

        self.bg=bg
        self.screen=screen
        self.offset=(0,0)
        self.gui_chengchi=None
        self.gui_chengchi_caidan=None

    def Show(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,self.offset)
        easy_pygame.GameObject.Show(self)
        

    def pos_to_chengchi(self,(x,y)):
        ''' 获取城池名称 (x,y)鼠标位置'''
        res=None
        
        i,j=x/100,y/100
        print i,j
        res=self.frame.db.map_chengchi.get((i,j))
        if not res:
            res=self.frame.db.map_chengchi.get((i-1,j))
        
        return res

    def Event(self,event):
        if easy_pygame.GameObject.Event(self,event):
            return True
        
        if event.type==pygame.QUIT:
            exit()
        if EVENT(event)==MOUSE_LEFT_MOVE:
            self.offset=Add(self.offset,event.rel)
            if self.gui_chengchi_caidan:
                self.gui_chengchi_caidan.menu.pos=Add(self.gui_chengchi_caidan.menu.pos,event.rel)

            return True

        if EVENT(event)==MOUSE_LEFT_DOWN:#鼠标左键
            self.frame.Kill(self.gui_chengchi)
            self.frame.Kill(self.gui_chengchi_caidan)
            
            self.gui_chengchi=None
            self.gui_chengchi_caidan=None

            #是否选中城池 
            selected=self.pos_to_chengchi(Sub(event.pos,self.offset))
            if selected:
                print selected
                self.gui_chengchi=ChengChiInfo(self.screen,selected)
                self.Add(self.gui_chengchi)
                self.gui_chengchi_caidan=ChengchiMenu(self.screen,event.pos)
                self.Add(self.gui_chengchi_caidan)
            return True

        if EVENT(event)==MOUSE_LEFT_UP:#鼠标右键
            pass
        return False

class SGFrame(easy_pygame.GameFrame):
    
    def __init__(self,db):
        self.db=db
        easy_pygame.GameFrame.__init__(self)


#-----------
class Load:
    def __init__(self,screen):
        self.screen=screen
        self.y=0
        self.font=pygame.font.Font('wqy-zenhei.ttc',18)
        screen.fill((0,0,0))

    def load(self,text):
        text=self.font.render('utf8',True,(0,255,0))
        self.screen.blit(text,(0,self.y))
        pygame.display.update()
        self.y+=20

def run(screen,guanka,myshili):
    logo=Load(screen)
    screensize=(screen.get_width(),screen.get_height())
    logo.load('loading...')
    print 'loading'
    db=SGDatabase(guanka)
    print 'ok'

    game=SGFrame(db)

    bg=Background(db.get_world(),screen)
    game.Add(bg)

    game.MainLoop()

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------
    run(screen,'董卓弄权','刘备')

