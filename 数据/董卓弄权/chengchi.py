#coding=utf8

import random 

fi=open('城池位置.地图','r')
fo=file('cc.地图','w')

sssline=fi.readlines()

for sss in sssline:
    fo.write(sss.strip()+'\t')
    fo.write(str(random.randint(0,8))+'\n')

fo.close()
fi.close()
