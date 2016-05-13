#coding=utf8
"""
选择太守界面
"""
import pygame
import easy_pygame
from mod_wujiang import WujiangList

def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)

class Taishou(easy_pygame.GameObject):
    def __init__(self,screen,pos,chengchi,db):
        """ pos=屏幕位置 name=城池名称 db=DB数据"""
        easy_pygame.GameObject.__init__(self)

        self.screen=screen
        self.pos=pos
        self.db=db
        self.chengchi=chengchi
        self.size=(800,560)
        self.taishou=self.db.info_chengchi[chengchi]['太守']
        self.sf=pygame.Surface(self.size)
        wj_list=db.shili[db.info_chengchi[chengchi]['势力']][chengchi]
        self.wjlist=WujiangList(self.sf,(250,10),db.get_wujiang(wj_list),size=(550,500),radio=True)
        self.wjlist.set_checked(self.taishou)
        self.img=self.db.info_wujiang[self.taishou]['大身像']
        self.info=easy_pygame.Label(self.sf,(10,260),size=(240,300),alpha=200,touch=True)
        self.update()

    def update(self):
        self.img=self.db.info_wujiang[self.taishou]['大身像']

        ts=self.db.info_wujiang[self.taishou]
        cc=self.db.info_chengchi[self.chengchi]
        self.info.clear()
        self.info.set_font(('../wqy-zenhei.ttc',18))
        self.info.add(self.chengchi,(255,255,0))
        self.info.add('太守:')
        self.info.add(self.taishou,(255,255,0))
        self.info.endl(3)
    
        zz=cc['农业资源']*(ts['智力']-50)/50.0
        zz=int(zz)
        zs=cc['农业资源']+zz
        self.info.add('农业资源:'+str(zs))
        if zz>=0:
            self.info.add(' (+'+str(zz)+')',(255,0,0))
        else:
            self.info.add(' ('+str(zz)+')',(255,255,0))
        self.info.endl(3)
        
        zz=cc['商业资源']*(ts['智力']-50)/50.0
        zz=int(zz)
        zs=cc['商业资源']+zz
        self.info.add('商业资源:'+str(zs))
        if zz>=0:
            self.info.add(' (+'+str(zz)+')',(255,0,0))
        else:
            self.info.add(' ('+str(zz)+')',(255,255,0))
        self.info.endl(3)

        self.info.add('城池防御: 15%')
        self.info.add('+'+str(ts['武力']/10)+'%',(255,0,0))
        self.info.endl(3)
        
    def Show(self):
        self.sf.blit(self.img,(10,10))
        self.wjlist.Show()
        self.info.Show()
        self.screen.blit(self.sf,self.pos)

    def Event(self,event):

        if self.info.Event(event):
            return True
        if self.wjlist.Event(event):
            wj=self.wjlist.get_checked()
            if wj!=self.taishou:
                self.taishou=wj
                self.update()
            return True

class BG(easy_pygame.GameObject):
    def __init__(self,screen):
        easy_pygame.GameObject.__init__(self)
        self.screen=screen

    def Show(self):
        self.screen.fill((0,0,0))


def run(screen,db,chengchi):
    """ chengchi 城池名称"""

    game=easy_pygame.GameFrame()
    bg=BG(screen)
    ts=Taishou(screen,(0,0),chengchi,db)

    game.Add(bg)
    game.Add(ts)

    ok_style=easy_pygame.LoadImg('../src/ok.png')
    ok_style=easy_pygame.Scale(ok_style,(80,80))
    ok=easy_pygame.Button(screen,(720,480),ok_style)
    def fn_ok():
        print ':',db.info_chengchi[chengchi]['太守']
        db.info_chengchi[chengchi]['太守']=ts.taishou
        print db.info_chengchi[chengchi]['太守']
        game.Quit()

    ok.Click=fn_ok
    back_style=easy_pygame.LoadImg('../src/back.png')
    back_style=easy_pygame.Scale(back_style,(50,50))
    back=easy_pygame.Button(screen,(670,510),back_style)
    def fn_back():
        game.Quit()

    back.Click=fn_back

    game.Add(ok)
    game.Add(back)
    print '1'
    game.debug()
    game.MainLoop()
    print '2'
    game.debug()
if __name__=="__main__":

    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------

    db=DB('董卓弄权','刘备')
    
    run(screen,db,'洛阳')

    exit()




