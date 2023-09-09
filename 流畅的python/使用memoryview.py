from array import array
#memoryview是一种共享内存的序列类型

octests = array('B', range(6))
m1 = memoryview(octests)  # 使用array初始化一个memoryview对象m1
lm1 = m1.tolist()  # memoryview转换成list
print('lm1',lm1)

m2 = m1.cast('B', [2, 3])  # 把memoryview转换成2行3列
lm2 = m2.tolist()  # memoryview转换成list
print('lm2',lm2)

m3 = m1.cast('B', [3, 2])  # 把memoryview转换成3行2列
lm3 = m3.tolist()  # memoryview转换成list
print('lm3',lm3)

#cast操作只是把对memoryview的数据做了分组，但是其返回的变量仍然是指向的同一份memoryview数据
#所以m3的修改会反映到m2上，因为数据源是同一份

m2[1, 1] = 22
m3[1, 1] = 33
print(octests)
