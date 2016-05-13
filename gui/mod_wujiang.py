#coding=utf8
import sys
sys.path.append('..')

from easy_pygame.EVENT import *
import easy_pygame


def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)
    

class WujiangList(easy_pygame.GameObject):
    def Update(self):
        pass
    def __init__(self,screen,pos,wujiang_list,size=(800,560),radio=False):
        """ pos wujiang_list=武将列表 {武将：''} size=大小 radio=武将是否单选"""
        self.screen=screen
        self.pos=pos
        self.radio=radio #是否单选武将
        self.pos_img=Add(pos,(0,30))#头像位置
        self.pos_text=Add(pos,(80,30))#信息位置
        size_x,size_y=size
        self.size_head=(size_x,30)
        self.size_text=(size_x-80-80,size_y-30)
        self.size_img=(80,size_y-30)
        self.pos_check=(pos[0]+size_x-80,pos[1]+30)#选择列表位置
        self.size_check=(80,size_y-30)

        self.sf=pygame.Surface(self.size_text)
        self.sf.set_alpha(200)
        self.img=pygame.Surface(self.size_img)
        self.head=pygame.Surface(self.size_head)
        self.head.set_alpha(200)
        self.offset_x,self.offset_y=0,0
        self.font=pygame.font.Font('../wqy-zenhei.ttc',20)
        self.check=pygame.Surface(self.size_check)
        self.check.set_alpha(200)
        
        self.select_text=False
        self.select_img=False
        self.template=[80,80,60,60,80,60]
        self.wujiang_list=wujiang_list

        self.wujiangs=wujiang_list.keys()
        self.index=0
        
        if self.radio:
            self.checked=0
        else:
            self.checked=[False]*len(self.wujiangs)
        self.Update()

    def set_checked(self,name):
        self.checked=self.wujiangs.index(name)

    def get_checked(self):
        if self.radio:
            return self.wujiangs[self.checked]
          
        res=[]
        for i in xrange(0,len(self.wujiangs)):
            if self.checked[i]:
                wj=self.wujiangs[i]
                res.append(wj)

        return res

    def txt(self,text,pos,color=(0,255,0),sf=None):
        row,col=pos
        x=4
        for i in range(row):
            x+=self.template[i]
        text=str(text)

        textsf=self.font.render(unicode(text,'utf8'),True,color)
        if sf:
            pos=x+80+self.offset_x,0
            sf.blit(textsf,pos)

        else:
            pos=x,col*64+18
            sf=self.sf
            sf.blit(textsf,Add(pos,(self.offset_x,self.offset_y)))
    def Show(self):
        self.sf.fill((0,0,0))
        self.img.fill((0,0,0))
        self.head.fill((0,0,0))
        self.check.fill((0,0,0))

        self.txt('武将',(0,0),sf=self.head)
        self.txt('兵种',(1,0),sf=self.head)
        self.txt('武力',(2,0),sf=self.head)
        self.txt('智力',(3,0),sf=self.head)
        self.txt('兵力',(4,0),sf=self.head)
        self.txt('忠诚',(5,0),sf=self.head)


        textsf=self.font.render(str(len(self.wujiangs)),True,(0,255,0))
        self.head.blit(textsf,(0,0))

        textsf=self.font.render(u'选择',True,(0,255,0))
        self.head.blit(textsf,Sub(self.pos_check,(0,30)))
        
        pygame.draw.line(self.head,(0,255,0),(0,29),(800,29),1)
        
        wujiangs=self.wujiangs[self.index:self.index+10]

        i=0
        for name in  wujiangs:
            wj=self.wujiang_list[name]
            pos_img=(10,i*64)
            img=pygame.transform.scale(wj['小头像'],(60,60))
            self.img.blit(img,Add(pos_img,(0,self.offset_y)))
            y=i*64-2+self.offset_y
            #pygame.draw.line(self.img,(0,255,0),(0,y),(80,y),1)
            
            #选择            
            if (not self.radio) and self.checked[i+self.index]:
                pygame.draw.rect(self.check,(0,255,0),((0,y),(80,62)),0)
            else:
                pygame.draw.rect(self.check,(0,255,0),((0,y),(80,62)),1)

            self.txt(name,(0,i))
            self.txt(wj['兵种'],(1,i))
            self.txt(wj['武力'],(2,i))
            self.txt(wj['智力'],(3,i))
            self.txt(wj['兵力'],(4,i))
            self.txt(wj['忠诚'],(5,i))
            pygame.draw.rect(self.sf,(0,255,0),((1,y),(self.size_text[0],64)),1)
            pygame.draw.rect(self.img,(0,255,0),((1,y),(self.size_img[0],64)),1)
            
            i+=1
        if self.radio:
            y=self.checked*64-2+self.offset_y
            pygame.draw.rect(self.check,(0,255,0),((0,y),(80,62)),0)

        self.screen.blit(self.head,self.pos)
        self.screen.blit(self.img,self.pos_img)
        self.screen.blit(self.sf,self.pos_text)
        self.screen.blit(self.check,self.pos_check)

    def _isin(self,xy,pos,size):
        x,y=xy
        xs,ys=pos
        w,h=size
        if x>xs and x<xs+w and y>ys and y<ys+h:
            return True
    
        return False

    def update_index(self):
        if self.offset_y<-64:
            self.offset_y+=64
            self.index+=1
        elif self.offset_y>0:
            self.offset_y-=64
            self.index-=1
            if self.index<0:
                self.index=0
                self.offset_y=0
        
    def Event(self,event):
        if EVENT(event)==MOUSE_LEFT_DOWN:
            if self._isin(event.pos,self.pos_img,(80,500)):
                self.select_text=False
                self.select_img=True
                return True
            elif self._isin(event.pos,self.pos_text,self.size_text):
                self.select_text=True
                self.select_img=False
                return True
            elif self._isin(event.pos,self.pos_check,self.size_check):
                x,y=self.pos_check#选择列表位置
                _id=(event.pos[1]-y-self.offset_y)/64+self.index
                try:
                    if self.radio:
                        if _id!=self.checked and _id>=0 and _id<len(self.wujiangs):
                            self.checked=_id
                        return True

                    self.checked[_id]=(not self.checked[_id])
                    return True
                except:
                    pass
            return None
                    
        if EVENT(event)==MOUSE_LEFT_UP:
            self.select_text=False
            self.select_img=False
        
        if EVENT(event)==MOUSE_LEFT_MOVE:
            if self.select_text:
                x,y=event.rel
                self.offset_x+=x
                self.offset_y+=y
                self.update_index()
                return True
            if self.select_img:
                x,y=event.rel
                self.offset_y+=y
                self.update_index()
                return True

        #鼠标滚轮
        if EVENT(event)==MOUSE_MIDDLE_BACKWARD :
            self.offset_y-=64
            return True
        if EVENT(event)==MOUSE_MIDDLE_FORWARD:
            self.offset_y+=64
            return True
            
        return False


def LoadImg(src,res):
    for x in res.keys():
        try:
            img=pygame.image.load(src+'/'+x+'.jpg')
        except:
            img=pygame.Surface((64,80))
            img.fill((255,255,255))
        res[x]['小头像']=pygame.transform.scale(img,(60,60))
    return res

class BG(easy_pygame.GameObject):
    def __init__(self,screen):
        self.screen=screen

    def Show(self):
        self.screen.fill((0,0,0))

def run(screen,wujiang=None,caidan=None):
    """
    wj=init.LoadInfo('数据/董卓弄权/武将/武将')
    #cout(wj)
    wj=LoadImg('数据/董卓弄权/资源/小头像',wj)
    """

    print 'loading'
    db= sgdata.SGDatabase('董卓弄权')
    print 'ok'

    game=easy_pygame.GameFrame()

    bg=BG(screen)

    wjl=WujiangList(screen,(0,0),db)

    game.Add(bg)
    game.Add(wjl)
    game.MainLoop()

    font=pygame.font.Font('wqy-zenhei.ttc',25)
    textsf=font.render(unicode('选择执行'+caidan+'的武将','utf8'),True,(0,255,255))
    WJList=WujiangList(screen,(0,30),db)
    #ll=WJ((0,30),wujiang)
    ok=OKButton((720,480))
    back=BackButton((670,510))

if __name__=='__main__':

    import sgdata

    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------
    
    run(screen,'测试')

    exit()
