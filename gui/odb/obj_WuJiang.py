#coding=utf8
from DBObject import *
class WuJiang(DBObject):
    ''' 武将类 '''
    def __init__(self,wujiang):
        
        __T={"武将":"无名氏",#str
             "兵种":"步兵",#str
             "兵力":0,#int
             "武力":0,#int
             "智力":0,#int
             "道具":[],#[] str
             "官职":None,# str
             "技能":[]
             }

        DBObject.__init__(self,wujiang,__T)
        self.active=True #武将活动状态，处于活动状态的武将可以执行策略指令

    def get_zhili(self):
        ''' 获取智力'''
        res=DBObject.__getitem__(self,"智力")
        for dj in self.__getitem__("道具"):
            res+=dj["智力"]
        return res

    def get_wuli(self):
        ''' 获取武力'''
        res=DBObject.__getitem__(self,"武力")
        for dj in self.__getitem__("道具"):
            res+=dj["武力"]
        return res

    def __getitem__(self,key):
        if key=="武力":
            return self.get_wuli()
        if key=="智力":
            return self.get_zhili()

        return DBObject.__getitem__(self,key)

if __name__=="__main__":
    wj=WuJiang({
            })

    print wj
