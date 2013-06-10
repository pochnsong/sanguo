#coding=utf8
'''
读取势力列表
'''
import os
import re
import sys
sys.path.append('..')
import module.resources as resources

def get_shili_list(path):
    """
    return 
    {
    君主：{城池:[武将列表]}
    }
    """
    shili={}
    flist=resources.get_file_list(path,'.势力')
    for ff in flist:
        #读取每个势力文件
        junzhu=os.path.basename(ff).split('.')[0]
        shili[junzhu]=resources.load_dict_1(ff)
    
    return shili

if __name__=="__main__":
    #shili=get_shili_list('../数据/董卓弄权/势力信息')
    shili=resources.load_dict_path('../数据/董卓弄权/势力信息',
                                   resources.load_dict_1,'.势力')

    #print shili

    for junzhu in shili.keys():
        print junzhu
        for chengchi in shili[junzhu].keys():
            print ' ',chengchi
            print '\t',
            '''for wj in shili[junzhu][chengchi]:
                print wj,'''
            print ' '
