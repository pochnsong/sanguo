#coding=utf8
class DBObject(dict):
    def __init__(self,src_dict,T_dict=None):
        ''' T_dict=模板'''
        if T_dict:
            for key in T_dict.keys():
                if not src_dict.has_key(key):
                    src_dict[key]=T_dict[key]
                    
        dict.__init__(self,src_dict)

    def __repr__(self):
        res="{"
        __split=False
        for key in self.keys():
            if __split:
                res+=","
            else:
                __split=True
            res+=key+':'+str(self.__getitem__(key))

        res+="}"
        return res


#--------------------------------------------------
class JN(DBObject):
    ''' 技能'''
    def __init__(self,src):
        __T={"技能":"未知",#str
             "描述":"无",#str
             "使用函数":None
             }
        DBObject.__init__(self,src,__T)
#--------------------------------------------------
class DaoJu(DBObject):
    ''' 道具'''
    def __init__(self,daoju):
        __T={"道具":"未命名",#str
             "描述":"无",#str
             "智力":0,#int
             "武力":0,#int
             "移动":0,#int
             "技能":[],#[]
             "使用函数":None
             }

        DBObject.__init__(self,daoju,__T)
 
dj=DaoJu({"道具":"方天画戟",
          "武力":10,
          "智力":0,
          "技能":[]
        })
print dj
#--------------------------------------------------
class GuanZhi(DBObject):
    ''' 官职'''
    def __init__(self,guanzhi):
        __T={"官职":"布衣",#str
                "俸禄":{"金钱":0,"粮食":0},#dict
                "技能":[],#[]
                "领兵数量":1 #int
                }
        DBObject.__init__(self,guanzhi,__T)
    
#--------------------------------------------------
class BingZhong(DBObject):
    ''' 兵种'''
    def __init__(self,bingzhong):
        __T={"兵种":"未知兵种",#str
             "移动":0,#int
             "克制":None,#str
             "技能":[]#[]
             }
        DBObject.__init__(self,bingzhong,__T)
#--------------------------------------------------
class WuJiang(DBObject):
    ''' 武将类 '''
    def __init__(self,wujiang):
        __T={"武将":"无名氏",#str
             "兵种":"步兵",#str
             "兵力":0,#int
             "武力":0,#int
             "智力":0,#int
             "道具":[],#[] str
             "官职":"布衣",# str
             "技能":[]
             }

        DBObject.__init__(self,wujiang,__T)

    def get_zhili(self):
        ''' 获取智力'''
        res=Dict.__getitem__(self,"智力")
        for dj in self.__getitem__("道具"):
            res+=dj["智力"]
        return res

    def get_wuli(self):
        ''' 获取武力'''
        res=Dict.__getitem__(self,"武力")
        for dj in self.__getitem__("道具"):
            res+=dj["武力"]
        return res

    def __getitem__(self,key):
        if key=="武力":
            return self.get_wuli()
        if key=="智力":
            return self.get_zhili()

        return Dict.__getitem__(self,key)


class ChengChi(DBObject):
    ''' 城池'''
    pass


class Shili(DBObject):
    
