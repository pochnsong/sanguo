#coding=utf8
from DBObject import *

class ChengChi(DBObject):
    ''' 城池
    '''
    def __init__(self,src):
        __T={"城池":"名称",#str
             "太守":None,#str
             "武将":[],#list 势力武将
             "在野":[],#list 在野武将
             "仓库":[],#list 仓库道具
             "监狱":[], #list 俘虏
             "金钱":0,#int
             "粮食":0, #int
             "特产":[],#list 城市特产
             "城技":[],#list 城市技能
             "人口":0,#int 
             "农业资源":0,#int
             "农业":0,#int
             "商业资源":0,#int
             "商业":0,#int
             "防灾":0,#int 0-100
             "民忠":0,#int 0-100
             "后备兵力":0
            }

        DBObject.__init__(self,src,__T)
        
    def get_taishou(self):
        taishou=DBObject.__getitem__(self,"太守")
        if taishou:
            return self["武将"][taishou]

        return None
        
    def get_nongyeziyuan(self):
        ''' 获取农业资源'''
        taishou=self.get_taishou()
        res=DBObject.__getitem__(self,"农业资源")
        if taishou:
            res=res+int(res*(taishou['智力']-50)/50.0)
                        
        return res

    def get_shangyeziyuan(self):
        ''' 获取商业资源'''
        taishou=self.get_taishou()
        res=DBObject.__getitem__(self,"商业资源")
        if taishou:
            res=res+int(res*(taishou['智力']-50)/50.0)
            
        return res

    def get_active_wujiang(self):
        ''' 获取所有处于活跃状态的武将'''
        res=[]
        for wj in DBObject.__getitem__(self,"武将"):
            if wj.active:
                res.append(wj)
        return res

    def set_all_active(self,active):
        ''' 设置所有武将活跃性'''
        for wj in DBObject.__getitem__(self,"武将"):
            wj.active=active

    def get_dict(self,key):
        res={}
        for wj in DBObject.__getitem__(self,key):
            res[wj[key]]=wj
        return res

    def __getitem__(self,key):
        if key=="太守":
            return self.get_taishou()

        if key=="农业资源":
            return self.get_nongyeziyuan()

        if key=="活跃武将":
            return self.get_active_wujiang()

        if key=="武将":
            return self.get_dict("武将")
        if key=="武将列表":
            return DBObject.__getitem__(self,"武将")

        return DBObject.__getitem__(self,key)


if __name__=="__main__":
    from obj_WuJiang import *
    from obj_DaoJu import *
    cc=ChengChi({"太守":"诸葛亮",
                 "农业资源":1000,
                 "武将":
                     [WuJiang({"武将":"诸葛亮",
                               "智力":100,
                               "道具":[DaoJu({"道具":"春秋","智力":10})]})
                      ]           
            })
    print '太守',cc["太守"]
    print cc["农业资源"]
    print '-'*30
    print cc["武将"]["诸葛亮"]
    print "::",cc["武将列表"]
    cc.set_all_active(False)
    print '-'*30
    print cc["活跃武将"]
