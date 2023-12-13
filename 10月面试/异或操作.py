# ######
# 异或操作
# ######
# 两数的异或操作，就是在二进制的各个位上，数据相同为0，不同为1——这是普通的异或定义
# 更加容易记录的方式就是——异或操作就是无进位的相加

# 3^6
# 0 1 1
# 1 1 0
# 1 0 1 ->3
# 形同的位异或后为0，等同于相同的位相加，舍弃进位，如 1^1=0，就是1+1=10舍弃进位1为0，1^0=1相当于1+0=1无进位

# #####################
# 异或操作满足交换律和结合率
# #####################
# a^b^c = a^c^b = b^a^c = b^c^a = ...

# 既然数据的异或操作是无进位相加，那么a,b,c 各个数据在二进制形式上，1和0的顺序和位置是固定的
# a=2,b=6,c=7
# a 0 1 0
# b 1 1 0
# c 1 1 1

# 异或看成是纵向的各个位无进位相加，那么无论a，b，c的顺序如何变化，结果都是一样的，所以，只要数据是同一批，异或时各个数据的顺序无关紧要，已获得结果是一样的

# ###########
# 异或的几种用法
# ###########
# 数据交换
a,b = 10,100

a = a^b  #1
b = a^b  #2
a = a^b  #3

# 原理:在#1 处，a=a^b,那么带入#2,里面 b = a^b^b，数据异或自身，那结果为0，所以b= a^b^b = a^0 = a,此时b的值交换为了a，注意此时a仍然等于a=a^b,而b=a
# 在#3处，a=a^b,b=a 带入a = a^b = (a^b)^a = a^a^b = 0^b ，此时a和b完成交换

# 在一组数据中有一个数据出现了奇数次，其他的数据都是偶数次
# 使用异或操作的结合和交换律，因为如果是偶数次出现的数据，那么异或的结果一定是0，如果是奇数次出现的记过，异或的结果一定是数据自身，而同一批次的数据，异或的顺序无关紧要
# 数据依次异或操作即可，结果必然是出现偶数次的那个数据的值
import random
li = [1,1,2,2,3,3,3,3,4,4,4]
ret=0
for each in li:
    ret^=each
print(ret)  # 4

# 在一组数据中有两个数a,b出现的次数为奇数次，找出这两个数据
li=[3,3,4,4,6,6,10,10,10,12,12,12]
xor = 0
for each in li:
    xor ^= each # xor = a^b
print('xor:',xor)
rightone = (~xor+1) & xor
# print('rightone:',rightone)

n = 0
for each in li:
    if each&rightone == rightone:
        # 通过rightone和each相与，把数据分为两类，而偶数次的数据异或终究是0，不影响最终异或结果，最终n记录的就是两个出现奇数次的两个结果的其中一个
        n ^= each
print(n,n^xor)

# 获取数字N的二进制形式上的1有多少位
n = 100;cnt = 0
while n != 0:
    rightone = (~n+1)&n
    cnt+=1
    # n = n^rightone
    n^=rightone
print(f'100的二进制一共有{cnt}个1')

