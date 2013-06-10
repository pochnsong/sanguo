#coding=utf8
from DBObject import *

class ShiLi(DBObject):
    ''' 势力
    势力由城池组成
    '''

    def __init__(self,src):
        __T={"势力":"无",#str
             "主公":"未知",#str
             "城池":[],#list class ChengChi
             "史记":"" #str
            }
        DBObject.__init__(self,src,__T)

    def __getitem__(self,key):
        if key=="主公":
            pass

        return DBOBject.__getitem__(self,key)
