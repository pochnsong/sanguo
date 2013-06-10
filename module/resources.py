#coding=utf8
import os
import re
import pygame
#-------------------------------------------------------------------
def get_file_list(path,suffix=''):
    '''
    获取文件列表
    '''
    res=[]
    path=os.path.abspath(path)

    if os.path.exists(path)==False:
        return False
    
    if not os.path.isdir(path):
        return [path]
    
    fflist=os.listdir(path)
    
    for ff in fflist:
        fname=path+os.sep+ff
        
        if os.path.isdir(fname):
            flist=get_filelist(fname)
            if flist==False:
                return False
            else:
                res=res+flist
        else:
            if fname.endswith(suffix):
                res.append(fname)
    return res

#-------------------------------------------------------------------

def load_image(src,default={'size':(240,240),'fill':(255,255,255)}):

    try:
        sf=pygame.image.load(src).convert_alpha()
        sf=pygame.transform.smoothscale(sf,default['size'])

    except:
        print '无法打开',os.path.abspath(src)
        sf=pygame.Surface(default['size'])
        sf.fill(default['fill'])

    return sf

#-------------------------------------------------------------------
def load_dict_1(fname,pyeval=[False]):
    '''
    return dict
    以行为单位。
    每行第一个单词为key,其余的单词保存为list格式。
    以#开头的行,为注释
    空行忽略
    例子:
    -----------------
    key1 v1 v2 v3
    key2 v4 v5 v6
    key3 v7 v8 v9
    -----------------
    return 
    {
    key1:[v1 v2 v3],
    key2:[v4 v5 v6],
    key3:[v7 v8 v9]
    }

    '''
    lines=file(fname,'r').readlines()
    res={}

    for line in lines:
        line=line.strip()
        if line=='' or line[0]=='#':
            continue

        dat=re.split(r'\s+',line)
        for i in range(len(pyeval)):
            if pyeval[i]:
                dat[i]=eval(dat[i])

        res[dat[0]]=dat[1:]
    
    return res
#-------------------------------------------------------------------
def load_dict_0(fname,pyeval=[False]):
    '''
    return dict
    以行为单位。
    每行第一个单词为key,后面的为value。
    以#开头的行,为注释
    空行忽略
    例子:
    -----------------
    key1 v1
    key2 v2
    key3 v3
    -----------------
    return 
    {
    key1:v1,
    key2:v2,
    key3:v3
    }
    '''
    lines=file(fname,'r').readlines()
    res={}
    checker=re.compile(r'^(?P<key>\S+)(\s+(?P<value>.*))?')
    for line in lines:
        line=line.strip()
        if line=='' or line[0]=='#':
            continue
        tmp_res=checker.match(line).groupdict()
        dat=[tmp_res['key'],tmp_res['value']]
        for i in range(len(pyeval)):
            if pyeval[i]:
                dat[i]=eval(dat[i])
                pass
            pass
    
        res[dat[0]]=dat[1]
        pass

    return res
#-------------------------------------------------------------------
def load_dict_2(fname):

    '''
    return dict
    以行为单位。
    以#开头的行,为注释
    空行忽略
    例：
    -----------------
          k1 k2 k3
    type  str int str
    key1  a  b  c
    key2  d  e  f
    ----------------
    return dict
    {
    key1:{k1:a,k2:b,k3;c},
    key1:{k1:a,k2:b,k3;c},
    }
    '''    
    #print 'init.LoadInfo,',fname,res
    res={}
    lines=file(fname,'r').readlines()
    keys=re.split(r'\s+',lines[0].strip())
    _T=[str]*(len(keys)+1)

    for line in lines[1:]:
        line=line.strip()
        if line=='' or line[0]=='#':
            continue
        dat=re.split(r'\s+',line)
        dat[0]=_T[0](dat[0])
        info={}
        if dat[0]=='type':
            for i in range(len(dat[1:])):
                _T[i]=eval(dat[i+1])
            continue

        for i in range(len(keys)):
            dat[i+1]=_T[i+1](dat[i+1]) #类型转换            
            info[keys[i]]=dat[i+1]
            pass
        if info:
            res[dat[0]]=info

    return res
#-------------------------------------------------------------------
def load_dict_path(path,load_function,suffix=''):
    '''
    path=目录
    suffix=文件后缀
    load_function=装载文件的函数,load_function(文件名)

    返回以 目录下的文件名(不含后缀)为key，文件内容为value的 dict

    return dict 
    {
    file1:pygame.image,
    file2:pygame.image,
    file3:pygame.image
    }
    '''
    res={}
    flist=get_file_list(path,suffix)
    for ff in flist: #读取每个势力文件

        key=os.path.basename(ff).split('.')[0]
        res[key]=load_function(ff)

    return res
 
