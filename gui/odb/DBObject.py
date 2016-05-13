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

