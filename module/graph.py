#coding=utf8

class Graph:
    '''
    适用于SG地图的无向图
    '''

    def __init__(self):
        '''
        __link=[(),(),(),...]
        '''
        self.__link=[]
        
    def AddLink(self,(A,B)):
        '''
        添加边
        '''
        if ((A,B) not in self.__link) or ((B,A) not in self.__link):
            self.__link.append((A,B))

    def Link(self):
        return self.__link


    def GetNext(self,X):
        '''
        获取直接和X点相连接的点
        return 
        [A,B,C]
        '''
        res=[]
        for (A,B) in self.__link:
            if X==A:
                res.append(B)
            elif X==B:
                res.append(A)

        return res

    def Path(self,A,B):
        '''
        计算从A点到B点的最短路径。A!=B
        return
        [A,x,y,B]
        or None

        '''
        pathlist=[[A]]
        while pathlist!=[]:
            tmp_pathlist=[]
            for path in pathlist: #对每条路径搜索
                #print path,
                next_node=self.GetNext(path[-1])
                #print next_node
                if B in next_node:#找到路径
                    return path+[B]

                for node in next_node:
                    if node in path:#循环路径丢弃
                        continue
                    tmp_pathlist.append(path+[node])

            pathlist=tmp_pathlist

        return None
#------------------------------------------------------------------
if __name__=='__main__':
    g=Graph()

    g.AddLink((1,2))
    g.AddLink((2,3))
    g.AddLink((4,3))
    g.AddLink((1,5))


    print g.Link()
    print g.Path(3,1)
