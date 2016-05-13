#coding=utf8
import pygame

from easy_pygame.EVENT import *
import easy_pygame

#---------------------
def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)


class ChengChiInfo(easy_pygame.GameObject):

    def update(self):
        cc=self.db.info_chengchi[self.chengchi]

        self.info.clear()
        self.info.addline(self.chengchi,color=(255,255,0),font=('../wqy-zenhei.ttc',24))

        self.info.set_font(('../wqy-zenhei.ttc',16))
        

        if cc['太守']:
            self.info.add('太守:')
            self.info.add(cc['太守'],color=(255,0,0))
            self.info.endl()
            #太守头像
            txtsf=self.font.render(unicode(cc['太守'],'utf8'),True,(255,255,0))
            img=self.db.info_wujiang[cc['太守']]['大身像']
            self.img=pygame.transform.scale(img,(200,200))
            self.img.blit(txtsf,(100-txtsf.get_width()/2,200-txtsf.get_height()))


        if cc['势力']:
            self.info.add('君主:')
            self.info.add(cc['势力'],color=(255,0,0))
            self.info.endl()

        sss='农业：'
        if cc['农业']>=cc['农业资源']:
            sss+='^255,128,0&'+str(cc['农业'])+'^0,255,0&'
        else:
            sss+=str(cc['农业'])
        sss+='/'+str(cc['农业资源'])+'\n'

        sss+='商业：'
        if cc['商业']>=cc['商业资源']:
            sss+='^255,128,0&'+str(cc['商业'])+'^0,255,0&'
        else:
            sss+=str(cc['商业'])
        sss+='/'+str(cc['商业资源'])+'\n'
        sss+='粮食：'+str(cc['粮食'])+'\n'
        sss+='金钱：'+str(cc['金钱'])+'\n'
        sss+='人口：'+str(cc['人口'])+'\n'
        sss+='特产：'+str(cc['特产'])+'\n'
        sss+='城市技能：'+str(cc['城技'])+'\n'
        sss+='民忠：'+str(cc['民忠'])+'\n'
        sss+='防灾：'+str(cc['防灾'])+'\n'
        sss+='后备兵力：'+str(cc['后备兵力'])+'\n'
        self.info.addtext(sss,H=2)

    def __init__(self,screen,chengchi):
        self.db=self.frame.db
        self.pos=(0,0)
        self.size=(200,380)
        self.screen=screen
        self.chengchi=chengchi
        self.info=TextInfo(self.pos,size=self.size,alpha=180,touch=True)
        self.font=pygame.font.Font('../wqy-zenhei.ttc',20)
        self.update()
        

    def _isin(self,xy,pos,size):
        x,y=xy
        xs,ys=pos
        w,h=size
        if x>xs and x<xs+w and y>ys and y<ys+h:
            return True
    
        return False

    def Event(self,event):
        if self.info.Event(event):return True

        if event.type ==MOUSE_LEFT_DOWN:
            if self.shili and self._isin(event.pos,(0,360),(200,200)):
                print 'taishou ok'
                #mod_taishou.run(self.screen,self.db,self.chengchi)
                self.update()
                return True

        return False
        
    def Show(self):
        self.info.Show(self.screen)
            
        if self.db.cc['太守']:
            self.screen.blit(self.img,(0,360))
