# 就地运算指的是像+=，-=，*=，/=这样的运算

#就地运算在可变数据对象中的表现
l = [1,2,3]
print(id(l))
l *= 2
print(id(l))    #对于可变对象，就地运算前后数据对象还是同一个，其id保持不变

#就地运算在不可变对象中的表现
t = (1,2,3)
print(id(t))
t *= 2
print(id(t))    #对于不可变对象，就地运算前后数据对象不在是同一个，id值前后不一致，也就是在运算后，生成了新的对象

#尽量不要再不可变对象中添加可变对象类型的数据
#下面的语句会引发error
try:
    t = (1,2,[3,4])
    t[2] += [4,5]   #抛出异常，'tuple' object does not support item assignment
except Exception as e:
    print(e)


#即使在不可变数据类型中保存的是可变数据类型的引用变量那么也有问题
try:
    li=[33,44]
    t1 = (1,2,li)
    t1[2] += [5,6]  # 抛出异常，'tuple' object does not support item assignment
    print(t1)
except Exception as e:
    print(e)

