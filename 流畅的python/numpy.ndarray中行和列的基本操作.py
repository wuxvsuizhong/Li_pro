import numpy
import numpy as np

a = np.arange(12)  # 创建一个ndarray数组
print(a)  # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print(type(a))  # <class 'numpy.ndarray'>
print('a.shape', a.shape)  # 查看数组维度
a.shape = 3, 4  # 增加一个维度（3行4列)
print('a->', a)  # 按照上一句设置的3行4列打印数组a
print('a[2]->', a[2])  # [ 8  9 10 11]
print('a[2,1]->', a[2, 1])  # 9
print('a[:,1]->', a[:, 1])  # [1 5 9]  获取各个行的下标为1的元素
a1 = a.transpose()  # 行列转换
print("a1->", a1)

# 从文件读取数据
floats = numpy.loadtxt('floats.txt')
print(floats[-3:])  # 获取最后3个数
floats *= 5  # 把floats中每个数据都乘以5
print(floats[-3:])  # 获取最后3个数

from time import perf_counter as pc #导入高分辨率新能衡量计时器
t0=pc()
floats /= 3
print(pc()-t0) #打印运行时间

numpy.save('floats.npy',floats)
t0=pc()
floats2 = numpy.load('floats.npy','r+')
floats2 *= 6
print(pc()-t0) #打印运行时间

print(floats2[-3:])