#coding=utf8 
""" """
class Loop:
    """ 循环列表 """
    def __init__(self,nodelist,length=0):
        ''' nodelist=[] length:loop长度'''
        self.__list=list(nodelist)
        self.__length=0
        self.set_length(length)
        self.__index=0
    
    def set_length(self,length=0):
        """ 设置长度"""
        if type(length)!=int:
            raise LoopError('lenght is a int type')
        if length<0:
            raise LoopError('lenght must > 0')
        if length:
            self.__length=length
        else:
            self.__length=len(self.__list)

    def get_list(self):
        return self.__list
        
    def get_start(self):
        """ return start index"""
        return self.__index
    def get(self,index=None):
        ''' 获取列表'''
        if index==None:
            index=self.__index

        if type(index)==list:
            _index=index[0]
        else:
            _index=index

        while _index>len(self.__list):
            _index-=len(self.__list)
        while _index<0:
            _index+=len(self.__list)
            
        res=self.__list[_index:_index+self.__length]

        while len(res)<self.__length:
            res=res+self.__list[0:self.__length-len(res)]
        
        self.__index=_index

        if type(index)==list:
            index[0]=_index

        return res
    
    def get_next(self):
        ''' 获取下一个 '''
        return self.get(self.__index+1)
    def get_prev(self):
        ''' 获取上一个 '''
        return self.get(self.__index-1)

class LoopError(Exception):
    def __init__(self,value):
        Exception.__init__(self)
        self.value=value
    def __str__(self):
        return repr(self.value)

    
if __name__=='__main__':

    l=Loop([1,2,3,4,5,6,7,8,9,0],5)
    print l.get_list()
    for i in xrange(0,10):
        print l.get_prev()

