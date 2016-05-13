#coding=utf8 
'''
JJDL.三国 大地图模块
'''
GAME_PATH='../'
SRC_CITY=GAME_PATH+'src/city'
SRC_WORLD='../src/wd.png'
#DATA_MAP='数据/sanguo.map'
#DATA_CITY='数据/city/city'

import pygame
from pygame.locals import *
from sys import exit
import sourcetool
import init
import random

from GUI_chengchi_info import ChengchiInfo
from GUI_chengchi_menu import ChengchiMenu
from GUI_junzhu_info import JunzhuInfo
from GUI_xitong_menu import XitongMenu
from GUI_celue_menu import CelueMenu
from GUI_tishi import Tishi
from GUI_yanqing import YQWuJiang as YQWJ
import mod_wujiang
from db import DB
from mod_rundata import RunData
#---------------------
def Add(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1+x2,y1+y2)
def Sub(pos1,pos2):
    x1,y1=pos1
    x2,y2=pos2
    return (x1-x2,y1-y2)


class ShiJie:
    def __init__(self,guanka):
        ''' '''
        self.guanka=guanka
        self._bg = pygame.image.load(SRC_WORLD).convert()

        self.W,self.H=self._bg.get_width(),self._bg.get_height()
        self._screen=pygame.Surface((self.W,self.H))
        
        self._font= pygame.font.Font("wqy-zenhei.ttc", 18)
        self._create_city()
        self._create_road_dict()
        self.bg=self.create_map()
        pass


    def _create_city(self):
        ''' 创建字典：
        地图上城市信息 dict[地图位置 (x,y)]=城市名称；
        self._name_to_pos_city dict[城市名称]=地图位置 (x,y)
        城市基本信息 dict[城市名称]=图像id；
        城市图像 dict[城市名称]=地图位置,图像
        '''
        self._pos_to_name_city=sourcetool.LoadDatDict('数据/'+self.guanka+'/城池位置.地图',pyeval=True)
        
        self._data_city=sourcetool.LoadDatDict('数据/'+self.guanka+'/城池图像.地图')
        _src_city=sourcetool.LoadSrcDict(SRC_CITY,alpha=True,resize=(200,100))
        self._img_city={}
        for pos in self._pos_to_name_city.keys():
            name=self._pos_to_name_city[pos][0]
            #print name
            src_id=self._data_city[name][0]
            #print src_id
            img=_src_city[src_id].copy()
            name_surface = self._font.render(unicode(name,'utf8'), True, (0,255,255))
            txt_x=(img.get_width()-name_surface.get_width())/2
            txt_y=img.get_height()-name_surface.get_height()
            img.blit(name_surface,(txt_x,txt_y))
            self._img_city[name]=pos,img
        return
    def draw_citys(self):
        ''' 城市'''
            
        for name in self._img_city.keys():
            pos,img=self._img_city[name]
            x,y=pos
            self._screen.blit(img, (x*100,y*100))

    def _create_road_dict(self):
        '''创建道路字典 '''
        self._road_dict=sourcetool.LoadDatDict('数据/'+self.guanka+'/道路.地图')
        self._road_list={}#((x1,y1),(x2,y2))=True
        for name,_data in self._road_dict.iteritems():
            try:
                pos_start,tmp=self._img_city[name]
            except KeyError:
                print '[道路字典] 警告：无效的城市名称',name
                continue
                
            x,y=pos_start
            pos_start=x*100+100,y*100+50
            for city in _data:
                try:
                    pos_end,tmp=self._img_city[city]
                except KeyError:
                    print '[道路字典] 警告：无效的城市名称',city
                    continue
                x,y=pos_end
                pos_end=x*100+100,y*100+50
                self._road_list[pos_start,pos_end]=True
                self._road_list[pos_end,pos_start]=True
                
            pass
        return 
    def draw_roads(self):
        ''' 道路'''
        for pos_start,pos_end in self._road_list.keys():
            pygame.draw.line(self._screen,(255,0,0),pos_start,pos_end,5)
            
        pass
    def create_map(self):
        #竖线
        self._screen.blit(self._bg, (0,0))
        
        xs,ys,xe,ye=0,0,0,self.H
        for i in range(0,50):
            pygame.draw.line(self._screen,(0,255,0),(xs,ys),(xe,ye))
            xs,xe=xs+100,xe+100
        #横线
        xs,ys,xe,ye=0,0,self.W,0
        for i in range(0,100):
            pygame.draw.line(self._screen,(0,255,0),(xs,ys),(xe,ye))
            ys,ye=ys+100,ye+100

        for i in range(0,100):
            for j in range(0,33):
                sss= self._font.render(str(i)+':'+str(j), True, (0, 255, 255))
                self._screen.blit(sss,(i*100,j*100))
        self.draw_citys()
        self.draw_roads()
        return self._screen

    def get_width(self):
        return self.W
    def get_height(self):
        return self.H
    def isin(self,pos):
        ''' 检查是否选中城市 pos 鼠标坐标 '''
        x,y=pos
        i,j=x/100,y/100
        name=self._pos_to_name_city.get((i,j))
        if name:
            return name
        
        return self._pos_to_name_city.get((i-1,j))


#-----------
class Load:
    def __init__(self,screen):
        self.screen=screen
        self.y=0
        self.font=pygame.font.Font('wqy-zenhei.ttc',18)
        screen.fill((0,0,0))

    def load(self,text):
        text=self.font.render(unicode(text,'utf8'),True,(0,255,0))
        self.screen.blit(text,(0,self.y))
        pygame.display.update()
        self.y+=20

#-----------
def run(screen,guanka,myshili):
    logo=Load(screen)
    logo.load('装载DB...')
    db=DB(guanka,myshili)
    logo.load('装载RunData')
    rundb=RunData(db)
    logo.load('装载Shijie')
    sj=ShiJie(guanka)
    logo.load('GUI 初始化...')

    mouse_down=False
    
    screensize=(screen.get_width(),screen.get_height())
    gui_chengchi_xinxi=None
    gui_chengchi_caidan=None
    gui_junzhu_xinxi=JunzhuInfo((300,0),myshili,db)
    gui_celue_caidan=CelueMenu( Sub( (screen.get_width(),0),(120,0) ) )
    gui_xitong_caidan=XitongMenu((screen.get_width(),screen.get_height()))
    gui_tishi=None
    gui_yanqing_wujiang=None
    map_offset=(0,0)

    while True:        
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if gui_tishi and gui_tishi.event(event):
                gui_tishi=None
                continue
            
            if gui_yanqing_wujiang:
                res=gui_yanqing_wujiang.event(event)
                if res:
                    if res!=True:
                        gui_tishi=rundb.run_menu('宴请',(gui_chengchi_xinxi.chengchi,res))
                        gui_chengchi_xinxi.update()
                    continue

            if gui_xitong_caidan.event(event):
                continue
            
            if gui_chengchi_xinxi:
                if gui_chengchi_xinxi.event(event):
                    continue
                select=gui_chengchi_caidan.event(event)
                if select:
                    if select=='宴请':
                        wj=db.get_wujiang_list_from_chengchi(gui_chengchi_xinxi.chengchi)
                        gui_yanqing_wujiang=YQWJ((200,0),wj,size=(600,400))
                        continue
                    if select!=True:
                        wj=db.get_wujiang_list_from_chengchi(gui_chengchi_xinxi.chengchi)
                        wjlist=mod_wujiang.run(screen,wj,select)
                        if wjlist:
                                
                            gui_tishi=rundb.run_menu(select,(gui_chengchi_xinxi.chengchi,wjlist))
                            gui_chengchi_xinxi.update()
                    continue

            if event.type == QUIT:
                exit()
            if event.type ==MOUSEBUTTONDOWN:
                mouse_down=True
                fd=sj.isin(Sub(event.pos,map_offset))
                if fd:
                    gui_chengchi_xinxi=ChengchiInfo((0,0),fd[0],db,screen)
                    gui_chengchi_caidan=ChengchiMenu(event.pos)
                else:
                    gui_chengchi_xinxi=None
                    gui_chengchi_caidan=None

                gui_yanqing_wujiang=None

            if event.type ==MOUSEBUTTONUP:
                mouse_down=False
            if event.type ==MOUSEMOTION:
                if mouse_down:
                    map_offset=Add(map_offset,event.rel)
                    if gui_chengchi_caidan:
                        gui_chengchi_caidan.menu.pos=Add(gui_chengchi_caidan.menu.pos,event.rel)
        screen.blit(sj.bg, map_offset)

        #"是否显示城市信息"
        if gui_chengchi_xinxi:
            gui_chengchi_xinxi.show(screen)
            gui_chengchi_caidan.show(screen)

        gui_junzhu_xinxi.show(screen)
        gui_xitong_caidan.show(screen)
        gui_celue_caidan.show(screen)

        if gui_yanqing_wujiang:
            gui_yanqing_wujiang.show(screen)

        if gui_tishi:
            gui_tishi.show(screen)
        pygame.display.update()

if __name__=='__main__':
    XWIDTH,XHEIGHT=800,560

    pygame.init()
    screen = pygame.display.set_mode((XWIDTH, XHEIGHT), 0, 32)
    pygame.display.set_caption("JJDL.三国")
    #-----------
    run(screen,'董卓弄权','刘备')
