#coding=utf8

import pygame
from EVENT import *
from frame import GameObject
#---------------------
def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)

class Label(GameObject):
    ''' 用来显示文字信息的对话框 '''
    def __init__(self,screen,pos,size=(200,150),alpha=200,touch=False):        
        self.screen=screen
        self.sf=pygame.Surface(size)
        self.font=pygame.font.SysFont(None,16)
        self.pos=pos
        self.textpos=(0,0)
        self.sf.set_alpha(alpha)
        self.touch=touch
        self.offset=(0,0)
        self.textlist=[]
        self.size=size
        self.select=False
        self.color=(0,255,0)
    #-----设置------------------
    def clear(self):
        self.textlist=[]
        self.textpos=(0,0)
        self.offset=(0,0)

    def set_font(self,font):
        font,size=font
        self.font=pygame.font.Font(font,size)
        
    def set_alpha(self,alpha):
        self.sf.set_alpha(alpha)

    def set_color(self,color):
        self.color=color
    def set_pos(self,pos):
        self.textpos=pos
    def set_touch(self,touch):
        self.touch=touch
    #------------------------------------
    def _addtext(self,text,color,font,pos):
        if not color:
            color=self.color
        if font:
            font,size=font
            font=pygame.font.Font(font,size)
        else:
            font=self.font
        if not pos:
            x,y=self.textpos
        else:
            x,y=pos

        try:
            text=unicode(text,'utf8')
        except:
            pass
        txtsf = self.font.render(text, True, color)
        self.textlist.append((txtsf,(x,y)))
        return txtsf.get_width(),txtsf.get_height()
    
    def add(self,text,color=None,font=None,pos=None):
        '''
        color(255,255,255) font(font,size) pos(x,y)
        '''
        w,h=self._addtext(text,color,font,pos)
        x,y=self.textpos
        x=x+w
        self.textpos=x,y
    def endl(self,H=1):
        x,y=self.textpos
        x,y=0,y+(self.font.get_ascent()+H)
        self.textpos=x,y
    def addline(self,text,color=None,font=None,pos=None):
        '''
        color(255,255,255) font(font,size) pos(x,y)
        '''
        w,h=self._addtext(text,color,font,pos)
        x,y=self.textpos
        y=y+h
        self.textpos=x,y
    def addtext(self,text,font=None,pos=None,H=1):
        ''' 
        ^255,0,0&word
        '''
        getrgb=False
        color=None
        for w in unicode(text,'utf8'):
            if w==u'\n':
                self.endl(H)
                continue
            if w==u'^':
                getrgb=True
                color=''
                continue
            if w==u'&':
                r,g,b=color.split(u',')
                color=(int(r),int(g),int(b))        
                getrgb=False
                continue
            if getrgb:
                color=color+w
                continue
            self.add(w,color)
            
    def Show(self):
        self.sf.fill((0,0,0))
        for x in self.textlist:
            txtsf,txtpos=x
            self.sf.blit(txtsf,Add(txtpos,self.offset))
        self.screen.blit(self.sf,self.pos)

    def Event(self,event):
        if self.touch==False:
            return False

        Event=EVENT(event)
        if Event==MOUSE_LEFT_DOWN:
            x,y=event.pos
            posx,posy=self.pos
            w,h=self.size
            if x>posx and x<posx+w and y>posy and y<posy+h:
                self.select=True
                return True
            else:
                return False
                    
        if Event ==MOUSE_LEFT_UP:
            self.select=False
            
        if self.select and Event==MOUSE_LEFT_MOVE:
            dx,dy=event.rel
            self.offset=Add(self.offset,(0,dy))
            return True

        return False
 
