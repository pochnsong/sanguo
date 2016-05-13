#coding=utf8
from DBObject import *
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

    
