# 切片对象命令，可以设置slice对象，在slice中指定要截取的字符串的序号段
# 然后使用可迭代对象item[SliceName]方式来固定截取迭代中的某些位置段的元素

s='''
1909 Pimormi                $17.60  3   $30
1489 6mm Taci Swi           $20.01  5   $40'''
SKU = slice(0,5)
DISCRIPTION = slice(5,29)
UNITPRICE = slice(29,36)

items = s.split('\n')[1:]
for item in items:
    print(item[DISCRIPTION],item[UNITPRICE])

# 可迭代对象中切片区域赋值
l = list(range(10))
print(l)
l[2:5] = [20,30]    #把2-5之间（不包含5）的元素替换为20,30
print(l)
# 切片区域del
del l[5:7]      #删除序号为5,6位置的元素
print(l)
l[3::2] = [11,22]   #把l从下标3开始,后面每增加步长2的元素依次替换为11,22
print(l)
# l[2:5] = 100      #Error,切片区域赋值需要时一个了迭代对象，即使只有1个值也要用可迭代的数据对象包含
# print(l)
l[2:5] = [100]  #把从2-5(不包含5)区域的数据替换为100
print(l)

