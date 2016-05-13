# coding=utf8
from __future__ import unicode_literals

import math

from pygame.locals import *

import module.resources as resources
from easy_pygame.EVENT import *
from load_shili import *


class ShiLi:
    ''' 选择势力 '''
    def __init__(self,guanka):
        '''guanka 关卡 '''
        self.guanka=guanka
        self.logoW,self.logoH=1028,560
        #self.shili=get_shili_list('../数据/'+guanka+'/势力信息')        
        self.shili=resources.load_dict_path('数据/'+guanka+'/势力信息',
                                            resources.load_dict_1,
                                            suffix='.势力')        

    def get_imglist(self):
        """ [ (),(),()] """
        res=[]
        font=pygame.font.Font('wqy-zenhei.ttc',36)
    
        for x in self.shili.keys():
            if x=='在野':
                continue
            img=resources.load_image('数据/'+self.guanka+'/资源/大身像/'+x+'.jpg')
            txt=font.render(x,True,(255,0,0))
            img.blit(txt,((img.get_width()-txt.get_width())/2,img.get_height()-txt.get_height()))
            res.append((x,img,0))

        return res

def po_to_xy(p,o):
    return p*math.cos(o),p*math.sin(o)

def LuoXuan(screen,imgdict,pos=0,seleted=None):
    ''' 螺旋旋转 '''
    a=30 #半径
    o=0.0+pos 
    _kk=1.0/180.0/len(imgdict)
    for name,wujiang,wid in imgdict:

        k=int(1.0/1080.0*o*50.0)
        _k=_kk*o
        wujiang=pygame.transform.scale(wujiang, (k, k))
        x,y=po_to_xy(a*o/360.0,o/360.0)
        x,y=int(x+519),(y+180)
        screen.blit(wujiang, (x, y))
        if seleted==name:
            pygame.draw.rect(screen,(0,255,0),Rect(x,y,k,k),2)
        o=o+180.0

    pass
#---------------------------------------
def looplist(srclist,lenght,index):
    """
    列表,返回长度,起点,方向=+,-
    """
    srclen=len(srclist)
    while index>srclen:
        index-=srclen
        
    rsrclist=srclist[::-1]
    res=srclist[index:lenght]

    i=index
    while len(res)<lenght:
        res=res+srclist[0:lenght-len(res)]
        
    return res
#---------------------------------------
def select_wujiang(pos,screen,wujiangs,angle=0):
    a=30
    o=0.0+angle
    mx,my=pos
    res=None
    for name,wujiang,wid in wujiangs:
        k=int(1.0/1080.0*o*50.0)
        x,y=po_to_xy(a*o/360.0,o/360.0)
        x,y=int(x+519),(y+180)
        if mx>x and my>y and mx<x+k and my<y+k:
            res=name
        o=o+180.0
        
    return res
#---------------------------------------

class Menu:
    def __init__(self,screen):
        self.backbt=pygame.image.load('src/back.png').convert_alpha()
        self.backbt=pygame.transform.scale(self.backbt, (100, 100))
        self.okbt=pygame.image.load('src/ok.png').convert_alpha()
        self.okbt=pygame.transform.scale(self.okbt, (100, 100))
        self.screen=screen
        self.ok=False
    def set(self,ok):
        self.ok=ok
        
    def menu(self,screen):
        self.screen.blit(self.backbt,(0,self.screen.get_height()-self.backbt.get_height()))
        if self.ok:
            self.screen.blit(self.okbt,(self.screen.get_width()-self.okbt.get_width(),screen.get_height()-self.okbt.get_height()))
        
    def isin(self,pos):
        x,y=pos
        if x<self.backbt.get_width() and y>self.screen.get_height()-self.backbt.get_height():
            return '后退'
        if self.ok and x>self.screen.get_width()-self.okbt.get_width() and y>self.screen.get_height()-self.okbt.get_height():
            return '确定'

        return None

def run(screen,guanka):
    font=pygame.font.Font('wqy-zenhei.ttc',24)
    shili=ShiLi(guanka)

    wujiang_liebiao=shili.get_imglist()

    MAX_wujiang=len(wujiang_liebiao) #武将长度

    i=0
    LEN_wujiang=20 #显示长度

    wujiangs=looplist(wujiang_liebiao,LEN_wujiang,0)

    i_s=0
    
    pause=False
    angle=0
    di=10 #角速度
    clock=pygame.time.Clock()
    
    menu=Menu(screen)
    seleted=None
    while True:
        screen.fill((0,0,0,))
        time_passed = clock.tick()
        time_passed_seconds = time_passed/100.0

        for event in pygame.event.get():
            if event.type == FRAME_QUIT:
                exit()
            if EVENT(event)==MOUSE_LEFT_DOWN:
                bt=menu.isin(event.pos)
                if bt=='后退':
                    return
                if bt=='确定':

                    import celue
                    celue.run(screen, guanka, seleted)
                seleted=select_wujiang(event.pos,screen,wujiangs,angle=i)
                if seleted!=None:
                    menu.set(True)
                    di=0
                else:
                    menu.set(False)
                    di=10
                '''
                x,y=event.pos
                angle=math.atan2(y-180,x-400)
                '''
            if EVENT(event)==MOUSE_LEFT_UP:
                di=10
                angle=0

            if EVENT(event)==MOUSE_LEFT_MOVE:
                x,y=event.pos
                di=(math.atan2(y-180,x-400)-angle)
                if math.fabs(di)<0.01:di=0
                di=di*10000
                if di>90:di=90
                if di<-90:di=-90
                angle=math.atan2(y-180,x-400)
                    
        if i<0:
            i=i+180
            i_s=i_s+1
            
            if i_s>MAX_wujiang:
                i_s=i_s-MAX_wujiang
            wujiangs=looplist(wujiang_liebiao,LEN_wujiang,i_s)
            

        if i>180:
            i=i-180
            i_s=i_s-1
            if i_s<0:
                i_s=i_s+MAX_wujiang
            
            wujiangs=looplist(wujiang_liebiao,LEN_wujiang,i_s)

        LuoXuan(screen,wujiangs,i,seleted)

        distance_moved = time_passed_seconds * di
        i=i+distance_moved
        menu.menu(screen)
        pygame.display.update()

if __name__ =='__main__':
    """
    ss=[1,2,3,4,5]
    sl=looplist(ss,10,3,direction='+')
    rsl=looplist(ss,10,3,direction='-')
    
    print ss
    print sl
    print rsl
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')

    pygame.init()
    screen = pygame.display.set_mode((1028, 560), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    run(screen, "董卓弄权")

    
    
