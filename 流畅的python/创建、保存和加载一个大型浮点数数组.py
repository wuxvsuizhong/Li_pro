from array import array
from random import  random
#如果是数据只有数字类型，那么array.array比list更合适，它效率更快

#创建1000万个随机浮点数
floats = array('d',(random() for i in range(10**7)))
print(floats[-1])

fp = open('floats.bin','wb')
floats.tofile(fp)
fp.close()

with open('floats.txt','w') as fp:
    for each in floats[:10000]:
        fp.write(str(each)+'\n')

floats2 = array('d')
fp = open('floats.bin','rb')
floats2.fromfile(fp,10**7)
fp.close()
print(floats2[-1])
print(floats2 == floats)