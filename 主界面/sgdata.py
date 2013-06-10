#coding=utf8
'''
管理游戏数据
model
'''
import re
import sys
sys.path.append('..')
import module.resources as resources
import module.graph as graph
import easy_pygame
import pygame
import random
GAME_PATH='../'

#-------------------------------------------------------------
class SGDATA:
    img_chengchi=None #城池.图像
    ''' img_chenghci=
    {
    "洛阳":pygame_surface,
    "天水":pygame_surface,
    ...
    }
    '''
    img_wujiang=None #武将.图像
    '''img_wujing=
    {
    "刘备":{"大身像":pygame_surface,"小头像":pygame_surface},
    "曹操":{"大身像":pygame_surface,"小头像":pygame_surface},
    ...
    }
    '''
    img_map=None #背景
    ''' img_map=
    pygame_surface
    '''
    map_chengchi=None #城池.地图
    '''map_chengchi=
    {
    (6,3):"西凉",
    (10,6):"安定",
    ...
    }
    '''
    map_daolu=None #道路.地图
    ''' map_daolu=
    graph.Graph
    '''
    info_chengchi=None #城池.信息
    '''info_chengchi=     
    {
    "西凉":{
           "农业":
           "商业":
           "特产":
           "城技":
           "人口":
           "农业资源":
           "商业资源":
           "防灾":
           "民忠":
           "后备兵力":
           "粮食":
           "金钱":
           "太守":
           "势力":
           "大身像":
           "小头像":
           },
    }
    '''
    info_wujiang=None #武将.信息
    ''' info_wujiang=
    {
    "马腾":{
           "兵种":,
           "兵力":
           "武力":
           "智力":
           }
    }
    '''
    shili=None #势力
    ''' shili=
    {
    "董卓":{
           "长安":[李榷 郭汜 李肃 候成],
           "洛阳":[董卓 李儒 吕布 华雄 张辽 王允 荀攸],
           "宛城":[高顺 牛辅]
           },
    ...
    }
    '''
    
    def __init__(self,guanka):
        self.guanka=guanka
        PATH=GAME_PATH+'数据/'+guanka+'/'
        self.info_chengchi=resources.load_dict_2(PATH+'城池信息')
        self.map_chengchi=resources.load_dict_0(PATH+'城池.地图',pyeval=[True])
        self.info_wujiang=resources.load_dict_2(PATH+'武将/武将')
        self.load_img_wujiang(PATH)
        self.map_daolu=self.load_map_daolu(PATH+'道路.地图')
        self.shili=resources.load_dict_path(PATH+'势力信息',
                                            resources.load_dict_1,'.势力')

        self.img_chengchi=resources.load_dict_path(PATH+'资源/城池',
                                                   self.fn_img_chengchi,'.png')
        #self.img_wujiang=self.load_img_wujiang(PATH)
        self.img_map=easy_pygame.LoadImg(PATH+'资源/大地图.png')
        #在城池信息中添加位置
        for pos in self.map_chengchi.keys():
            cc=self.map_chengchi[pos]
            self.info_chengchi[cc]['pos']=pos

    def fn_img_chengchi(self,src):
        return easy_pygame.Scale(easy_pygame.LoadImg(src),(200,100))
    
    def load_img_wujiang(self,path):

        for wj in self.info_wujiang.keys():
            self.info_wujiang[wj]['大身像']=easy_pygame.LoadImg(path+'资源/大身像/'+wj+'.jpg')
            self.info_wujiang[wj]['小头像']=easy_pygame.LoadImg(path+'资源/大身像/'+wj+'.jpg') 
        '''
        #大身像
        img_big=resources.load_dict_path(path+'资源/大身像',
                                          easy_pygame.LoadImg,'.jpg')
        #小头像
        img_little=resources.load_dict_path(path+'资源/小头像',
                                            easy_pygame.LoadImg,'.jpg')

        res={}
        for i in img_big.keys():
            res[i]={}
            res[i]['大身像']=img_big[i]
            res[i]['小头像']=img_little[i]

        return res
        '''  
    def load_map_daolu(self,fname):
        res=graph.Graph()
        lines=file(fname).readlines()
        for line in lines:
            line=line.strip()
            if line=='' or line[0]=='#':
                continue
            dat=re.split(r'\s+',line)
            res.AddLink((dat[0],dat[1]))

        return res    

#------------------------------------------------------------------
class SGDatabase(SGDATA):
    def __init__(self,guanka):
        SGDATA.__init__(self,guanka)
        self.load_init()

    def load_init(self):
        ''' 数据初始化'''
        ''' 城池 '''
        for cc in self.info_chengchi.keys():

            self.info_chengchi[cc]['农业']=int(self.info_chengchi[cc]['农业资源']*0.1)
            self.info_chengchi[cc]['商业']=int(self.info_chengchi[cc]['商业资源']*0.1)
            self.info_chengchi[cc]['防灾']=random.randint(0,30)
            self.info_chengchi[cc]['民忠']=random.randint(0,10)
            self.info_chengchi[cc]['后备兵力']=0
            self.info_chengchi[cc]['粮食']=self.info_chengchi[cc]['农业资源']*10
            self.info_chengchi[cc]['金钱']=self.info_chengchi[cc]['商业资源']*10
            self.info_chengchi[cc]['势力']=None
            self.info_chengchi[cc]['太守']=None
            pass

        #初始化城池太守
        for shili in self.shili.keys():
            if shili=="在野":
                continue
            for cc in self.shili[shili].keys():
                self.info_chengchi[cc]['势力']=shili
                self.info_chengchi[cc]['太守']=self.AI_get_taishou(self.shili[shili][cc])       

        #武将
        for wj in self.info_wujiang.keys():
            self.info_wujiang[wj]['兵力']=100
            self.info_wujiang[wj]['忠诚']=random.randint(0,30)
            self.info_wujiang[wj]['官职']="无"
        return

    def world_debug(self,sf):
        '''  在sf上画上网格 ，测试使用'''
        #竖线
        W,H=sf.get_width(),sf.get_height()

        xs,ys,xe,ye=0,0,0,H
        for i in range(0,50):
            pygame.draw.line(sf,(0,255,0),(xs,ys),(xe,ye))
            xs,xe=xs+100,xe+100
        #横线
        xs,ys,xe,ye=0,0,W,0
        for i in range(0,100):
            pygame.draw.line(sf,(0,255,0),(xs,ys),(xe,ye))
            ys,ye=ys+100,ye+100

        #网格编号
        font=pygame.font.SysFont(None,24)
        for i in range(0,100):
            for j in range(0,33):
                sss=font.render(str(i)+':'+str(j), True, (0, 255, 255))
                sf.blit(sss,(i*100,j*100))


    def get_world(self):
        ''' 获取世界 '''
        world=self.img_map.copy() #背景图片
        self.world_debug(world)
        font=pygame.font.Font('../wqy-zenhei.ttc',24)
        
        #画城池
        for pos in self.map_chengchi.keys():
            chengchi=self.map_chengchi[pos]
            x,y=pos
            world.blit(self.get_img_chengchi(chengchi), (x*100,y*100))
            sss=font.render(unicode(chengchi,'utf8'), True, (0,0,0),(255,255,255))
            world.blit(sss,(x*100,y*100))
            pass

        #画道路
        #cc_1,cc_2 城池1 2
        for cc_1,cc_2 in self.map_daolu.Link():
            x1,y1=self.info_chengchi[cc_1]['pos']
            x2,y2=self.info_chengchi[cc_2]['pos']
            pygame.draw.line(world,(255,0,0),(x1*100+100,y1*100+50),(x2*100+100,y2*100+50))
            pygame.draw.circle(world,(255,0,0),(x1*100+100,y1*100+50),5)
            pygame.draw.circle(world,(255,0,0),(x2*100+100,y2*100+50),5)

        return world

    def get_img_chengchi(self,chengchi):
        ''' 根据城池的状态获取城池样式
        chengchi=str(城池名称)
        '''
        status=self.info_chengchi[chengchi]['农业']+self.info_chengchi[chengchi]['商业']
        status=float(status)/2000.0
        max_status=len(self.img_chengchi)-1 #城池图像最大编号
        status=int(round(status*max_status))
        if status>max_status:
            status=max_status
        if status<0:
            status=0
        return self.img_chengchi[str(status)]
    
    def get_wujiang(self,wujiang_list):
        res={}
        for wj in wujiang_list:
            res[wj]=self.info_wujiang[wj]
        
        return res

    def AI_get_taishou(self,wujiang_list):
        ''' 获取智力最高的为太守
        wujiang_list=武将列表["曹操","刘备",..]
        return 
        "曹操"
        '''
        taishou=None
        for wj in wujiang_list:
            if taishou==None:
                taishou=wj
                continue
            try:
                if self.info_wujiang[taishou]['智力']<self.info_wujiang[wj]['智力']:
                    taishou=wj
            except KeyError,e:
                print 'sgdata:AI_get_taishou:KeyError',e.message
        return taishou


    def get_chengchi(self,chengchi):
        ''' '''
if __name__=='__main__':
    import pygame
    from pygame.locals import *

    pygame.init()
    screen = pygame.display.set_mode((100, 100), 0, 32)

    data=SGDATA('董卓弄权')
    '''
    for k in data.info_wujiang.keys():
        print k,
        for i in data.info_wujiang[k].keys():
            print i,':',data.info_wujiang[k][i],
        print ''
        
    '''
    print data.img_wujiang
